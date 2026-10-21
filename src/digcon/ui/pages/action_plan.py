"""Finding-led operational plan, persisted with the assessment."""
import streamlit as st
from digcon.domain.action_plan import ACTIONS, approved, approval_ready, findings, fingerprint, title
from digcon.domain.models import ActionPlanItem
from .. import state
from ..labels import PHASE_TITLES, REVIEW_TITLE

FIELDS = {
    'action': 'What will be done?', 'rationale': 'How does this action address this problem?',
    'owner': 'Responsible person or team', 'due_date': 'Target date (YYYY-MM-DD)',
    'implementation': 'What has been implemented?',
    'evidence_refs': 'Implementation evidence (one reference per line)',
    'verification_method': 'How was effectiveness checked?',
    'verification_result': 'What did the check establish for this problem?',
    'verification_evidence': 'Verification evidence (one reference per line)',
    'reviewer': 'Reviewer', 'review_date': 'Review date (YYYY-MM-DD)',
    'decision_reason': 'Reason for the review decision',
}


def _sync(rid):
    old = state.store().setdefault('action_plan', {}).get(rid, {})
    data = {'rule_id': rid, **old}
    for field in [*FIELDS, 'status']:
        key = f'w.plan.{rid}.{field}'
        if key not in st.session_state: continue
        value = st.session_state[key]
        data[field] = [x.strip() for x in value.splitlines() if x.strip()] if field.endswith('evidence') or field == 'evidence_refs' else value
    state.store()['action_plan'][rid] = ActionPlanItem.model_validate(data).model_dump(mode='json')


def _decide(rid, decision):
    _sync(rid)
    s = state.assessment()
    item = s.action_plan[rid]
    if decision == 'RESOLVED' and not approval_ready(item):
        st.session_state['plan_message'] = 'Complete the action, responsibility, implementation, verification, evidence and review fields first.'
        return
    data = state.store()['action_plan'][rid]
    history = list(data.get('review_history', []))
    current_fingerprint = fingerprint(s, rid)
    history.append({**{k: data.get(k) for k in ['reviewer','review_date','decision_reason']},
                    'decision': decision, 'reviewed_fingerprint': current_fingerprint})
    data.update(decision=decision, reviewed_fingerprint=current_fingerprint, review_history=history)


def _choose_measure(rid):
    st.session_state['plan_focus'] = rid
    st.session_state['w.plan_view'] = 'Catalogue measures'


def _field(rid, field, stored):
    value = stored.get(field, '')
    if isinstance(value, list): value = '\n'.join(value)
    key = f'w.plan.{rid}.{field}'
    state.seed(key, value)
    short = field in ('owner', 'due_date', 'reviewer', 'review_date')
    widget = st.text_input if short else st.text_area
    widget(FIELDS[field], key=key, on_change=_sync, args=(rid,))


def render(cfg, result):
    st.markdown('Start from the problem, record what must be done and return here when you resume your assessment. '
                '**Completing an action does not itself resolve a finding or remove a stop condition.**')
    if 'plan_message' in st.session_state: st.warning(st.session_state.pop('plan_message'))
    records = state.store().setdefault('action_plan', {})
    cards = findings(result, records)
    st.caption(f'{len(cards)} work items · {sum(v.get("status") == "IN_PROGRESS" for v in records.values())} in progress · '
               f'{sum(v.get("status") == "AWAITING_REVIEW" for v in records.values())} awaiting review')
    if not cards:
        st.success('No open finding currently needs an action.')
        return
    focus = st.session_state.get('plan_focus')
    for rid, info in sorted(cards.items(), key=lambda x: (x[0] != focus, not x[0].startswith('HS'), title(x[0]))):
        stored = records.get(rid, {})
        with st.expander(title(rid), expanded=rid == focus):
            st.caption(' · '.join(info['kinds']))
            if rid.startswith('HS'):
                steps = ('Read the facts and the grounds for the stop condition; identify what would need to change.',
                         'Document any changes and obtain a new reasoned legal determination. This action card cannot override the stop condition.')
            elif rid in ACTIONS:
                steps = ACTIONS[rid]
            else:
                steps = ('Review the source information below and specify the missing evidence or corrective action.',
                         'Record who will act, implement the action and submit the evidence for review.')
            st.markdown('**First:** ' + steps[0] + '\n\n**Then:** ' + steps[1])
            qids = [q for q in result.rules[rid].input_ids if any(x.id == q for x in cfg.questions.questions)] if rid in result.rules else []
            with st.expander('Information used in this finding'):
                for qid in qids:
                    q = cfg.question(qid); a = state.store()['answers'].get(qid, {})
                    st.markdown('**' + q.text + '**')
                    st.write(a.get('value') or a.get('state') or 'Not answered')
                    if a.get('detail'): st.write(a['detail'])
                    st.button('Review this answer', key=f'plan.source.{rid}.{qid}', on_click=state.go, args=(PHASE_TITLES[q.phase],))
                if not qids: st.caption('This finding requires review of the assessment evidence and judgement.')
            for f in ['action','rationale','owner','due_date']: _field(rid, f, stored)
            key=f'w.plan.{rid}.status'; state.seed(key, stored.get('status', 'TODO'))
            st.selectbox('Work progress', ['TODO','IN_PROGRESS','AWAITING_REVIEW'], key=key,
                         format_func=lambda v: {'TODO':'To do','IN_PROGRESS':'In progress','AWAITING_REVIEW':'Ready for review'}[v],
                         on_change=_sync,args=(rid,))
            with st.expander('Implementation and verification'):
                for f in ['implementation','evidence_refs','verification_method','verification_result','verification_evidence']:
                    _field(rid,f,stored)
            linked = [m for m in state.assessment().mitigations.values() if rid in m.linked_rule_ids and m.activated]
            st.caption('Linked catalogue measures: ' + ('; '.join(cfg.mitigation(m.mitigation_id).measure for m in linked) or 'None yet'))
            st.button('Choose a measure for this problem', key=f'plan.measure.{rid}',
                      on_click=_choose_measure, args=(rid,))
            st.caption('Linking a measure alone never closes this finding.')
            with st.expander('Review of this specific finding'):
                for f in ['reviewer','review_date','decision_reason']: _field(rid,f,stored)
                if rid.startswith('HS'):
                    st.button('Reopen legal assessment', key=f'plan.hs.{rid}',on_click=state.go,args=(REVIEW_TITLE,))
                else:
                    st.button('Approve resolution for this finding',key=f'plan.resolve.{rid}',on_click=_decide,args=(rid,'RESOLVED'))
                    st.button('Keep this finding open',key=f'plan.open.{rid}',on_click=_decide,args=(rid,'OPEN'))
                current = state.assessment()
                if stored.get('decision') == 'RESOLVED':
                    if approved(current,rid): st.success('Resolution approved for the recorded evidence. The engine still checks all applicable conditions.')
                    else: st.warning('The approval is incomplete or its supporting information changed. Review again.')
                elif stored.get('decision') == 'OPEN': st.info('Reviewer decision: the finding remains open.')
                st.caption('Missing answers must be updated at source. An approval does not erase evidence gaps or legal stop conditions.')
            with st.expander('Technical details'):
                st.code(rid)
                st.write(info['ids'])
                if stored.get('review_history'): st.json(stored['review_history'])

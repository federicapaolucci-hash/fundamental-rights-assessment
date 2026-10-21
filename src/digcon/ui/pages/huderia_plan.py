"""HUDERIA-informed impact mitigation plan, independent of T17 decision outcomes."""
from __future__ import annotations
import streamlit as st
from digcon.domain.models import ImpactMitigationPlan, ConfigBundle
from digcon.engine import EngineResult
from .. import state

FIELDS = [
    ("title", "Impact title"),
    ("impact_description", "Potential or actual adverse impact"),
    ("affected_people", "Affected persons and groups"),
    ("context_and_interdependencies", "Vulnerabilities, context and interdependencies (COBRA)"),
    ("stakeholder_input", "Input from affected people, or reason it is not available"),
    ("priority_reason", "Reason for priority: severity, probability and reversibility"),
    ("avoid", "AVOID — changes to prevent the adverse impact"),
    ("mitigate", "MITIGATE — actions to minimise the impact"),
    ("restore", "RESTORE — steps to repair harm already caused"),
    ("compensate", "COMPENSATE — where appropriate and legally available"),
    ("legal_constraints", "Legal obligations and restrictions, with sources"),
    ("responsible_actors", "Division of responsibilities across relevant actors"),
    ("responsible_owner", "Accountable owner"),
    ("target_date", "Deadline or trigger"),
    ("remedy_access", "How affected people can access review and remedies"),
    ("monitoring_method", "Indicators, tests and escalation triggers"),
    ("monitoring_owner", "Person responsible for monitoring"),
    ("review_date", "Next review date"),
    ("reviewer", "Effectiveness reviewer"),
    ("review_reason", "Reasoned result of effectiveness review"),
]

def _add():
    plans = state.store().setdefault("impact_plans", {})
    n = 1
    while f"IMPACT-{n:03d}" in plans:
        n += 1
    iid = f"IMPACT-{n:03d}"
    plans[iid] = ImpactMitigationPlan(impact_id=iid).model_dump(mode="json")
    st.session_state["huderia.focus"] = iid

def _save(iid):
    current = dict(state.store()["impact_plans"][iid])
    for name, _ in FIELDS:
        key = f"w.huderia.{iid}.{name}"
        if key in st.session_state:
            current[name] = st.session_state[key].strip()
    for name in ("occurrence", "priority", "risk_ids", "status"):
        key = f"w.huderia.{iid}.{name}"
        if key in st.session_state:
            current[name] = st.session_state[key]
    for name in ("implementation_evidence", "verification_evidence"):
        key = f"w.huderia.{iid}.{name}"
        if key in st.session_state:
            current[name] = [x.strip() for x in st.session_state[key].splitlines() if x.strip()]
    # A dropdown alone never proves effectiveness; record a reasoned review and evidence.
    if current["status"] == "EFFECTIVENESS_REVIEWED":
        required = ("reviewer", "review_reason", "responsible_owner", "monitoring_method")
        if any(not current.get(k) for k in required) or not current["implementation_evidence"] or not current["verification_evidence"]:
            current["status"] = "IMPLEMENTING"
            st.session_state[f"w.huderia.{iid}.status"] = "IMPLEMENTING"
    state.store()["impact_plans"][iid] = ImpactMitigationPlan.model_validate(current).model_dump(mode="json")

def _delete(iid):
    state.store()["impact_plans"].pop(iid, None)
    for k in list(st.session_state):
        if str(k).startswith(f"w.huderia.{iid}."):
            del st.session_state[k]

def _field(iid, name, label, stored):
    key = f"w.huderia.{iid}.{name}"
    state.seed(key, stored.get(name, ""))
    if name in ("title", "responsible_owner", "monitoring_owner", "target_date", "review_date", "reviewer"):
        st.text_input(label, key=key, on_change=_save, args=(iid,))
    else:
        st.text_area(label, key=key, height=82, on_change=_save, args=(iid,))

def render(cfg: ConfigBundle, result: EngineResult):
    st.markdown("**HUDERIA-informed mitigation planning** starts with the adverse impacts identified in the assessment, not a list of triggered rules. Scope and prioritise impacts by severity and probability, including contextual vulnerabilities, then consider **AVOID → MITIGATE → RESTORE → COMPENSATE**. Assign roles, provide access to remedy and establish iterative monitoring.")
    st.caption("Draft plans do not close assessment findings, reduce residual risks or override legal stop conditions.")
    plans = state.store().setdefault("impact_plans", {})
    st.button("Add an adverse impact", on_click=_add, type="primary")
    if not plans:
        st.info("No adverse impacts have been added. Start with an impact on affected persons, then document what must be done.")
        return
    risk_specs = {r.id: getattr(r, 'right', r.id).split(';')[0] for r in cfg.risks.risks}
    initial_risks = state.store().get("risks", {})
    for iid, data in list(plans.items()):
        with st.expander((data.get("title") or "New adverse impact") + " · " + data.get("priority", "UNDETERMINED").replace("_"," ").title(), expanded=st.session_state.get("huderia.focus")==iid):
            st.markdown("**1. Describe the impact and affected persons**")
            for name, label in FIELDS[:5]:
                _field(iid, name, label, data)
            for name, opts, label in [
                ("occurrence", ["POTENTIAL","ACTUAL","BOTH"], "Has the impact already occurred?"),
                ("priority", ["UNDETERMINED","IMMEDIATE","HIGH","STANDARD"], "Priority for action"),
            ]:
                key=f"w.huderia.{iid}.{name}"
                state.seed(key,data.get(name,opts[0]))
                st.selectbox(label,opts,key=key,format_func=lambda x:x.replace("_"," ").title(),on_change=_save,args=(iid,))
            key=f"w.huderia.{iid}.risk_ids"
            state.seed(key,data.get("risk_ids",[]))
            st.multiselect("Related assessed rights risks",list(risk_specs),key=key,format_func=lambda x:risk_specs[x],on_change=_save,args=(iid,))
            for rid in st.session_state[key]:
                r=initial_risks.get(rid,{})
                st.caption("Existing assessment — "+" · ".join(f"{n}: {r.get(n) or 'Not rated'}" for n in ("scale","scope","reversibility","probability")))
            _field(iid,*FIELDS[5],data)
            st.markdown("**2. Choose actions in the mitigation hierarchy**")
            for name,label in FIELDS[6:10]:
                _field(iid,name,label,data)
            st.markdown("**3. Legal context, responsibilities and remedies**")
            for name,label in FIELDS[10:15]:
                _field(iid,name,label,data)
            with st.expander("4. Monitoring and verification (after implementation)"):
                for name,label in FIELDS[15:]:
                    _field(iid,name,label,data)
                for name,label in [("implementation_evidence","Implementation evidence (one reference per line)"),("verification_evidence","Effectiveness evidence (one reference per line)")]:
                    key=f"w.huderia.{iid}.{name}"
                    state.seed(key,"\n".join(data.get(name,[])))
                    st.text_area(label,key=key,on_change=_save,args=(iid,))
                key=f"w.huderia.{iid}.status"
                state.seed(key,data.get("status","DRAFT"))
                st.selectbox("Record status",["DRAFT","PLANNED","IMPLEMENTING","EFFECTIVENESS_REVIEWED"],key=key,on_change=_save,args=(iid,),format_func=lambda x:x.replace("_"," ").title())
                st.caption("Recorded evidence and review are documentation, not automatic proof that mitigation worked.")
            st.button("Remove this impact",key=f"delete.{iid}",on_click=_delete,args=(iid,))

def render_catalogue(cfg, result):
    st.caption("These are candidate measures from T17, not a mitigation plan. They do not become effective automatically.")
    risks=set(state.store().get("risks",{}))
    eligible=[m for m in cfg.mitigations.mitigations if m.risk_id in risks]
    st.caption(f"{len(eligible)} candidate measures associated with assessed risks.")
    for m in eligible:
        with st.expander(m.measure[:120]):
            st.write(m.measure)
            st.caption(f"Suggested responsible role: {m.responsible_role}. Actual responsibilities must be verified.")

def render_page(cfg, result):
    a,b=st.tabs(["Impact mitigation plan (HUDERIA)","Candidate measures (reference only)"])
    with a: render(cfg,result)
    with b: render_catalogue(cfg,result)

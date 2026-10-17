"""Markdown report of one engine run: outcome, what to do next, answers, registers, governance, audit trail."""

from __future__ import annotations

from digcon.domain.enums import ElementSource, label
from digcon.domain.models import AssessmentState, ConfigBundle, ElementEvaluation
from digcon.engine import EngineResult
from digcon.ui.labels import APP_TITLE, DISCLAIMER, FOOTER, OUTCOME_TEXT, OUTCOME_TITLES, PHASE_TITLES

from .text import answer_text

# What stands between the case and a better outcome, in precedence order (as on 4.1).
NEXT = (
    ("evidence_gaps", "Evidence gaps", "Keep the outcome at O4 until resolved."),
    ("open_remediations", "Open remediations", "Keep the outcome at O3 until resolved."),
    ("open_conditions", "Conditions", "Remain attached to an O2 outcome."),
    ("pending_reviews", "Legal reviews pending", "Do not change the outcome by themselves."),
    ("verification_requests", "To be verified", "Do not change the outcome."),
)
GOVERNANCE = (
    ("G01", "g01_decision"), ("G02", "g02_decision_maker"), ("G03", "g03_review_date"),
    ("G04", "g04_conditions"), ("G05", "g05_reasoning"),
)
SEP_ATTRS = {"SEP00": "decision", "SEP03": "vulnerability", "SEP09": "effect", "SEP10": "new_risk", "SEP11": "new_mitigation"}


def _cell(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\r", "").replace("\n", "<br>") or "—"


def _table(head: list[str], rows: list[list[object]]) -> list[str]:
    return [
        "| " + " | ".join(head) + " |",
        "|" + "|".join("---" for _ in head) + "|",
        *("| " + " | ".join(_cell(v) for v in row) + " |" for row in rows),
        "",
    ]


def _v(member) -> str:
    return label(member) if member is not None else "—"


def element_origin(ev: ElementEvaluation) -> str:
    """Who set a reviewer check: a person, the API, or the API then confirmed by a person."""
    if ev.source is ElementSource.API:
        return "API (not yet confirmed)"
    if (ev.provenance or "").startswith("openai:"):
        return "API, confirmed by a person"
    return "Person"


def build(cfg: ConfigBundle, state: AssessmentState, result: EngineResult) -> str:
    out: list[str] = []
    add = out.append

    add(f"# {APP_TITLE} — assessment report")
    add("")
    add(f"- Assessment: **{state.assessment_id}**")
    add(f"- Workbook: {result.workbook_version}")
    add(f"- Engine run: {result.run_id}, {result.timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
    add("")
    add(f"> {DISCLAIMER}")
    add("")

    add("## 1. Recommended outcome")
    add("")
    add(f"**{OUTCOME_TITLES[result.outcome]}** (rule {result.outcome_rule}, precedence O5 → O4 → O3 → O2 → O1)")
    add("")
    add(OUTCOME_TEXT[result.outcome])
    add("")
    add("This is the recommended outcome, not the final governance decision (section 9).")
    if not result.closed:
        add("")
        add("**Audit defects: this run is not a valid closure.** " + "; ".join(result.audit_defects))
    for w in result.warnings:
        add("")
        add(f"Warning: {w}")
    add("")

    add("## 2. What to do next")
    add("")
    if not any(getattr(result, attr) for attr, *_ in NEXT):
        add("Nothing open: no gap, remediation, condition, pending review or verification request.")
        add("")
    for attr, title, effect in NEXT:
        findings = getattr(result, attr)
        if not findings:
            continue
        add(f"### {title} ({len(findings)})")
        add("")
        add(f"_{effect}_")
        add("")
        for f in findings:
            add(f"- `{f.rule_id}` {f.message}" + (f" ({', '.join(f.ids)})" if f.ids else ""))
        add("")

    add("## 3. Routing")
    add("")
    add(f"- High-risk (FOLLOW): {result.high_risk or 'not answered'}")
    add(f"- Role (C05): {result.role or 'not answered'}")
    add(f"- Article 9 provider add-on: {'open' if result.provider_module else 'closed'}")
    add(f"- Article 27 deployer add-on: {'open' if result.deployer_module else 'closed'}")
    if result.routing_suspended:
        add("- Ordinary routing suspended (C03 = YES): HS07 verification")
    add("")

    add("## 4. Answers")
    add("")
    visible = set(result.visible_questions)
    for phase, title in PHASE_TITLES.items():
        qs = [q for q in cfg.questions.questions if q.phase is phase and q.id in visible]
        if not qs:
            continue
        add(f"### {title}")
        add("")
        rows = []
        for q in qs:
            a = state.answers.get(q.id)
            rows.append([q.id, q.text, answer_text(cfg, q, a), a.detail if a else None])
        out.extend(_table(["ID", "Question", "Answer", "Basis or evidence"], rows))

    add("## 5. Stakeholder engagement (SEP)")
    add("")
    sep_rows = []
    for f in cfg.sep.fields:
        value = getattr(state.sep, SEP_ATTRS[f.id]) if f.id in SEP_ATTRS else state.sep.texts.get(f.id)
        if value is None or value == "":
            continue
        sep_rows.append([f.id, f.field, _v(value) if hasattr(value, "value") else value])
    if state.sep.effect_risk_ids:
        sep_rows.append(["SEP09", "Risks affected", ", ".join(state.sep.effect_risk_ids)])
    out.extend(_table(["ID", "Field", "Value"], sep_rows) if sep_rows else ["Nothing recorded.", ""])

    add("## 6. Risk register")
    add("")
    if result.risks:
        rows = []
        for rid, r in result.risks.items():
            ra = state.risks.get(rid)
            rows.append([
                rid, cfg.risk(rid).right.split(";")[0],
                " / ".join(_v(getattr(ra, d, None)) for d in ("scale", "scope", "reversibility", "probability")),
                _v(r.severity), _v(r.initial), _v(r.residual) if r.residual else "— (not verified)",
                "Yes" if r.to_reassess else "—",
            ])
        out.extend(_table(["Risk", "Right", "Scale / scope / reversibility / probability", "Severity",
                           "Initial", "Residual", "Reassess (SEP)"], rows))
        add("Residual risk is recorded only after a linked mitigation is verified effective.")
        add("")
    else:
        add("No risk in the case register.")
        add("")

    add("## 7. Rules and reviewer checks")
    add("")
    add("### Proportionality")
    add("")
    if result.prop_statuses:
        out.extend(_table(["Rule", "Status", "Action"], [
            [r, label(s), ", ".join(label(e) for e in result.rules[r].effects)] for r, s in result.prop_statuses.items()
        ]))
        add("The engine never concludes 'proportionate' or 'disproportionate': normative balancing stays with legal review.")
        add("")
    else:
        add("No proportionality check applicable.")
        add("")
    add("### Reviewer checks")
    add("")
    checks = [ev for eid, ev in sorted(state.elements.items()) if cfg.rule(eid.split(".", 1)[0]).family != "HS"]
    if checks:
        out.extend(_table(["Check", "State", "Set by", "Reason", "Cited"], [
            [ev.element_id, ev.state.value.replace("_", " "), element_origin(ev), ev.rationale,
             ", ".join(r.removeprefix("answer:") for r in ev.evidence_refs)]
            for ev in checks
        ]))
    else:
        add("No reviewer check recorded.")
        add("")
    gates = [g for g in state.human_gates.values() if cfg.rule(g.rule_id).family != "HS"]
    if gates:
        add("### Legal reviews")
        add("")
        out.extend(_table(["Rule", "Gate", "Decision", "Reviewer"],
                          [[g.rule_id, g.gate.value, g.decision, g.decided_by] for g in gates]))
    scrutiny = sorted(r for r, rr in result.rules.items() if rr.fired and any(e.value == "SCRUTINY" for e in rr.effects))
    if scrutiny:
        add(f"Higher scrutiny raised by: {', '.join(scrutiny)}.")
        add("")

    add("## 8. Mitigation plan and hard stops")
    add("")
    add("### Mitigation plan")
    add("")
    activated = [m for m in state.mitigations.values() if m.activated]
    if activated:
        out.extend(_table(["Mitigation", "Risk", "Measure", "Status", "Decision effect", "Owner"], [
            [m.mitigation_id, cfg.mitigation(m.mitigation_id).risk_id, cfg.mitigation(m.mitigation_id).measure,
             label(m.status), cfg.mitigation(m.mitigation_id).decision_effect_text, m.owner or "TO ASSIGN"]
            for m in activated
        ]))
    else:
        add("No measure activated.")
        add("")
    add("### Hard stops")
    add("")
    opened = {h: v for h, v in result.hard_stops.items() if v.opened}
    if opened:
        out.extend(_table(["HS", "State", "Legal review", "Elements"], [
            [h, v.state.value.replace("_", " "), v.gate.value,
             ", ".join(f"{k.split('.')[1]}={s.value}" for k, s in v.elements.items())]
            for h, v in opened.items()
        ]))
    else:
        add("No hard stop opened. High risk alone never produces O5.")
        add("")

    add("## 9. Final governance decision")
    add("")
    fields = {g.id: g.field for g in cfg.questions.governance_fields}
    gov = [(gid, fields.get(gid, gid), getattr(state.governance, attr)) for gid, attr in GOVERNANCE]
    if any(v for *_, v in gov):
        out.extend(_table(["ID", "Field", "Value"], [[gid, field, v] for gid, field, v in gov]))
    else:
        add("Not recorded yet. It is filled by the responsible person or body, never by the engine.")
        add("")

    add("## 10. Audit trail")
    add("")
    add(f"{len(result.audit_trail)} events, run {result.run_id}, workbook {result.workbook_version}. "
        "The JSON report holds every field of every event.")
    add("")
    out.extend(_table(["Event", "Module", "Rule", "Output", "Inputs", "Evidence", "API", "Human gate", "Parent"], [
        [e.event_id, e.module.value, e.rule_id, e.engine_output, ", ".join(e.input_ids), ", ".join(e.evidence_refs),
         ", ".join(f"{k}={v['state']}" for k, v in e.api_evaluation.items()) if e.api_evaluation else None,
         " — ".join(x for x in ((e.human_gate.value if e.human_gate else ""), e.human_decision or "") if x) or None,
         e.parent_event_id]
        for e in result.audit_trail
    ]))

    add("---")
    add("")
    add(FOOTER)
    add("")
    return "\n".join(out)

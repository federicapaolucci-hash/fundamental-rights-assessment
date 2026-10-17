"""CSV tables (risk register, mitigation plan, audit trail), with a BOM so Excel reads the accents."""

from __future__ import annotations

import csv
import io
import json

from digcon.domain.enums import label
from digcon.domain.models import AssessmentState, ConfigBundle
from digcon.engine import EngineResult

BOM = "﻿"


def _csv(head: list[str], rows: list[list[object]]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(head)
    writer.writerows([["" if v is None else v for v in row] for row in rows])
    return BOM + buf.getvalue()


def risk_register(cfg: ConfigBundle, state: AssessmentState, result: EngineResult) -> str:
    def v(x):
        return label(x) if x is not None else ""

    rows = []
    for rid, r in result.risks.items():
        ra = state.risks.get(rid)
        rows.append([
            rid, cfg.risk(rid).right.split(";")[0],
            *(v(getattr(ra, d, None)) for d in ("scale", "scope", "reversibility", "probability")),
            v(r.severity), v(r.initial),
            *(v(getattr(ra, f"residual_{d}", None)) for d in ("scale", "scope", "reversibility", "probability")),
            v(r.residual), "YES" if r.to_reassess else "", "; ".join(ra.evidence_refs) if ra else "",
        ])
    return _csv(["risk_id", "right", "scale", "scope", "reversibility", "probability", "severity", "initial_risk",
                 "residual_scale", "residual_scope", "residual_reversibility", "residual_probability", "residual_risk",
                 "reassess_sep", "evidence_refs"], rows)


def mitigation_plan(cfg: ConfigBundle, state: AssessmentState) -> str:
    rows = []
    for m in state.mitigations.values():
        if not m.activated:
            continue
        spec = cfg.mitigation(m.mitigation_id)
        rows.append([
            m.mitigation_id, spec.risk_id, spec.measure, label(m.status), spec.timing_text,
            spec.decision_effect_text, m.owner or "TO ASSIGN", "; ".join(m.linked_rule_ids),
            "; ".join(m.evidence_refs), m.verification_ref, m.notes,
        ])
    return _csv(["mitigation_id", "risk_id", "measure", "status", "timing", "decision_effect", "owner",
                 "remediates_rules", "evidence_refs", "verification_ref", "notes"], rows)


def audit_trail(result: EngineResult) -> str:
    rows = [
        [e.event_id, e.assessment_id, e.run_id, e.workbook_version, e.timestamp.isoformat(), e.module.value,
         e.rule_id, "; ".join(e.input_ids), "; ".join(e.evidence_refs),
         json.dumps(e.api_evaluation, ensure_ascii=False) if e.api_evaluation else "",
         e.human_gate.value if e.human_gate else "", e.human_decision,
         "; ".join(e.linked_risk_ids), "; ".join(e.linked_mitigation_ids),
         e.hs_state.state.value if e.hs_state else "", e.engine_output, e.parent_event_id]
        for e in result.audit_trail
    ]
    return _csv(["event_id", "assessment_id", "run_id", "workbook_version", "timestamp", "module", "rule_id",
                 "input_ids", "evidence_refs", "api_evaluation", "human_gate", "human_decision", "linked_risk_ids",
                 "linked_mitigation_ids", "hs_state", "engine_output", "parent_event_id"], rows)

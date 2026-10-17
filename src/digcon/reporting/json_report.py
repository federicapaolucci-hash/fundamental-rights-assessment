"""JSON report: the assessment as entered, the full engine result and the audit trail with every field."""

from __future__ import annotations

import json
from typing import Any

from digcon.domain.models import AssessmentState
from digcon.engine import EngineResult

FORMAT = "digcon-report/1"


def build(state: AssessmentState, result: EngineResult) -> dict[str, Any]:
    return {
        "format": FORMAT,
        "assessment_id": state.assessment_id,
        "workbook_version": result.workbook_version,
        "run_id": result.run_id,
        "generated_at": result.timestamp.isoformat(),
        "recommended_outcome": result.outcome.value,
        "outcome_rule": result.outcome_rule,
        "audit_closed": result.closed,
        "assessment": state.model_dump(mode="json"),
        "result": result.model_dump(mode="json"),
    }


def dumps(state: AssessmentState, result: EngineResult) -> str:
    return json.dumps(build(state, result), ensure_ascii=False, indent=2)


def assessment_of(data: dict[str, Any]) -> dict[str, Any]:
    """The assessment inside a JSON report, so a report can also be loaded to resume; other data is returned as is."""
    if isinstance(data, dict) and data.get("format") == FORMAT and isinstance(data.get("assessment"), dict):
        return data["assessment"]
    return data

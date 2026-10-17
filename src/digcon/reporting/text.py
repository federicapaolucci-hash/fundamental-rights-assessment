"""Readable names for answers, shared by the interface and the reports."""

from __future__ import annotations

from digcon.domain.enums import AnswerKind, AnswerState, ControlEffectiveness, NotificationStatus, RiskLevel, Role, label
from digcon.domain.models import Answer, ConfigBundle, QuestionSpec


def option_names(cfg: ConfigBundle, q: QuestionSpec) -> dict[str, str]:
    """Code -> label for every value a question accepts (answer states included)."""
    names = {s.value: label(s) for s in q.states}
    if q.kind is AnswerKind.ROLE:
        names |= {r.value: label(r) for r in Role if r is not Role.UNKNOWN}
    elif q.kind is AnswerKind.RISK_RATING:
        names |= {r.value: label(r) for r in RiskLevel}
    elif q.kind is AnswerKind.NOTIFICATION:
        names |= {n.value: label(n) for n in NotificationStatus}
    elif q.kind is AnswerKind.EFFECTIVENESS:
        names |= {e.value: label(e) for e in ControlEffectiveness}
    elif q.kind in (AnswerKind.SINGLE, AnswerKind.MULTI) and q.option_set:
        names |= {o.code: o.label for os_ in cfg.questions.option_sets if os_.id == q.option_set for o in os_.options}
    elif q.kind is AnswerKind.RISK_ROWS:
        names |= {r.id: f"{r.id} — {r.label or r.right.split(';')[0][:60]}" for r in cfg.risks.risks}
    return names


def answer_text(cfg: ConfigBundle, q: QuestionSpec, answer: Answer | None) -> str:
    """The answer as a person reads it; an unanswered question is 'Not answered' (never NO)."""
    if answer is None:
        return "Not answered"
    if answer.state is not None and not answer.value:
        return label(AnswerState(answer.state))
    names = option_names(cfg, q)
    if isinstance(answer.value, list):
        return "; ".join(names.get(v, v) for v in answer.value)
    return names.get(answer.value, answer.value or "")

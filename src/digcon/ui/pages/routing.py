"""Section 2.0: applicable requirements, i.e. the routing after scoping (00_MAPPA_FLUSSO §2)."""

from __future__ import annotations

import streamlit as st

from digcon.domain.models import ConfigBundle
from digcon.engine import EngineResult

from .questionnaire import routing_box

# 00_MAPPA_FLUSSO, "Routing dopo lo scoping".
ROUTES = [
    ("High-risk = NO", "These modules remain closed on the recorded classification; continue the wider assessment and check other applicable obligations"),
    ("High-risk = YES + Provider", "Step 1 + provider obligations (Article 9)"),
    ("High-risk = YES + Deployer + Article 27 applicable", "Step 1 + deployer FRIA (Article 27)"),
    ("High-risk = YES + Joint", "Step 1 + provider risk management (Article 9); deployer FRIA only if Article 27 applies"),
]


def _active_route(result: EngineResult) -> int | None:
    if result.high_risk == "NO":
        return 0
    if result.high_risk != "YES" or result.routing_suspended:
        return None
    return {"PROVIDER": 1, "DEPLOYER": 2, "JOINT": 3}.get(result.role or "")


def render(cfg: ConfigBundle, result: EngineResult) -> None:
    st.markdown(
        "Step 1 is always completed. The step 2 requirements apply **only once the scope is set**, from the "
        "recorded high-risk classification and the organisation’s role. Where both provider and deployer responsibilities "
        "are recorded, check each obligation separately: Article 27 does not apply automatically. "
        "The highlighted route reflects recorded answers, not an independent legal determination."
    )
    routing_box(result)
    active = _active_route(result)
    with st.container(border=True):
        st.subheader("The four possible cases")
        for i, (cond, path) in enumerate(ROUTES):
            if i == active:
                with st.container(key="route_active"):
                    st.markdown(f":blue-badge[:material/arrow_forward: Your case] **{cond}**")
                    st.markdown(path)
            else:
                st.markdown(f":gray[{cond} → {path}]")
    if result.routing_suspended:
        st.caption("No case applies while the step 2 requirements are on hold (C03 = YES).")
    elif active is None:
        st.caption("Not set yet: answer HIGH RISK (1.2) and the role C05 (1.1). UNKNOWN opens nothing and is an evidence gap.")

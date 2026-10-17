"""Interface texts that the workbook does not provide. Enum labels come from digcon.domain.enums.label."""

from __future__ import annotations

from digcon.domain.enums import Outcome, Phase

APP_TITLE = "Fundamental Rights Assessment"
APP_CAPTION = "Assessing fundamental rights risks, safeguards and governance decisions."
FOOTER = "DIGCON — FIS-funded project, Baffi Centre, Bocconi University · All rights reserved"
CREDITS = "Developed by Federica Paolucci, Eleonora Silva and Matteo Colombo."
BYLINE = "By Federica Paolucci, Eleonora Silva and Matteo Colombo · DIGCON, Baffi Centre, Bocconi University"
DISCLAIMER = (
    "**Research prototype** for research and evaluation purposes only. This tool does not certify legal compliance "
    "or replace legally required assessments or human decision-making. Do not enter personal data, confidential "
    "DPIAs, trade secrets or sensitive organisational information."
)

METHODOLOGY = """
This **research prototype** supports a structured assessment of **fundamental rights risks**, of the **safeguards**
that address them and of the **decision-making processes** around an AI system. It is developed by DIGCON
(Baffi Centre, Bocconi University).

The **DPIA** is the methodological reference for the assessment framework; **AI Act obligations** are covered
through the modules that apply to the case.

The assessment runs in four steps:

1. **Assessment framework**, common to providers and deployers: the scope, then WHAT → HOW → WHY;
2. **Regulatory requirements** that apply to the case;
3. **Rights assessment**: stakeholder involvement, fundamental rights risks, legal and procedural review,
   safeguards and mitigation, legal constraints and stop conditions;
4. **Findings and decision**: the recommended outcome (O1–O5), then the organisation's governance decision.

**Article 9 and Article 27 AI Act remain distinct obligations** and apply only once the scope is set:

- **provider obligations (Article 9)** apply when the system is high-risk and the role is Provider or Joint;
- the **deployer FRIA (Article 27)** applies when the system is high-risk, the role is Deployer or Joint and Article 27 applies.

Answers feed a deterministic decision logic (DIGCON T17). **Unknown, not applicable and not owned are never treated as "No"**:
they produce an evidence gap or a verification request. Risks are rated from scale, scope, reversibility and probability;
residual risk is recorded only after a safeguard has been verified effective.

**The tool does not decide whether a measure is proportionate.** Proportionality checks return a structured status;
normative balancing is referred to human legal review. **O5 (cannot proceed)** requires every element of a stop
condition (HS01–HS09) to be established and confirmed by a legal reviewer — high risk alone never produces O5.

The recommended outcome (O1–O5) is a recommendation of the tool, **not the final governance decision**, which the
organisation records separately.
"""

# The four steps of 00_MAPPA_FLUSSO: common core, add-ons opened after scoping, transversal modules, convergence.
STEP_CORE = "Step 1 — Assessment framework"
STEP_ADDONS = "Step 2 — Regulatory requirements"
STEP_ANALYSIS = "Step 3 — Rights assessment"
STEP_OUTCOME = "Step 4 — Findings and decision"
STEP_TEXT = {
    STEP_CORE: "Common to providers and deployers: the assessment scope, then WHAT → HOW → WHY. "
               "No later step replaces these questions.",
    STEP_ADDONS: "The AI Act requirements that apply once the scope is set: Article 9 for providers, Article 27 (FRIA) "
                 "for deployers, both for joint roles. If the system is not high-risk they do not apply and the "
                 "assessment continues on step 1.",
    STEP_ANALYSIS: "Built on steps 1 and 2: stakeholder involvement, fundamental rights risks, legal and procedural "
                   "review, safeguards and mitigation, legal constraints and stop conditions.",
    STEP_OUTCOME: "The recommended outcome (O1–O5) follows from everything above. It is a recommendation of the tool: "
                  "the final decision belongs to the organisation and is recorded in 4.2.",
}

PHASE_TITLES = {
    Phase.INTRO: "1.1 Assessment scope",
    Phase.WHAT: "1.2 WHAT — System and context",
    Phase.HOW: "1.3 HOW — Governance and oversight",
    Phase.WHY: "1.4 WHY — Legal justification",
    Phase.PROVIDER: "2.1 Provider obligations — Article 9 AI Act",
    Phase.DEPLOYER: "2.2 Deployer FRIA — Article 27 AI Act",
}

SUBSECTIONS = {"Scoping e ruoli": "Scope and roles"}

OUTCOME_TITLES = {
    Outcome.O1: "O1 — Proceed",
    Outcome.O2: "O2 — Proceed subject to conditions",
    Outcome.O3: "O3 — Revision required",
    Outcome.O4: "O4 — Assessment incomplete — evidence gaps",
    Outcome.O5: "O5 — Cannot proceed under current conditions",
}
OUTCOME_TEXT = {
    Outcome.O1: "No stop condition, material evidence gap, open remediation or restrictive condition. Ordinary monitoring and review may remain.",
    Outcome.O2: "Only explicit pilot, deployment or continuous conditions remain. Proceed subject to those conditions.",
    Outcome.O3: "At least one required remediation is still open, failed or not verified. Revise before proceeding.",
    Outcome.O4: "Material information needed for a required conclusion is missing or unknown. Complete the assessment.",
    Outcome.O5: "At least one stop condition (HS01–HS09) is fully established and confirmed by legal review. A mitigation plan cannot override it.",
}
RECOMMENDATION_NOTE = (
    "This is the tool's recommendation, not a decision: the final decision belongs to the organisation "
    "and is recorded in 4.2 Governance decision."
)


START_TITLE = "1.0 Assessment workspace"
ROUTING_TITLE = "2.0 Applicable assessment requirements"
SEP_TITLE = "3.1 Stakeholder involvement"
RISKS_TITLE = "3.2 Fundamental rights risks"
RULES_TITLE = "3.3 Legal and procedural review"
MITIGATION_TITLE = "3.4 Safeguards and mitigation"
REVIEW_TITLE = "3.5 Legal constraints and stop conditions"
RESULT_TITLE = "4.1 Assessment findings"
GOVERNANCE_TITLE = "4.2 Governance decision"

# Notes shown under specific questions. Interface guidance only: they change no logic.
QUESTION_NOTES = {
    "C05": "Once the system is high-risk (HIGH RISK = YES, section 1.2), this role sets the step 2 requirements: "
           "Provider → Article 9 (2.1); Deployer → Article 27 (2.2, after D00 = YES); Joint → both.",
    "C06": "For the record only: it does not change which requirements apply. The role that counts is C05.",
    "FOLLOW": "YES opens the step 2 requirements for the role chosen in C05 (section 1.1).",
    "D00": "YES opens the Article 27 questions D01–D10.",
    "C43": "Effectiveness evidence only: VERIFIED EFFECTIVE does not lower any risk by itself. Residual risk is recalculated "
           "in Fundamental rights risks (3.2), after a linked mitigation is verified.",
    "C48": "Effectiveness evidence only: VERIFIED EFFECTIVE does not lower any risk by itself. Residual risk is recalculated "
           "in Fundamental rights risks (3.2), after a linked mitigation is verified.",
    "C34": "Imported from a prior DPIA or impact assessment: it does not override the DIGCON risk rating. N/A if none applies.",
    "C35": "Imported evidence, not the DIGCON residual-risk calculation. N/A if no prior assessment applies.",
    "D04": "Select concrete risks from the DIGCON catalogue (RSEL-01). Rate them in Fundamental rights risks (3.2).",
}


def subsection(name: str) -> str:
    return SUBSECTIONS.get(name, name)


# English versions of the hard-stop elements (05_RULES has them in Italian only), AS-037: provisional,
# display only. The engine, the audit trail and config/ keep the workbook text.
HS_ELEMENTS = {
    "HS01": ("Purpose manifestly unlawful", "Reasoned legal determination",
             "Purpose cannot be redefined in a lawful form"),
    "HS02": ("C14 = No", "No valid alternative legal basis (alternatives documented)", "No lawful redesign possible"),
    "HS03": ("Reuse of data", "Incompatibility established",
             "Cannot be reconfigured (purpose restriction / new collection)"),
    "HS04": ("N02 = No", "Grave risk to rights", "Use cannot be reconfigured"),
    "HS05": ("Human oversight essential", "Structurally impossible", "Not remediable"),
    "HS06": ("Contestability essential", "Structurally impossible", "Not remediable"),
    "HS07": ("Use expressly prohibited by applicable law (closed list)",),
    "HS08": ("Grave harm to rights established", "Mitigations assessed and insufficient",
             "Risk cannot be reduced to an acceptable level"),
    "HS09": ("Vulnerable group identified", "Grave harm specific to the group", "Not mitigable"),
}

# Workbook texts shown in the interface: English for the ones the workbook has in Italian (AS-037), reworded
# where they carry internal jargon. Meaning unchanged.
WORKBOOK_TEXT = {
    **{(f"{hs}.E{i}", "text"): t for hs, els in HS_ELEMENTS.items() for i, t in enumerate(els, 1)},
    **{(hs, "trigger_text"): " AND ".join(els) for hs, els in HS_ELEMENTS.items()},
    ("EG-01", "trigger_text"): "Necessary information missing or not sufficiently determined",
    ("FLOW-03", "trigger_text"): "High-risk = Yes AND role = Provider/Joint",
    ("CROSS-02", "trigger_text"): "Use case not consistent with the intended purpose",
    ("QUAL-01", "trigger_text"): "Reasoning field not empty but substantially insufficient",
    ("G01", "purpose"): "Final decision, distinct from the recommended outcome",
    ("G02", "purpose"): "Identifies the responsible person or body",
    ("G03", "purpose"): "Sets the review date",
    ("G04", "purpose"): "Records conditions and limitations",
    ("G05", "purpose"): "Records the reasoning of the decision",
    ("SEP00", "activation"): "Assess after affected persons/groups and material harm context are identified; "
                             "C55 is evidence, not a precondition.",
    ("RSEL-01", "trigger_text"): "A question, rule or evidence identifies a harm, affected right/area or material "
                                 "contextual risk that must be represented in the fundamental rights risks (3.2).",
}


def workbook_text(item_id: str, field: str, text: str) -> str:
    return WORKBOOK_TEXT.get((item_id, field), text)


# Names of the sections in the left menu.
NAV_LABELS = {
    START_TITLE: "1.0  Assessment workspace",
    PHASE_TITLES[Phase.INTRO]: "1.1  Assessment scope",
    PHASE_TITLES[Phase.WHAT]: "1.2  WHAT — System and context",
    PHASE_TITLES[Phase.HOW]: "1.3  HOW — Governance and oversight",
    PHASE_TITLES[Phase.WHY]: "1.4  WHY — Legal justification",
    ROUTING_TITLE: "2.0  Applicable requirements",
    PHASE_TITLES[Phase.PROVIDER]: "2.1  Provider obligations · Art. 9",
    PHASE_TITLES[Phase.DEPLOYER]: "2.2  Deployer FRIA · Art. 27",
    SEP_TITLE: "3.1  Stakeholder involvement",
    RISKS_TITLE: "3.2  Fundamental rights risks",
    RULES_TITLE: "3.3  Legal and procedural review",
    MITIGATION_TITLE: "3.4  Safeguards and mitigation",
    REVIEW_TITLE: "3.5  Legal constraints and stop conditions",
    RESULT_TITLE: "4.1  Assessment findings",
    GOVERNANCE_TITLE: "4.2  Governance decision",
}

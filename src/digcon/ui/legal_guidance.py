"""Explanatory guidance only; no applicability or decision rules are defined here.

Sources checked 2026-10-21: European Commission AI Act Service Desk,
Articles 9 and 27 (displayed consolidated text dated 2026-07-27).
Examples describe useful evidence, not additional statutory formalities.
"""
ARTICLE_9 = 'https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-9'
ARTICLE_27 = 'https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-27'

# question -> precise provision, practical completion prompt
QUESTION_GUIDANCE = {
    'P01': ('9(1)–(2)', 'Identify the process owner, review cycle and events that trigger an update. Example: risk procedure and dated review record.'),
    'P02': ('9(2)(a)', 'Describe any identified health or safety harm and who may experience it. A negative answer should reflect an actual review, not missing analysis.'),
    'P03': ('9(2)(a)', 'Connect a concrete effect on people to the right at risk. Example: unequal access to a service, identifying the affected group and evidence.'),
    'P04': ('9(2)(a)–(b)', 'Explain the risk scenario within the intended use, including how an output can affect a person.'),
    'P05': ('9(2)(b)', 'Identify plausible misuse given the actual users and setting. Example: staff using a recommendation as an automatic decision.'),
    'P06': ('9(2)(b)', 'Explain how the foreseeable misuse scenarios were evaluated. Identifying a scenario and evaluating its risk are separate steps.'),
    'P07': ('9(2)(c)', 'Reference monitoring findings and explain which risk review they triggered. Link the finding to the resulting action.'),
    'P08': ('9(2)(d), 9(3)–(5)', 'For each risk, identify the targeted measure, responsible actor and implementation evidence. Explain relevant interactions with other safeguards.'),
    'P09': ('9(5)', 'Explain the judgement on each relevant residual risk and on the overall residual risk. A low rating alone does not explain acceptability.'),
    'P10': ('9(6)–(8)', 'Reference the test method, predefined metrics and thresholds, date and results. Explain what happened when a threshold was not met.'),
    'D00': ('27(1)', 'Explain the applicable route: an Article 6(2) high-risk use outside Annex III point 2 by a public-law body or private public-service entity; or a high-risk use under Annex III point 5(b) or 5(c). Record the relevant category and role. High-risk status alone is insufficient.'),
    'D01': ('27(1)(a)', 'Describe where the system enters the workflow, who uses its output and how that output affects the decision. Compare the actual process with the intended purpose.'),
    'D02': ('27(1)(b)', 'State the planned period and frequency. Example: a six-month pilot, used on each application, with weekly review.'),
    'D03': ('27(1)(c)', 'Identify the people affected in this particular setting, including groups exposed indirectly. Explain relevant vulnerabilities.'),
    'D04': ('27(1)(d)', 'Describe the harm scenario for each affected group and identify the provider information considered under Article 13. Explain any information still missing.'),
    'D05': ('27(1)(e)', 'Explain who reviews the output, what they can see, when they can intervene and whether they can change the outcome. Relate this to the instructions for use.'),
    'D06': ('27(1)(f)', 'Describe the response if harm occurs: responsible team, escalation, corrective action and usable complaint route. Naming an incident is not a response plan.'),
    'D07': ('27(2)', 'Identify the previous assessment and explain why the cases are similar. State which conclusions can be reused and which need fresh examination.'),
    'D08': ('27(2)', 'Identify any changed use, affected group, risk, oversight or response measure, and the corresponding update. Reference the version and review date.'),
    'D09': ('27(4)', 'Map each relevant FRIA element to a specific DPIA section or incorporate the relevant content. A document title alone does not establish coverage; complete any remaining elements.'),
    'D10': ('27(3), 27(5)', 'Record the notification reference and date, or the grounds for an applicable exemption under Article 46(1). Exporting a DIGCON report does not itself notify an authority.'),
}

PROVIDER_INTRO = '''**Purpose of this module — Risk management system, Article 9 AI Act.**
Describe how the provider identifies, evaluates and addresses risks throughout the system’s lifecycle.
Use the prompts below to connect the process to actual decisions and evidence.

“Systemic risk management” is the DIGCON module label. The statutory title is **Risk management system**;
this module does not assess the separate GPAI systemic-risk regime.
'''

PROVIDER_DETAIL = '''Article 9(3) limits the risks covered here to those reasonably addressed through design,
development or technical information. The wider DIGCON assessment also examines organisational and legal responses.
Under Article 9(5), consider design changes, controls for remaining risks, and information or training for deployers.
Article 9(9) calls for attention to impacts on under-18s and, where appropriate, other vulnerable groups.
Article 9(10) permits integration with other Union-law risk management processes.

These prompts support documentation; completing the ten questions does not establish full compliance with Article 9.
'''

DEPLOYER_INTRO = '''**Purpose of this module — Fundamental rights impact assessment, Article 27 AI Act.**
Assess the effects of the deployer’s concrete use on people. First explain why Article 27 applies;
then describe the use, affected people, harms, human oversight and response arrangements.

Having both provider and deployer responsibilities does not automatically establish Article 27 applicability.
The tool opens this module from your recorded classification and applicability answers; these require human justification.
'''

DEPLOYER_DETAIL = '''Article 27(1) requires the assessment before deployment for the uses and deployers within its scope.
Paragraph 2 addresses first use, reliance on earlier assessments in similar cases, and updates.
Paragraph 3 concerns notification of results; paragraph 4 addresses information already covered by a DPIA.
Paragraph 5 provides for an AI Office questionnaire/template. DIGCON is a research tool, not that official template.

Applicability, the relevant date of application and any transitional provision require a case-specific legal check.
An unopened module does not mean that no other AI Act or data protection obligations apply.
'''

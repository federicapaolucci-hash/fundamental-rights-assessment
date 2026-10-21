"""Readable scope guidance; does not classify a system or change stored answers."""
import streamlit as st

ARTICLE_6 = 'https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6'
ARTICLE_27 = 'https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-27'
ANNEXES = 'https://eur-lex.europa.eu/eli/reg/2024/1689/eng'

QUESTION_TITLES = {
    'FOLLOW': 'Is this AI system classified as high-risk under the AI Act?',
    'D00': 'Does your organisation need to carry out a FRIA under Article 27?',
}


def render_scope_guide(question_id):
    if question_id == 'FOLLOW':
        st.caption('This is a legal classification of the system and its intended use, not the risk score calculated later in this assessment.')
        left, right = st.columns(2)
        with left:
            with st.container(border=True):
                st.markdown('**🛡️ Route 1 — Regulated products**')
                st.markdown('Both conditions must be met:\n\n'
                            '1. The AI is a safety component of a product, or is itself a product, covered by legislation listed in Annex I.\n'
                            '2. That product requires a third-party conformity assessment under that legislation.')
                st.caption('Examples may include medical devices or machinery. Being used in one of these sectors is not enough.')
                st.markdown(f'[Article 6(1)]({ARTICLE_6})')
        with right:
            with st.container(border=True):
                st.markdown('**⚖️ Route 2 — Uses listed in Annex III**')
                st.markdown('The intended use matches a specific Annex III category. Examples include certain uses in recruitment, education, creditworthiness assessment, law enforcement and migration.')
                st.caption('Check the exact listed use and its exclusions. A sector name alone does not establish high-risk status. The Article 6(3) exception also needs examination.')
                st.markdown(f'[Article 6(2)–(4)]({ARTICLE_6}) · [Check Annex III]({ANNEXES})')
        with st.expander('Exceptions and qualifications to check before answering'):
            st.markdown('**For Route 1:** Article 6(1a)–(1c) qualifies the safety-component and third-party assessment criteria. '
                        'Non-safety assistance or optimisation alone does not qualify; a failure that endangers health or safety does. '
                        'Third-party assessment required solely for non-health-and-safety risks does not satisfy the second condition.')
            st.markdown('**For Route 2:** Article 6(3) allows an exception where there is no significant risk of harm '
                        'and one of its specified conditions applies: a narrow procedural task; improving a completed human activity; '
                        'detecting decision patterns or deviations without replacing or influencing a completed human assessment without proper review; '
                        'or a preparatory task. Human involvement alone is not an exemption.')
            st.markdown('An Annex III system that profiles natural persons remains high-risk. '
                        'A provider relying on the exception must document the assessment and comply with the registration requirement in Article 6(4).')
        st.markdown('**Choose Yes** if either route establishes high-risk status. **Choose No** if the legal assessment excludes it. '
                    '**Choose Unknown** if the intended use, relevant category or supporting assessment is still unclear.')
        st.caption('Classification and the date on which obligations apply are separate questions. High-risk status does not automatically make Article 27 applicable.')
    elif question_id == 'D00':
        st.caption('Deployer means the organisation using the system under its authority. Check whether either case below describes your organisation and use.')
        left, right = st.columns(2)
        with left:
            with st.container(border=True):
                st.markdown('**🏛️ Case A — Public bodies and public-service providers**')
                st.markdown('All three conditions must be met:\n\n'
                            '1. Your organisation is a body governed by public law or a private entity providing public services.\n'
                            '2. It deploys a high-risk system under Article 6(2), linked to Annex III.\n'
                            '3. The use is outside Annex III point 2, concerning critical infrastructure.')
                st.caption('Check the organisation’s legal status or public-service activity. A public-sector customer alone does not settle this question.')
        with right:
            with st.container(border=True):
                st.markdown('**🏦 Case B — Creditworthiness and life/health insurance**')
                st.markdown('Your organisation deploys a high-risk system for either of these listed uses:\n\n'
                            '- Evaluating the creditworthiness of natural persons or establishing their credit score — Annex III 5(b), excluding financial-fraud detection.\n'
                            '- Risk assessment and pricing for natural persons in life or health insurance — Annex III 5(c).')
                st.caption('This case also covers private deployers that are not public-service providers. It does not cover every banking or insurance AI use.')
        st.markdown('**Choose Yes** if Case A or Case B applies. **Choose No** if neither applies. '
                    '**Choose Unknown** if the legal status, use category or high-risk classification remains unresolved.')
        st.caption('Example: a private bank using a high-risk system to assess an individual’s creditworthiness falls within Case B. '
                   'A generic banking chatbot does not fall within Case B merely because a bank uses it.')
        st.markdown(f'[Legal basis: Article 27(1)]({ARTICLE_27}) · [Check Annex III, points 2 and 5(b)–(c)]({ANNEXES})')
        st.caption('A system classified only through the regulated-product route in Article 6(1) does not trigger Article 27(1) on that ground alone. '
                   'Other legal obligations may still apply. Explain your conclusion and its supporting reference below where available.')

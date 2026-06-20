import streamlit as st
from google import genai
import json
import re
import os

st.set_page_config(
    page_title="The PM Employee",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

SAMPLE_GOAL = (
    "Reduce post-purchase anxiety and improve delivery transparency "
    "for DTC brands shipping 1,000+ orders per day."
)

SAMPLE_FEEDBACK = """Customer interview — Sarah, VP Operations at a DTC apparel brand (500K orders/year):
"Our #1 support ticket is 'where's my order?' — easily 40% of our volume. Customers email us after getting the shipping confirmation because the tracking page is useless. It just says 'in transit' for 4 days and then the package shows up."

Support ticket — anonymous customer:
"I ordered 6 days ago. Tracking hasn't updated in 3 days. This is my first order and I'm already regretting it. Please respond ASAP."

Customer interview — Marcus, founder of a supplements brand ($8M ARR):
"We switched carriers last quarter and our WISMO rate went up 60%. The carrier tracking is just worse. But we can't switch back — the rates are better. We need something that normalises the experience regardless of which carrier we're on."

NPS survey comment (score 7 out of 10):
"Product is amazing, 10/10. But the delivery experience was stressful. No communication after the shipping confirmation. That's why you're getting a 7 and not a 10."

Customer interview — Janet, eCommerce Director at a home goods brand:
"We've looked at tracking tools but they're all expensive and require us to host a branded page. We just need proactive notifications — text or email — that tell the customer what's happening before they have to ask us."

Support ticket volume data (last 30 days):
- WISMO (Where Is My Order): 847 tickets — 43% of total support volume
- Average first response time: 6.2 hours
- Average resolution time: 18.4 hours
- CSAT for WISMO tickets: 3.1 out of 5"""


if st.session_state.get("load_demo"):
    st.session_state["goal_input"] = SAMPLE_GOAL
    st.session_state["fb_input"] = SAMPLE_FEEDBACK
    del st.session_state["load_demo"]


def get_api_key():
    try:
        return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        return os.environ.get("GOOGLE_API_KEY")


def extract_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    raise ValueError("Could not parse structured output. Please try again.")


def run_pm_employee(goal, feedback):
    api_key = get_api_key()
    if not api_key:
        st.error("No API key found. Add GOOGLE_API_KEY to .streamlit/secrets.toml")
        st.stop()

    client = genai.Client(api_key=api_key)

    prompt = f"""You are an exceptional AI Product Manager employee. Analyse the customer feedback below against the stated product goal and produce high-quality, immediately usable PM artifacts.

PRODUCT GOAL:
{goal}

CUSTOMER FEEDBACK:
{feedback}

Return ONLY a valid JSON object. No markdown fences, no preamble, no explanation. Exact structure:

{{
  "summary": "2-sentence executive summary: the core customer problem and the opportunity it represents.",
  "insights": [
    {{
      "theme": "Short descriptive theme name",
      "finding": "Specific, grounded finding from the feedback",
      "evidence": "Direct quote or close paraphrase from the feedback",
      "frequency": "high | medium | low"
    }}
  ],
  "user_stories": [
    {{
      "title": "Concise story title",
      "story": "As a [specific user type], I want [specific capability], so that [specific measurable outcome].",
      "acceptance_criteria": [
        "Given [context], when [action], then [outcome]",
        "Given [context], when [action], then [outcome]",
        "Given [context], when [action], then [outcome]"
      ],
      "impact": "high | medium | low",
      "effort": "high | medium | low",
      "rationale": "One sentence on why this story sits at this priority."
    }}
  ],
  "stakeholder_email": {{
    "subject": "Clear, specific subject line",
    "body": "Professional email, 3 paragraphs. P1: what we learned from customers. P2: what we are planning as a result. P3: what we need from stakeholders and next steps."
  }},
  "risks": [
    {{
      "title": "Risk name",
      "description": "What could go wrong and why it matters",
      "mitigation": "Specific, actionable mitigation strategy",
      "severity": "high | medium | low"
    }}
  ]
}}

Rules:
- 3 to 5 insights, each with a direct quote from the feedback as evidence
- 3 to 5 user stories ordered by impact descending
- Exactly 3 risks
- Acceptance criteria must be testable
- No generic statements — every word must be grounded in the actual feedback provided"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    return extract_json(response.text)


st.markdown("## ⚡ The PM Employee")
st.caption("Paste a product goal and raw customer feedback. Get a sprint's worth of PM work in 30 seconds.")
st.divider()

left, right = st.columns([2, 3], gap="large")

with left:
    st.markdown("**Product goal**")
    goal = st.text_area("goal_input", label_visibility="collapsed",
                        placeholder="What outcome are you trying to drive, and for which users?",
                        height=90, key="goal_input")

    st.markdown("**Customer feedback**")
    feedback = st.text_area("fb_input", label_visibility="collapsed",
                            placeholder="Paste interviews, support tickets, NPS comments, reviews — anything raw.",
                            height=280, key="fb_input")

    c1, c2 = st.columns(2)
    with c1:
        run = st.button("⚡ Run PM Employee", type="primary", use_container_width=True)
    with c2:
        if st.button("Load demo data", use_container_width=True):
            st.session_state["load_demo"] = True
            st.rerun()

with right:
    if run:
        current_goal = st.session_state.get("goal_input", "").strip()
        current_fb = st.session_state.get("fb_input", "").strip()

        if not current_goal or not current_fb:
            st.warning("Add a product goal and some customer feedback first.")
        else:
            with st.spinner("Your PM Employee is working..."):
                try:
                    results = run_pm_employee(current_goal, current_fb)

                    if results.get("summary"):
                        st.info(f"**TL;DR** — {results['summary']}")

                    t1, t2, t3, t4 = st.tabs(["💡 Insights", "📋 User Stories", "✉️ Stakeholder Email", "⚠️ Risks"])

                    with t1:
                        for ins in results.get("insights", []):
                            icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(ins.get("frequency", "medium"), "🟡")
                            st.markdown(f"**{icon} {ins.get('theme', '')}**")
                            st.write(ins.get("finding", ""))
                            if ins.get("evidence"):
                                st.caption(f"*\"{ins['evidence']}\"*")
                            st.divider()

                    with t2:
                        for i, story in enumerate(results.get("user_stories", []), 1):
                            impact = story.get("impact", "medium")
                            effort = story.get("effort", "medium")
                            i_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(impact, "🟡")
                            e_label = {"high": "heavy", "medium": "medium", "low": "light"}.get(effort, "medium")
                            with st.expander(f"#{i} · {i_icon} {story.get('title', '')} · effort {e_label}"):
                                st.markdown(f"*{story.get('story', '')}*")
                                if story.get("rationale"):
                                    st.caption(story["rationale"])
                                st.markdown("**Acceptance criteria**")
                                for ac in story.get("acceptance_criteria", []):
                                    st.markdown(f"- {ac}")

                    with t3:
                        em = results.get("stakeholder_email", {})
                        st.markdown(f"**Subject:** {em.get('subject', '')}")
                        st.divider()
                        st.text_area("Copy email body", value=em.get("body", ""), height=280, label_visibility="visible")

                    with t4:
                        for risk in results.get("risks", []):
                            sev = risk.get("severity", "medium")
                            content = f"**{risk.get('title', '')}**\n\n{risk.get('description', '')}\n\n💡 **Mitigation:** {risk.get('mitigation', '')}"
                            if sev == "high":
                                st.error(content)
                            elif sev == "medium":
                                st.warning(content)
                            else:
                                st.info(content)

                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
    else:
        st.markdown("""
#### What gets eliminated

A PM today spends 3+ hours per sprint on cognitive overhead:
reading interviews → extracting themes → writing user stories
→ drafting the stakeholder update → flagging risks.

**The PM Employee does all of it in 30 seconds.**

---

**Output on every run:**
- Key insights anchored to evidence from the actual feedback
- User stories specific enough to hand directly to an engineer
- A stakeholder email ready to send
- The top 3 risks with concrete mitigations

---

Click **Load demo data** to see it working immediately.
        """)
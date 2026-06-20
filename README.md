# ⚡ The PM Employee

> Turn raw customer feedback into a sprint's worth of PM work — in 30 seconds.

## The Problem

A PM today spends 3+ hours per sprint on cognitive overhead:

- Reading 20 customer interviews
- Extracting themes and patterns
- Writing user stories with acceptance criteria
- Drafting the stakeholder update email
- Flagging risks for engineering

This is the anguish era: busy work that occupies the calendar but does not require a human brain.

## The Solution

The PM Employee is an AI-powered tool that takes a product goal and raw customer feedback — interviews, support tickets, NPS comments, reviews — and instantly outputs:

| Output | What it is |
|---|---|
| **Insights** | Key themes with evidence quotes from the actual feedback |
| **User Stories** | Written to hand directly to an engineer, with acceptance criteria |
| **Stakeholder Email** | Drafted, subject line included, ready to send |
| **Risks** | Top 3 with specific mitigations, severity ranked |

Not a chatbot you have to guide. A colleague you hand work to.

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/pm-employee
cd pm-employee
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**

Create `.streamlit/secrets.toml` (already templated in this repo):
```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

**4. Run**
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`. Click **Load demo data** to see it working immediately.

---

## Deploying for a shareable link

Push to GitHub, then go to [share.streamlit.io](https://share.streamlit.io) and connect the repo. Add your API key as a secret in their dashboard. You get a public URL in under two minutes.

---

## Where This Goes

**v1 (this):** Paste feedback → get artifacts

**v2:** Connect directly to Jira, Intercom, or Zendesk — no pasting required, feedback is pulled automatically on a schedule

**v3:** Runs every Monday morning — synthesises the past week's feedback and prepares the sprint brief before the PM logs on

**v4:** Full autonomous product scoping agent — given the company's OKRs, it monitors customer signals continuously and proposes roadmap changes without being asked

The vision is an AI PM employee that handles everything below the line of strategic judgment. You set the direction. The employee handles the work.

That is what Zamp builds for enterprises. This is what it looks like for product teams.

---

Built by Rushikesh Kulkarni

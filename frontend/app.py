import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ---------- CONFIG ----------
BACKEND_URL = "https://moneymapai.onrender.com"

st.set_page_config(page_title="AI Money Mentor", layout="wide")
st.title("💸 AI Money Mentor")

tabs = st.tabs([
    "🔥 FIRE Planner",
    "💪 Money Health",
    "💰 Tax AI",
    "📊 MF Portfolio"
])

# ---------- SESSION STATE ----------
if "fire_goals" not in st.session_state:
    st.session_state.fire_goals = [{"goal_name": "", "target_amount": 0, "target_year": 2030}]

if "holdings" not in st.session_state:
    st.session_state.holdings = [{"fund_name": "", "amount": 0}]

# ---------------- FIRE PLANNER ----------------
with tabs[0]:
    st.header("🔥 FIRE Planner")

    for i, g in enumerate(st.session_state.fire_goals):
        cols = st.columns([3, 2, 2, 1])
        g["goal_name"] = cols[0].text_input("Goal Name", value=g["goal_name"], key=f"name_{i}")
        g["target_amount"] = cols[1].number_input("Amount", value=g["target_amount"], key=f"amt_{i}")
        g["target_year"] = cols[2].number_input("Year", value=g["target_year"], key=f"year_{i}")
        if cols[3].button("❌", key=f"remove_goal_{i}"):
            st.session_state.fire_goals.pop(i)
            st.rerun()

    if st.button("➕ Add Goal"):
        st.session_state.fire_goals.append({"goal_name": "", "target_amount": 0, "target_year": 2030})
        st.rerun()

    age = st.number_input("Age", value=25)
    income = st.number_input("Monthly Income", value=50000)
    expenses = st.number_input("Monthly Expenses", value=20000)
    investments = st.number_input("Existing Investments", value=100000)

    if st.button("Generate Plan"):
        try:
            res = requests.post(
                f"{BACKEND_URL}/fire-planner",
                json={
                    "age": age,
                    "income": income,
                    "expenses": expenses,
                    "existing_investments": investments,
                    "goals": st.session_state.fire_goals
                },
                timeout=10
            )
            res.raise_for_status()
            plan = res.json().get("plan", "No plan generated")
        except Exception as e:
            plan = f"Error: {e}"

        st.text_area("Your FIRE Plan", plan, height=250)

# ---------------- MONEY HEALTH ----------------
with tabs[1]:
    st.header("💪 Money Health Score")

    emergency = st.slider("Emergency Fund", 0, 100, 50)
    insurance = st.slider("Insurance", 0, 100, 50)
    investment = st.slider("Investments", 0, 100, 50)
    debt = st.slider("Debt", 0, 100, 20)
    tax = st.slider("Tax Efficiency", 0, 100, 50)
    retirement = st.slider("Retirement", 0, 100, 40)

    if st.button("Check Score"):
        try:
            res = requests.post(
                f"{BACKEND_URL}/money-health",
                json={
                    "emergency_fund": emergency,
                    "insurance_coverage": insurance,
                    "investments": investment,
                    "debt": debt,
                    "tax_efficiency": tax,
                    "retirement_savings": retirement
                },
                timeout=10
            )

            res.raise_for_status()
            result = res.json()

            score = result.get("score", 0)
            advice = result.get("advice", "")

            st.subheader(f"Score: {score}/100")
            st.progress(int(score))
            st.text_area("Advice", advice)

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- TAX AI ----------------
with tabs[2]:
    st.header("💰 Tax AI Assistant")

    query = st.text_area("Ask your tax question:")

    if st.button("Get Answer"):
        try:
            res = requests.post(
                f"{BACKEND_URL}/tax-ai",
                json={"query": query},
                timeout=15
            )

            res.raise_for_status()
            data = res.json()

            if "error" in data:
                st.warning("⚠️ AI unavailable. Showing basic advice.")
                st.text_area("Answer", "Invest in ELSS, NPS, and maximize 80C deductions.", height=200)
            else:
                st.text_area("AI Answer", data["answer"], height=250)

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- MF PORTFOLIO ----------------
with tabs[3]:
    st.header("📊 MF Portfolio X-Ray")

    for i, h in enumerate(st.session_state.holdings):
        cols = st.columns([3, 2, 1])
        h["fund_name"] = cols[0].text_input("Fund Name", value=h["fund_name"], key=f"fund_{i}")
        h["amount"] = cols[1].number_input("Amount", value=h["amount"], key=f"amt_hold_{i}")
        if cols[2].button("❌", key=f"remove_hold_{i}"):
            st.session_state.holdings.pop(i)
            st.rerun()

    if st.button("➕ Add Fund"):
        st.session_state.holdings.append({"fund_name": "", "amount": 0})
        st.rerun()

    if st.button("Analyze Portfolio"):
        try:
            res = requests.post(
                f"{BACKEND_URL}/mf-xray",
                json={"holdings": st.session_state.holdings},
                timeout=10
            )

            res.raise_for_status()
            data = res.json()

            df = pd.DataFrame(data.get("top_holdings", []))

            if not df.empty:
                st.table(df)

                fig1 = px.pie(df, names="fund_name", values="amount", title="Portfolio Split")
                st.plotly_chart(fig1, use_container_width=True)

                fig2 = px.bar(df, x="fund_name", y="amount", title="Top Holdings")
                st.plotly_chart(fig2, use_container_width=True)

            st.text_area("Advice", data.get("advice", ""), height=150)

        except Exception as e:
            st.error(f"Error: {e}")
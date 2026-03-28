from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

# ---------- LOAD ENV ----------
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ---------- APP ----------
app = FastAPI(title="AI Money Mentor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# FIRE PLANNER
# -------------------------------
@app.post("/fire-planner")
def fire_planner(data: dict):
    try:
        income = data.get("income", 0)
        expenses = data.get("expenses", 0)
        goals = data.get("goals", [])

        monthly_saving = max(income - expenses, 0)

        goal_summary = "\n".join([
            f"- {g.get('goal_name')} → ₹{g.get('target_amount')} by {g.get('target_year')}"
            for g in goals
        ])

        plan = f"""
📊 FIRE PLAN

💰 Monthly Saving: ₹{monthly_saving}

🎯 Goals:
{goal_summary if goal_summary else "No goals added"}

📌 Suggestion:
- Invest in SIPs
- Maintain emergency fund (6 months expenses)
- Diversify across equity + debt
"""

        return {"plan": plan.strip()}

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# MONEY HEALTH SCORE
# -------------------------------
@app.post("/money-health")
def money_health(data: dict):
    try:
        score = round((
            data.get("emergency_fund", 0) +
            data.get("insurance_coverage", 0) +
            data.get("investments", 0) +
            (100 - data.get("debt", 0)) +
            data.get("tax_efficiency", 0) +
            data.get("retirement_savings", 0)
        ) / 6, 2)

        if score < 40:
            advice = "⚠️ Poor financial health. Focus on saving and reducing debt."
        elif score < 70:
            advice = "⚡ Average financial health. Improve investments and tax planning."
        else:
            advice = "✅ Excellent financial health. Keep optimizing investments!"

        return {"score": score, "advice": advice}

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# TAX AI (SECURE)
# -------------------------------
@app.post("/tax-ai")
def tax_ai(data: dict):
    try:
        user_query = data.get("query", "")

        if not OPENROUTER_API_KEY:
            return {"error": "API key not configured"}

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an expert Indian financial and tax advisor."},
                {"role": "user", "content": user_query}
            ],
            "max_tokens": 500
        }

        response = requests.post(url, headers=headers, json=payload, timeout=15)

        if response.status_code == 401:
            return {"error": "Unauthorized API key"}

        response.raise_for_status()

        answer = response.json()["choices"][0]["message"]["content"]

        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# MF PORTFOLIO X-RAY
# -------------------------------
@app.post("/mf-xray")
def mf_xray(data: dict):
    try:
        holdings = data.get("holdings", [])

        if not holdings:
            return {"error": "No holdings provided"}

        total = sum(h.get("amount", 0) for h in holdings)

        # Sort top holdings
        sorted_holdings = sorted(holdings, key=lambda x: x.get("amount", 0), reverse=True)
        top_holdings = sorted_holdings[:5]

        concentration = sum(h.get("amount", 0) for h in top_holdings) / total

        if concentration > 0.7:
            advice = "⚠️ High concentration risk. Diversify your portfolio."
        else:
            advice = "✅ Portfolio looks diversified."

        return {
            "total_investment": total,
            "top_holdings": top_holdings,
            "advice": advice
        }

    except Exception as e:
        return {"error": str(e)}
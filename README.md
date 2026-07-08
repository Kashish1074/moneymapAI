# MoneyMapAI
# AI Money Mentor

An AI-powered personal finance assistant that helps users plan, analyze, and optimize their finances — making financial planning as simple as chatting.

---

## 🚀 Features

### 🔥 FIRE Planner

* Generate a Financial Independence roadmap
* Monthly savings calculation
* Goal-based planning (amount + timeline)

### 💪 Money Health Score

* Get a financial wellness score out of 100
* Based on:

  * Emergency fund
  * Insurance coverage
  * Investment diversification
  * Debt health
  * Tax efficiency
  * Retirement readiness

### 💰 Tax AI Assistant

* Ask any tax-related question
* AI-powered responses
* Personalized Indian tax advice

### 📊 Mutual Fund Portfolio X-Ray

* Analyze your mutual fund holdings
* View top holdings
* Interactive pie & bar charts
* Portfolio diversification insights

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI
* **AI:** OpenRouter API
* **Visualization:** Plotly

---

## 📁 Project Structure

```
ai_money_mentor/
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 🔹 1. Clone Repository

```
git clone <your-repo-link>
cd ai_money_mentor
```

---

### 🔹 2. Backend Setup

```
cd backend
pip install -r requirements.txt
```

Create a `.env` file inside the backend folder:

```
OPENROUTER_API_KEY=your_api_key_here
```

Run backend server:

```
uvicorn main:app --reload
```

---

### 🔹 3. Frontend Setup

```
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 Deployment

* **Backend:** Render
* **Frontend:** Streamlit Cloud

---

## 🔐 Security

* API keys stored securely in `.env`
* `.env` excluded using `.gitignore`
* No sensitive data exposed in frontend

---

## 🎯 Future Improvements

* 📄 Upload Form 16 for automatic tax analysis
* 📊 Upload portfolio CSV for deeper insights
* 📈 Unified financial dashboard
* 🎤 Voice-based AI financial advisor

---
## Changelog

- Improved project documentation.

## 👨‍💻 Author

**Kashish**


import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="CreditLens AI", layout="wide")

st.title("🏦 CreditLens AI — Alternative Credit Scoring")
st.subheader("Bank Statement Intelligence & Creditworthiness Assessment")

st.sidebar.header("Input Financial Data")
income = st.sidebar.slider("Monthly Income (₹)", 5000, 150000, 35000)
expenses = st.sidebar.slider("Monthly Expenses (₹)", 3000, 100000, 22000)
utility = st.sidebar.slider("Utility Bills Paid on Time (%)", 0, 100, 92)
rent = st.sidebar.slider("Rent Payment Regularity (%)", 0, 100, 100)
upi = st.sidebar.slider("UPI Transactions/Month", 0, 200, 67)
tenure = st.sidebar.slider("Months at Current Job", 0, 120, 18)
overdraft = st.sidebar.slider("Account Overdrafts (Last 12m)", 0, 24, 1)
balance = st.sidebar.slider("Avg Monthly Balance (₹)", 500, 50000, 8500)

def compute_score(income, expenses, utility, rent, upi, tenure, overdraft, balance):
    score = 300
    savings_rate = (income - expenses) / income
    score += min(utility * 1.2, 120)
    score += min(rent * 1.0, 100)
    score += min(savings_rate * 200, 100)
    score += min(upi * 0.8, 80)
    score += min(tenure * 1.5, 90)
    score += min(balance / 500, 80)
    score -= overdraft * 15
    return max(300, min(900, int(score)))

score = compute_score(income, expenses, utility, rent, upi, tenure, overdraft, balance)

col1, col2, col3 = st.columns(3)
col1.metric("Credit Score", f"{score}/900")
col2.metric("Monthly Savings", f"₹{income - expenses:,}")
col3.metric("Savings Rate", f"{round((income-expenses)/income*100)}%")

if score >= 750:
    st.success(f"✅ Score: {score} — Excellent | Low Risk")
elif score >= 650:
    st.info(f"🟡 Score: {score} — Good | Moderate Risk")
elif score >= 550:
    st.warning(f"⚠️ Score: {score} — Fair | Medium Risk")
else:
    st.error(f"❌ Score: {score} — Poor | High Risk")

st.subheader("Score Components")
components = {
    "Utility Payments": min(utility * 1.2, 120),
    "Rent Regularity": min(rent * 1.0, 100),
    "Savings Rate": min((income-expenses)/income * 200, 100),
    "UPI Activity": min(upi * 0.8, 80),
    "Job Tenure": min(tenure * 1.5, 90),
    "Avg Balance": min(balance / 500, 80),
}
fig = go.Figure(go.Bar(
    x=list(components.values()),
    y=list(components.keys()),
    orientation='h',
    marker_color='#f0a500'
))
fig.update_layout(template="plotly_dark", height=300)
st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Title and Description
st.title("Investment Property and Primary Residence Financial Analysis")
st.write("This app provides a detailed analysis of property investments, cash flow, and long-term financial outcomes.")
st.write("Personalized investment return app developed by Kyle Kaufman")

# Sidebar Inputs
st.sidebar.header("User Inputs")
investment_price = st.sidebar.number_input("Investment Property Price ($)", value=539000)
investment_loan = st.sidebar.number_input("Investment Loan Amount ($)", value=480000)
investment_rate = st.sidebar.number_input("Investment Interest Rate (%)", value=6.5, step=0.1) / 100
investment_term = st.sidebar.number_input("Investment Loan Term (years)", value=30)
investment_rent = st.sidebar.number_input("Monthly Rental Income ($)", value=3600)
investment_expenses = st.sidebar.number_input("Monthly Expenses ($)", value=1000)
investment_pmi = st.sidebar.number_input("Monthly PMI ($)", value=200)

primary_price = st.sidebar.number_input("Primary Residence Price ($)", value=620000)
primary_loan = st.sidebar.number_input("Primary Loan Amount ($)", value=620000)
primary_rate = st.sidebar.number_input("Primary Interest Rate (%)", value=6.3, step=0.1) / 100
primary_term = st.sidebar.number_input("Primary Loan Term (years)", value=30)
primary_pmi = st.sidebar.number_input("Monthly PMI ($)", value=90)

# Loan Calculation Function
def calculate_loan_details(principal, rate, term):
    monthly_rate = rate / 12
    num_payments = term * 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    return monthly_payment

# Calculate Monthly Payments
investment_monthly_payment = calculate_loan_details(investment_loan, investment_rate, investment_term)
primary_monthly_payment = calculate_loan_details(primary_loan, primary_rate, primary_term)

# Total Monthly Costs
investment_total_monthly = investment_monthly_payment + investment_expenses + investment_pmi
primary_total_monthly = primary_monthly_payment + primary_pmi

# Data for Visualization
years = np.arange(1, 31)
investment_cashflow = []
investment_balance = investment_loan
primary_balance = primary_loan
investment_equity = []
primary_equity = []
property_appreciation_rate = 0.03

for year in years:
    # Annual Equity and Cash Flow Calculation
    investment_cashflow.append((investment_rent * 12) - (investment_total_monthly * 12))
    investment_balance -= (investment_monthly_payment * 12 * 0.3)  # 30% goes to principal
    primary_balance -= (primary_monthly_payment * 12 * 0.3)

    # Property Appreciation
    investment_price *= (1 + property_appreciation_rate)
    primary_price *= (1 + property_appreciation_rate)

    # Equity
    investment_equity.append(investment_price - investment_balance)
    primary_equity.append(primary_price - primary_balance)

# DataFrame for Plotting
analysis_df = pd.DataFrame({
    "Year": years,
    "Investment Cash Flow": investment_cashflow,
    "Investment Equity": investment_equity,
    "Primary Equity": primary_equity,
})

# Visualizations
st.subheader("Investment Cash Flow Over Time")
cashflow_fig = px.line(analysis_df, x="Year", y="Investment Cash Flow", title="Annual Cash Flow", labels={"Investment Cash Flow": "Cash Flow ($)"})
st.plotly_chart(cashflow_fig)

st.subheader("Equity Growth Over Time")
equity_fig = px.line(
    analysis_df, x="Year", y=["Investment Equity", "Primary Equity"], 
    title="Equity Growth", labels={"value": "Equity ($)", "variable": "Property Type"}
)
st.plotly_chart(equity_fig)

st.subheader("Summary")
st.write("### Total Investment Cash Flow Over 30 Years: ", f"${sum(investment_cashflow):,.2f}")
st.write("### Total Investment Equity After 30 Years: ", f"${investment_equity[-1]:,.2f}")
st.write("### Total Primary Equity After 30 Years: ", f"${primary_equity[-1]:,.2f}")

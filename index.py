import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title="Personal Finance Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("💰 Personal Finance Dashboard")
st.write("Visualize and analyze your income and expenses over time.")

uploaded_file = st.file_uploader("Upload your transactions CSV", type="csv")

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    st.sidebar.header("🛠️ Filters")
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])
    
    if start_date and end_date:
        df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
    
    total_income = df[df['Amount'] > 0]['Amount'].sum()
    total_expense = df[df['Amount'] < 0]['Amount'].sum()
    net_balance = total_income + total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${abs(total_expense):,.2f}")
    col3.metric("Net Balance", f"${net_balance:,.2f}")

    st.markdown("---")
    
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    monthly = df.groupby(['Month']).agg(
        Income=pd.NamedAgg(column='Amount', aggfunc=lambda x: x[x > 0].sum()),
        Expense=pd.NamedAgg(column='Amount', aggfunc=lambda x: x[x < 0].sum())
    ).reset_index()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=monthly['Month'],
        y=monthly['Income'],
        name='Income',
        marker_color='green'
    ))
    fig_trend.add_trace(go.Bar(
        x=monthly['Month'],
        y=monthly['Expense'],
        name='Expenses',
        marker_color='red'
    ))
    fig_trend.update_layout(
        title="Monthly Income vs Expenses",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        barmode='group'
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    
else:
    st.info("📂 Please upload a CSV file containing your transaction data to see the dashboard.")

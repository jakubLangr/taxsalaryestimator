import streamlit as st
import pandas as pd
from salary import get_uk_takehome_salary, get_salary_bands
import plotly.graph_objects as go

st.set_page_config(page_title="UK Salary Calculator", layout="wide")

st.title("UK Salary Calculator")

# Input section
salary = st.number_input(
    "Enter your annual salary (GBP)",
    min_value=0,
    max_value=1000000,
    value=100000,
    step=1000,
    help="Enter your gross annual salary in GBP"
)

# Calculate take-home salary
if salary:
    result = get_uk_takehome_salary(salary)
    
    # Display summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Salary Breakdown")
        total_takehome = sum([result['tax_free'], result['basic'], result['higher'], result['additional']])
        total_tax = sum([result['taxes_free'], result['taxes_basic'], result['taxes_higher'], result['taxes_additional']])
        
        st.metric("Total Take-Home", f"£{total_takehome:,.2f}")
        st.metric("Total Tax", f"£{total_tax:,.2f}")
        
        st.write("Monthly Take-Home:", f"£{total_takehome/12:,.2f}")
        
    with col2:
        st.subheader("Tax Breakdown")
        tax_data = {
            "Category": ["Tax Free", "Basic Rate", "Higher Rate", "Additional Rate"],
            "Amount": [
                result['tax_free'],
                result['basic'],
                result['higher'],
                result['additional']
            ],
            "Tax": [
                result['taxes_free'],
                result['taxes_basic'],
                result['taxes_higher'],
                result['taxes_additional']
            ]
        }
        st.dataframe(pd.DataFrame(tax_data))

    # Visualization
    st.subheader("Salary Band Analysis")
    df = get_salary_bands(salary)
    
    fig = go.Figure()
    categories = ['tax_free', 'basic', 'higher', 'additional']
    colors = ['rgb(44, 160, 44)', 'rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(214, 39, 40)']
    
    for cat, color in zip(categories, colors):
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[cat],
            name=cat.replace('_', ' ').title(),
            stackgroup='one',
            fillcolor=color,
            line=dict(color=color)
        ))

    fig.update_layout(
        title='UK Take-Home Salary Analysis',
        xaxis_title='Salary (£)',
        yaxis_title='Amount (£)',
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    Note: This calculator includes:
    - Personal Allowance (reduces when earning over £100,000)
    - Basic rate tax (20%) from £12,571 to £50,270
    - Higher rate tax (40%) from £50,271 to £150,000
    - Additional rate tax (45%) over £150,001
    
    National Insurance contributions are not included in this calculation.
    """) 
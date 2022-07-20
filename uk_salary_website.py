from mlt.salary import *
import streamlit as st
import bokeh as bk

st.title("UK After Tax Salary Calculator")

salary = st.sidebar.number_input(min_value=0, max_value=1_000_000, value=35_000, step=1_000, label='salary')

salary_components = get_uk_takehome_salary(salary)

st.sidebar.json(salary_components)

figure = get_salary_figure(df)

st.bokeh_chart(figure, use_container_width=True)
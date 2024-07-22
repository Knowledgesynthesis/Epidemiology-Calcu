import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(layout="centered")
st.title("Epidemiology Calculator")

# Default data
data = {
    'exposed': {'disease': 100, 'noDisease': 900},
    'unexposed': {'disease': 300, 'noDisease': 700},
}

# Input fields
st.subheader("2x2 Table")
col1, col2 = st.columns(2)

with col1:
    data['exposed']['disease'] = st.number_input("Exposed - Disease", value=data['exposed']['disease'])
    data['exposed']['noDisease'] = st.number_input("Exposed - No Disease", value=data['exposed']['noDisease'])

with col2:
    data['unexposed']['disease'] = st.number_input("Unexposed - Disease", value=data['unexposed']['disease'])
    data['unexposed']['noDisease'] = st.number_input("Unexposed - No Disease", value=data['unexposed']['noDisease'])

def calculate_measures(data):
    a = data['exposed']['disease']
    b = data['exposed']['noDisease']
    c = data['unexposed']['disease']
    d = data['unexposed']['noDisease']
    
    total_exposed = a + b
    total_unexposed = c + d
    total_disease = a + c
    total_no_disease = b + d
    total = total_exposed + total_unexposed

    incidence_exposed = a / total_exposed
    incidence_unexposed = c / total_unexposed
    incidence = total_disease / total

    or_ratio = (a * d) / (b * c)
    rr = incidence_exposed / incidence_unexposed
    rd = incidence_exposed - incidence_unexposed
    arr = -rd
    arp = (rr - 1) / rr * 100
    pf = (1 - rr) * 100
    rrr = (1 - rr) * 100
    nnt = 1 / np.abs(rd) if rd != 0 else np.inf
    nnh = -nnt if rd != 0 else np.inf

    return {
        'or': or_ratio, 
        'rr': rr, 
        'rd': rd, 
        'arr': arr, 
        'arp': arp, 
        'pf': pf, 
        'rrr': rrr, 
        'nnt': nnt, 
        'nnh': nnh,
        'incidence': incidence * 100,
        'incidence_exposed': incidence_exposed * 100,
        'incidence_unexposed': incidence_unexposed * 100,
    }

calculations = calculate_measures(data)

def format_number(num):
    return f"{num:.2f}" if np.isfinite(num) else 'N/A'

incidence_data = pd.DataFrame([
    {'name': 'Exposed', 'value': calculations['incidence_exposed']},
    {'name': 'Unexposed', 'value': calculations['incidence_unexposed']},
    {'name': 'Overall', 'value': calculations['incidence']}
])

st.subheader("Incidence Comparison")
bar_chart = alt.Chart(incidence_data).mark_bar().encode(
    x='name',
    y='value'
).properties(
    width=alt.Step(50)  # controls width of bar.
)
st.altair_chart(bar_chart, use_container_width=True)

st.subheader("Key Measures")
measures = [
    ("RR (Relative Risk)", calculations['rr']),
    ("OR (Odds Ratio)", calculations['or']),
    ("ARR (Absolute Risk Reduction)", calculations['arr']),
    ("RRR (Relative Risk Reduction)", calculations['rrr']),
    ("NNT (Number Needed to Treat)", calculations['nnt']),
    ("NNH (Number Needed to Harm)", calculations['nnh']),
    ("AR% (Attributable Risk Percent)", calculations['arp']),
    ("PF (Preventive Fraction)", calculations['pf']),
]

for name, value in measures:
    st.write(f"**{name}:** {format_number(value)}")

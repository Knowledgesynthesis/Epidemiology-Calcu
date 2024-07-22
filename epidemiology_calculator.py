import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout="wide")
st.title("Epidemiology Calculator")

# Default data
data = {
    'exposed': {'disease': 100, 'noDisease': 900},
    'unexposed': {'disease': 300, 'noDisease': 700},
}

# Input fields in table layout
st.subheader("2x2 Table")

table_col1, table_col2, table_col3, table_col4 = st.columns([1, 1, 1, 1])

with table_col1:
    st.write("")
    st.write("Exposed")
    st.write("Unexposed")

with table_col2:
    st.write("Disease")
    data['exposed']['disease'] = st.number_input("Exposed - Disease", value=data['exposed']['disease'], key="exposed_disease")
    data['unexposed']['disease'] = st.number_input("Unexposed - Disease", value=data['unexposed']['disease'], key="unexposed_disease")

with table_col3:
    st.write("No Disease")
    data['exposed']['noDisease'] = st.number_input("Exposed - No Disease", value=data['exposed']['noDisease'], key="exposed_no_disease")
    data['unexposed']['noDisease'] = st.number_input("Unexposed - No Disease", value=data['unexposed']['noDisease'], key="unexposed_no_disease")

with table_col4:
    st.write("Total")
    total_exposed = data['exposed']['disease'] + data['exposed']['noDisease']
    total_unexposed = data['unexposed']['disease'] + data['unexposed']['noDisease']
    st.write(total_exposed)
    st.write(total_unexposed)

# Calculate column totals
total_disease = data['exposed']['disease'] + data['unexposed']['disease']
total_no_disease = data['exposed']['noDisease'] + data['unexposed']['noDisease']
grand_total = total_exposed + total_unexposed

st.write("### Table Summary")
table_data = pd.DataFrame({
    '': ['Exposed', 'Unexposed', 'Total'],
    'Disease': [data['exposed']['disease'], data['unexposed']['disease'], total_disease],
    'No Disease': [data['exposed']['noDisease'], data['unexposed']['noDisease'], total_no_disease],
    'Total': [total_exposed, total_unexposed, grand_total]
})
st.table(table_data)

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
        'or': round(or_ratio, 3), 
        'rr': round(rr, 3), 
        'rd': round(rd, 3), 
        'arr': round(arr, 3), 
        'arp': round(arp, 3), 
        'pf': round(pf, 3), 
        'rrr': round(rrr, 3), 
        'nnt': round(nnt, 3), 
        'nnh': round(nnh, 3),
        'incidence': round(incidence * 100, 3),
        'incidence_exposed': round(incidence_exposed * 100, 3),
        'incidence_unexposed': round(incidence_unexposed * 100, 3),
    }

# Update data dictionary with user inputs
calculations = calculate_measures(data)

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
    ("RD (Risk Difference)", calculations['rd']),
    ("ARR (Absolute Risk Reduction)", calculations['arr']),
    ("RRR (Relative Risk Reduction)", calculations['rrr']),
    ("NNT (Number Needed to Treat)", calculations['nnt']),
    ("NNH (Number Needed to Harm)", calculations['nnh']),
    ("AR% (Attributable Risk Percent)", calculations['arp']),
    ("PF (Preventive Fraction)", calculations['pf']),
]

for name, value in measures:
    st.write(f"**{name}:** {value}")

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Set page layout to centered
st.set_page_config(layout="centered")
st.title("Epidemiology Calculator")

# Default data
data = {
    'exposed': {'disease': 100, 'noDisease': 900},
    'unexposed': {'disease': 300, 'noDisease': 700},
}

# Input fields in table layout
st.subheader("2x2 Table")

# Create columns to center the input and table summary
table_col1, table_col2, table_col3 = st.columns([1, 2, 1])

with table_col2:
    st.write("### Input Table")
    st.write("")

    data['exposed']['disease'] = st.number_input("Exposed/Treated - Disease", value=data['exposed']['disease'], key="exposed_disease")
    data['exposed']['noDisease'] = st.number_input("Exposed/Treated - No Disease", value=data['exposed']['noDisease'], key="exposed_no_disease")
    data['unexposed']['disease'] = st.number_input("Unexposed/Control - Disease", value=data['unexposed']['disease'], key="unexposed_disease")
    data['unexposed']['noDisease'] = st.number_input("Unexposed/Control - No Disease", value=data['unexposed']['noDisease'], key="unexposed_no_disease")

    # Calculate totals for each row
    total_exposed = data['exposed']['disease'] + data['exposed']['noDisease']
    total_unexposed = data['unexposed']['disease'] + data['unexposed']['noDisease']

    # Calculate column totals
    total_disease = data['exposed']['disease'] + data['unexposed']['disease']
    total_no_disease = data['exposed']['noDisease'] + data['unexposed']['noDisease']
    grand_total = total_exposed + total_unexposed

    st.write("### Table Summary")
    table_data = pd.DataFrame({
        '': ['Exposed/Treated', 'Unexposed/Control', 'Total'],
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
        'formulas': {
            'or': f"(a * d) / (b * c) = ({a} * {d}) / ({b} * {c}) = {round(or_ratio, 3)}",
            'rr': f"incidence_exposed / incidence_unexposed = {round(incidence_exposed, 3)} / {round(incidence_unexposed, 3)} = {round(rr, 3)}",
            'rd': f"incidence_exposed - incidence_unexposed = {round(incidence_exposed, 3)} - {round(incidence_unexposed, 3)} = {round(rd, 3)}",
            'arr': f"-rd = {-round(rd, 3)}",
            'arp': f"(rr - 1) / rr * 100 = ({round(rr, 3)} - 1) / {round(rr, 3)} * 100 = {round(arp, 3)}",
            'pf': f"(1 - rr) * 100 = (1 - {round(rr, 3)}) * 100 = {round(pf, 3)}",
            'rrr': f"(1 - rr) * 100 = (1 - {round(rr, 3)}) * 100 = {round(rrr, 3)}",
            'nnt': f"1 / |rd| = 1 / |{round(rd, 3)}| = {round(nnt, 3) if nnt != np.inf else '∞'}",
            'nnh': f"-nnt = {-round(nnt, 3) if nnt != np.inf else '∞'}",
        }
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
    ("RR (Relative Risk)", calculations['rr'], calculations['formulas']['rr']),
    ("OR (Odds Ratio)", calculations['or'], calculations['formulas']['or']),
    ("RD (Risk Difference)", calculations['rd'], calculations['formulas']['rd'], " { (+) RD indicates a harmful exposure, (-) RD indicates a preventive exposure }"),
    ("ARR (Absolute Risk Reduction)", calculations['arr'], calculations['formulas']['arr']),
    ("_**Harmful Exposure (e.g. risk factor) or when RD is +:**_", "", ""),
    ("&nbsp;&nbsp;&nbsp;AR% (Attributable Risk Percent)", calculations['arp'], calculations['formulas']['arp']),
    ("_**Preventive Exposure (e.g. treatment) or when RD is -:**_", "", ""),
    ("&nbsp;&nbsp;&nbsp;PF (Preventive Fraction)", calculations['pf'], calculations['formulas']['pf']),
    ("RRR (Relative Risk Reduction)", calculations['rrr'], calculations['formulas']['rrr']),
    ("NNT (Number Needed to Treat)", calculations['nnt'], calculations['formulas']['nnt']),
    ("NNH (Number Needed to Harm)", calculations['nnh'], calculations['formulas']['nnh']),
]

for measure in measures:
    if len(measure) == 3:
        st.write(f"**{measure[0]}**: {measure[1]}")
        st.write(f"*Formula:* {measure[2]}")
    elif len(measure) == 4:
        st.write(f"**{measure[0]}**: {measure[1]}{measure[3]}")
        st.write(f"*Formula:* {measure[2]}")
    else:
        st.markdown(measure[0], unsafe_allow_html=True)

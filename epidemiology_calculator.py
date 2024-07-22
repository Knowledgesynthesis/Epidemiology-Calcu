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

    incidence_exposed = a / total_exposed if total_exposed != 0 else 0
    incidence_unexposed = c / total_unexposed if total_unexposed != 0 else 0
    incidence = total_disease / total if total != 0 else 0

    or_ratio = (a * d) / (b * c) if b * c != 0 else np.inf
    rr = incidence_exposed / incidence_unexposed if incidence_unexposed != 0 else np.inf
    rd = incidence_exposed - incidence_unexposed
    arr = incidence_unexposed - incidence_exposed
    arp = (incidence_exposed - incidence_unexposed) / incidence_exposed * 100 if incidence_exposed != 0 else np.inf
    pf = (incidence_unexposed - incidence_exposed) / incidence_unexposed * 100 if incidence_unexposed != 0 else np.inf
    rrr = (1 - rr) * 100 if rr != np.inf else np.inf
    nnt = 1 / np.abs(arr) if arr != 0 else np.inf
    nnh = 1 / np.abs(arr) if arr != 0 else np.inf

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
    ("OR (Odds Ratio)", "OR = (a * d) / (b * c)", calculations['or']),
    ("RR (Relative Risk)", "RR = (a / (a + b)) / (c / (c + d))", calculations['rr']),
    ("RD (Risk Difference)", "RD = (a / (a + b)) - (c / (c + d))", f"{calculations['rd']}      <span style='color:grey; font-size:small;'>{{ (+) RD indicates a harmful exposure, (-) RD indicates a preventive exposure }}</span>"),
    ("ARR (Absolute Risk Reduction)", "ARR = H5 - H4", calculations['arr']),
    ("***Harmful Exposure (e.g. risk factor) or when RD is +:***", "", ""),
    ("&nbsp;&nbsp;&nbsp;AR% (Attributable Risk Percent)", "ARP = (H4 - H5) / H4", calculations['arp']),
    ("***Preventive Exposure (e.g. treatment) or when RD is -:***", "", ""),
    ("&nbsp;&nbsp;&nbsp;PF (Preventive Fraction)", "PF = (H5 - H4) / H5", calculations['pf']),
    ("RRR (Relative Risk Reduction)", "RRR = 1 - H6", calculations['rrr']),
    ("***Number needed to treat (NNT)***", "NNT = 1 / (H5 - H4)", calculations['nnt']),
    ("***Number needed to harm (NNH)***", "NNH = 1 / (H4 - H5)", calculations['nnh']),
]

st.markdown("***where:***")
st.markdown("***H4 = Incidence among exposed***")
st.markdown("***H5 = Incidence among unexposed***")
st.markdown("***H6 = Relative Risk / Risk Ratio (RR)***")
st.write("")

for measure in measures:
    if len(measure) == 3:
        st.markdown(f"**{measure[0]}**:")
        st.markdown(f"Formula: {measure[1]}")
        st.markdown(f"Value: {measure[2]}")
    else:
        st.markdown(f"{measure[0]}", unsafe_allow_html=True)
    st.write("")  # Add a blank line for spacing

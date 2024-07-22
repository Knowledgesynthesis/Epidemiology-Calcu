import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout="centered")
st.title("Epidemiology Calculator")

# Default data
data = {
    'exposed': {'disease': 100, 'noDisease': 900},
    'unexposed': {'disease': 300, 'noDisease': 700},
}

# Input fields in table layout
st.subheader("2x2 Table")

table_data = [
    ["Exposed", st.number_input("Exposed - Disease", value=data['exposed']['disease'], key="exposed_disease"), 
               st.number_input("Exposed - No Disease", value=data['exposed']['noDisease'], key="exposed_no_disease"), 0],
    ["Unexposed", st.number_input("Unexposed - Disease", value=data['unexposed']['disease'], key="unexposed_disease"), 
                 st.number_input("Unexposed - No Disease", value=data['unexposed']['noDisease'], key="unexposed_no_disease"), 0]
]

# Calculate totals for each row
for row in table_data:
    row[3] = row[1] + row[2]

# Calculate column totals
total_disease = table_data[0][1] + table_data[1][1]
total_no_disease = table_data[0][2] + table_data[1][2]
total_total = table_data[0][3] + table_data[1][3]

# Display the input table
st.write("### Input Table")
st.write(pd.DataFrame(table_data, columns=["", "Disease", "No Disease", "Total"]))

# Calculate summary table data
summary_data = pd.DataFrame({
    '': ['Exposed', 'Unexposed', 'Total'],
    'Disease': [table_data[0][1], table_data[1][1], total_disease],
    'No Disease': [table_data[0][2], table_data[1][2], total_no_disease],
    'Total': [table_data[0][3], table_data[1][3], total_total]
})

st.write("### Table Summary")
st.write(summary_data)

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
        'or': round(or_ratio, 2), 
        'rr': round(rr, 2), 
        'rd': round(rd, 2), 
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

# Update data dictionary with user inputs
data['exposed']['disease'] = table_data[0][1]
data['exposed']['noDisease'] = table_data[0][2]
data['unexposed']['disease'] = table_data[1][1]
data['unexposed']['noDisease'] = table_data[1][2]

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
    ("RD (Risk Difference)", calculations['rd']),
    ("ARR (Absolute Risk Reduction)", f"{format_number(calculations['arr'])}%"),
    ("RRR (Relative Risk Reduction)", f"{format_number(calculations['rrr'])}%"),
    ("NNT (Number Needed to Treat)", format_number(calculations['nnt'])),
    ("NNH (Number Needed to Harm)", format_number(calculations['nnh'])),
    ("AR% (Attributable Risk Percent)", f"{format_number(calculations['arp'])}%"),
    ("PF (Preventive Fraction)", f"{format_number(calculations['pf'])}%"),
]

for name, value in measures:
    st.write(f"**{name}:** {value}")

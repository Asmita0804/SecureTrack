
import pandas as pd
import streamlit as st

from database import (
    add_risk, get_risks, update_risk, delete_risk,
    add_control, get_controls,
    add_mitigation, get_mitigations
)


# Page setup
st.set_page_config(
    page_title="SecureTrack",
    page_icon="🔐",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #F5F7FA;
    }

    h1, h2, h3 {
        color: #1E293B;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
    }

    .stButton button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔐 SecureTrack")
st.caption("Cybersecurity Risk & Compliance Tracker")
st.write("Monitor risks, manage security controls, and track mitigation plans.")

# Calculate risk severity
def calculate_level(score):
    if score <= 4:
        return "Low"
    elif score <= 9:
        return "Medium"
    elif score <= 16:
        return "High"
    else:
        return "Critical"


# Get data from database
risks = get_risks()
controls = get_controls()
mitigations = get_mitigations()


# Add a New Risk
st.divider()
st.header("Add a New Risk")

with st.form("risk_form"):
    risk_name = st.text_input("Enter Risk Name")
    likelihood = st.slider("Likelihood", 1, 5, 3)
    impact = st.slider("Impact", 1, 5, 3)

    submitted = st.form_submit_button("Calculate Risk")

    if submitted:
        if risk_name.strip():
            score = likelihood * impact
            level = calculate_level(score)

            add_risk(risk_name, likelihood, impact, score, level)
            st.success("Risk saved successfully!")
            st.rerun()
        else:
            st.warning("Please enter a risk name.")


st.divider()


# Risk Dashboard
st.header("📊 Risk Overview")
st.caption("A quick summary of your cybersecurity risks.")

risk_data = [
    {
        "Risk": row[1],
        "Likelihood": row[2],
        "Impact": row[3],
        "Score": row[4],
        "Level": row[5]
    }
    for row in risks
]

total = len(risk_data)
high = sum(r["Level"] in ["High", "Critical"] for r in risk_data)
low = sum(r["Level"] == "Low" for r in risk_data)

col1, col2, col3 = st.columns(3)

col1.metric("Total Risks", total)
col2.metric("High & Critical", high)
col3.metric("Low Risk", low)

if risk_data:
    st.subheader("Risk Severity Distribution")

    levels = ["Low", "Medium", "High", "Critical"]

    counts = [
        sum(r["Level"] == level for r in risk_data)
        for level in levels
    ]

    chart_data = pd.DataFrame({
        "Risk Level": levels,
        "Number of Risks": counts
    })

    st.bar_chart(chart_data, x="Risk Level", y="Number of Risks")


st.divider()


# Compliance Tracking
st.header("🛡️ Compliance Overview")
st.caption("Track the implementation status of your security controls.")
st.subheader("Add Security Control")

with st.form("control_form"):
    control_name = st.text_input("Control Name")
    description = st.text_area("Control Description")

    status = st.selectbox(
        "Implementation Status",
        ["Implemented", "Pending", "Not Implemented"]
    )

    control_submitted = st.form_submit_button("Add Control")

    if control_submitted:
        if control_name.strip():
            add_control(control_name, description, status)
            st.success("Security control added successfully!")
            st.rerun()
        else:
            st.warning("Please enter a control name.")


# Compliance Summary
st.subheader("Compliance Summary")

total_controls = len(controls)
implemented = sum(row[3] == "Implemented" for row in controls)
pending = sum(row[3] == "Pending" for row in controls)
not_implemented = sum(row[3] == "Not Implemented" for row in controls)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Controls", total_controls)
col2.metric("Implemented", implemented)
col3.metric("Pending", pending)
col4.metric("Not Implemented", not_implemented)


# Compliance Register
st.subheader("Compliance Register")

if controls:
    control_data = [
        {
            "Control Name": row[1],
            "Description": row[2],
            "Status": row[3]
        }
        for row in controls
    ]

    st.dataframe(control_data, use_container_width=True)
else:
    st.info("No security controls added yet.")


st.divider()


# Risk Register
st.header("📋 Risk Register")
st.caption("View, search, filter, and sort all recorded risks.")

sort_option = st.selectbox(
    "Sort Risks By",
    ["Highest Score", "Lowest Score", "Risk Name"]
)

selected_level = st.selectbox(
    "Filter by Risk Level",
    ["All", "Low", "Medium", "High", "Critical"]
)

search_name = st.text_input("Search Risk by Name")

filtered_risks = [
    risk for risk in risk_data
    if search_name.lower() in risk["Risk"].lower()
    and (selected_level == "All" or risk["Level"] == selected_level)
]

if sort_option == "Highest Score":
    filtered_risks = sorted(
        filtered_risks, key=lambda risk: risk["Score"], reverse=True
    )
elif sort_option == "Lowest Score":
    filtered_risks = sorted(
        filtered_risks, key=lambda risk: risk["Score"]
    )
else:
    filtered_risks = sorted(
        filtered_risks, key=lambda risk: risk["Risk"].lower()
    )

st.dataframe(filtered_risks, use_container_width=True)


# Download Risk Report
csv_data = pd.DataFrame(risk_data).to_csv(index=False)

st.download_button(
    label="Download Risk Report",
    data=csv_data,
    file_name="securetrack_risk_report.csv",
    mime="text/csv"
)


st.divider()


# Edit an Existing Risk
st.header("✏️ Edit Risk")
st.caption("Update the details and severity of an existing risk.") 

if risks:
    risk_options = {
        f"{row[0]} - {row[1]}": row
        for row in risks
    }

    selected_risk = st.selectbox(
        "Select a risk to edit",
        list(risk_options.keys())
    )

    risk = risk_options[selected_risk]

    new_name = st.text_input(
    "Risk Name", value=risk[1], key=f"edit_name_{risk[0]}"
    )

    new_likelihood = st.slider(
    "Likelihood", 1, 5, risk[2], key=f"edit_likelihood_{risk[0]}"
    )

    new_impact = st.slider(
    "Impact", 1, 5, risk[3], key=f"edit_impact_{risk[0]}"
    )

    if st.button("Update Risk"):
        new_score = new_likelihood * new_impact
        new_level = calculate_level(new_score)

        update_risk(
            risk[0], new_name, new_likelihood,
            new_impact, new_score, new_level
        )

        st.success("Risk updated successfully!")
        st.rerun()
else:
    st.info("No risks available to edit.")


st.divider()


# Risk Mitigation
st.header("🛠️ Risk Mitigation")
st.caption("Create and track plans to reduce identified cybersecurity risks.")

if risks:
    risk_options = {
        f"{row[0]} - {row[1]}": row[0]
        for row in risks
    }

    with st.form("mitigation_form"):
        selected_risk = st.selectbox(
            "Select Risk",
            list(risk_options.keys())
        )

        plan = st.text_area("Mitigation Plan")

        status = st.selectbox(
            "Plan Status",
            ["Pending", "In Progress", "Completed"]
        )

        mitigation_submitted = st.form_submit_button("Save Mitigation Plan")

        if mitigation_submitted:
            if plan.strip():
                add_mitigation(risk_options[selected_risk], plan, status)
                st.success("Mitigation plan saved successfully!")
                st.rerun()
            else:
                st.warning("Please enter a mitigation plan.")
else:
    st.info("Add a risk before creating a mitigation plan.")


# Mitigation Register
st.subheader("📋 Mitigation Register")
st.caption("Review the mitigation plans and their current status.")


risk_names = {
    row[0]: row[1]
    for row in risks
}

if mitigations:
    for item in mitigations:
        risk_name = risk_names.get(item[1], "Risk not found")

        st.write("**Risk:**", risk_name)
        st.write("**Mitigation Plan:**", item[2])
        st.write("**Status:**", item[3])
        st.divider()
else:
    st.info("No mitigation plans added yet.")


# Delete a Risk
st.header("🗑️ Delete Risk")
st.caption("Remove a risk that is no longer required.")

if risks:
    delete_options = {
        f"{row[0]} - {row[1]} (Score: {row[4]})": row[0]
        for row in risks
    }

    selected_risk = st.selectbox(
        "Select a risk to delete",
        list(delete_options.keys())
    )

    if st.button("Delete Selected Risk"):
        delete_risk(delete_options[selected_risk])
        st.success("Risk deleted successfully!")
        st.rerun()
else:
    st.info("No risks available to delete.")

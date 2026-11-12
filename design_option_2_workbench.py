#!/usr/bin/env python3
"""
Design Option 2: Underwriting Workbench
Banking interface for application search, affordability details, rule outcomes, decision timeline.
Connected to actual generated data - no mock values.
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(
    page_title="Underwriting Workbench - YottaFlex",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background: #102A43; }
    [data-testid="stSidebar"] * { color: white; }

    .detail-card {
        background: linear-gradient(135deg, #F5F7FA 0%, #FFFFFF 100%);
        border-left: 5px solid #0F766E;
        padding: 16px;
        margin-bottom: 12px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.08);
    }

    .app-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #E5EAEF;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.08);
        margin-bottom: 16px;
    }

    .status-approved { color: #10B981; font-weight: bold; font-size: 18px; }
    .status-review { color: #F59E0B; font-weight: bold; font-size: 18px; }
    .status-rejected { color: #EF4444; font-weight: bold; font-size: 18px; }

    .rule-box {
        background: linear-gradient(135deg, #F5F7FA 0%, #FFFFFF 100%);
        border-left: 5px solid #0F766E;
        padding: 14px;
        margin: 10px 0;
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(16, 42, 67, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Load data
data_dir = Path(__file__).parent / "data"

@st.cache_data
def load_data():
    return {
        "applications": pd.read_csv(data_dir / "loan_applications.csv"),
        "decisions": pd.read_csv(data_dir / "decisions.csv"),
        "affordability": pd.read_csv(data_dir / "affordability_checks.csv"),
        "incomes": pd.read_csv(data_dir / "incomes.csv"),
        "applicants": pd.read_csv(data_dir / "applicants.csv"),
    }

data = load_data()
apps = data["applications"]
decisions = data["decisions"]
affordability = data["affordability"]
incomes = data["incomes"]

# Sidebar
st.sidebar.title("YottaFlex Underwriting")
st.sidebar.markdown("---")

st.title("Underwriting Workbench")
st.markdown("**Synthetic data generated 2026-11-12. All names and details are generated for testing.**")
st.markdown("---")

# Search & Filters
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search_id = st.text_input("Search by Application ID", placeholder="LOAN-2026-000001")

with col2:
    status_filter = st.selectbox("Status", ["All", "APPROVED", "MANUAL_REVIEW", "REJECTED"])

with col3:
    aff_filter = st.selectbox("Affordability", ["All", "AFFORDABLE", "NOT_AFFORDABLE"])

# Filter applications
filtered_apps = apps.copy()

if search_id:
    filtered_apps = filtered_apps[filtered_apps["application_id"].str.contains(search_id, na=False)]

if status_filter != "All":
    filtered_apps = filtered_apps[filtered_apps["current_status"] == status_filter]

if aff_filter != "All":
    aff_apps = affordability[affordability["affordability_status"] == aff_filter]["application_id"].tolist()
    filtered_apps = filtered_apps[filtered_apps["application_id"].isin(aff_apps)]

st.markdown("---")
st.subheader(f"Results ({len(filtered_apps)} applications)")

# Display applications
for idx, row in filtered_apps.head(5).iterrows():
    app_id = row["application_id"]

    # Get decision
    dec = decisions[decisions["application_id"] == app_id]
    dec_status = dec.iloc[0]["decision_outcome"] if len(dec) > 0 else "UNKNOWN"

    # Get affordability
    aff = affordability[affordability["application_id"] == app_id]
    aff_status = aff.iloc[0]["affordability_status"] if len(aff) > 0 else "UNKNOWN"

    # Get income
    applicant_id = row["applicant_id"]
    app_incomes = incomes[incomes["applicant_id"] == applicant_id]
    verified_income = app_incomes[app_incomes["verification_status"] == "VERIFIED"]["gross_monthly_income"].sum()

    # Status colors
    status_color = "status-approved" if dec_status == "APPROVED" else "status-review" if dec_status == "MANUAL_REVIEW" else "status-rejected"

    with st.container(border=True):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.markdown(f"**{app_id}** | Applicant: {applicant_id}")
            st.markdown(f"Amount: ₹{row['requested_amount']:,.0f} | Term: {row['requested_term_months']} mo")

        with col2:
            st.markdown(f"<div class='{status_color}'>{dec_status}</div>", unsafe_allow_html=True)

        with col3:
            aff_color = "status-approved" if aff_status == "AFFORDABLE" else "status-review" if aff_status == "MARGINAL" else "status-rejected"
            st.markdown(f"<div class='{aff_color}'>{aff_status}</div>", unsafe_allow_html=True)

        # Expandable details
        with st.expander("📋 Decision Details & Affordability"):
            if len(dec) > 0:
                st.markdown("**Decision Outcome**")
                st.markdown(f"`{dec.iloc[0]['decision_outcome']}`")

                st.markdown("**Primary Reason**")
                st.markdown(f"`{dec.iloc[0]['primary_reason']}`")

                st.markdown("**Triggered Rules**")
                try:
                    rules = json.loads(dec.iloc[0]["triggered_rules"])
                    for rule in rules:
                        st.text(f"• {rule}")
                except:
                    st.text("Rules data unavailable")

            if len(aff) > 0:
                st.markdown("---")
                st.markdown("**Affordability Metrics**")
                aff_row = aff.iloc[0]

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Monthly Income", f"₹{aff_row['total_monthly_income']:,.0f}")
                with col2:
                    st.metric("Proposed EMI", f"₹{aff_row['proposed_emi']:,.0f}")
                with col3:
                    dti = aff_row['debt_to_income_ratio']
                    st.metric("DTI", f"{dti*100:.1f}%")

                st.markdown("**DTI Formula**")
                st.markdown("`DTI = (existing_debt + EMI) / monthly_income × 100`")
                st.text(f"Income: {aff_row['total_monthly_income']:.0f} | EMI: {aff_row['proposed_emi']:.0f} | DTI: {dti*100:.1f}%")

st.markdown("---")
st.subheader("8-Rule Decision Engine (Precedence Order)")

rules_info = [
    ("1", "TERM_RANGE", "Requested term outside product limits", "→ REJECT"),
    ("2", "AMOUNT_RANGE", "Requested amount outside product limits", "→ REJECT"),
    ("3", "MISSING_INCOME", "No verified income records", "→ MANUAL_REVIEW"),
    ("4", "UNVERIFIED_INCOME", "Income status UNVERIFIED/PENDING", "→ MANUAL_REVIEW"),
    ("5", "MISSING_DOCUMENTS", "Critical documents missing/rejected", "→ MANUAL_REVIEW"),
    ("6", "DTI_ACCEPTABLE", "DTI ≤ 40%", "→ APPROVE"),
    ("7", "DTI_MARGINAL", "40% < DTI ≤ 50%", "→ MANUAL_REVIEW"),
    ("8", "DTI_HIGH", "DTI > 50%", "→ REJECT"),
]

for num, name, desc, outcome in rules_info:
    st.markdown(f"<div class='rule-box'><strong>Rule {num}: {name}</strong><br/>{desc} <strong style='color:#0F766E'>{outcome}</strong></div>", unsafe_allow_html=True)


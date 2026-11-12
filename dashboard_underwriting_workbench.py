#!/usr/bin/env python3
"""
YottaFlex Underwriting Workbench
Searchable applications, affordability details, rule outcomes, and decision trace.

Run locally: streamlit run dashboard_underwriting_workbench.py
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Underwriting Workbench", layout="wide", initial_sidebar_state="collapsed")

# ============================================================================
# LOAD DATA
# ============================================================================

data_dir = Path(__file__).parent / "data"

def load_data():
    try:
        apps = pd.read_csv(data_dir / "loan_applications.csv")
        decisions = pd.read_csv(data_dir / "decisions.csv")
        affordability = pd.read_csv(data_dir / "affordability_checks.csv")
        applicants = pd.read_csv(data_dir / "applicants.csv")

        return {
            "applications": apps,
            "decisions": decisions,
            "affordability": affordability,
            "applicants": applicants
        }
    except FileNotFoundError:
        return None

data = load_data()

if data is None:
    st.error("❌ Synthetic data not found. Run: python generator.py")
    st.stop()

# ============================================================================
# TITLE
# ============================================================================

st.markdown("# 🔍 Underwriting Workbench")
st.markdown("**Search applications, view affordability details, trace decision rules**")
st.divider()

# ============================================================================
# SEARCH & FILTER
# ============================================================================

col1, col2, col3 = st.columns(3)

with col1:
    search_term = st.text_input("🔎 Search by Application ID", placeholder="e.g., LOAN-2026-000001")

with col2:
    status_filter = st.multiselect(
        "Filter by Status",
        ["APPROVED", "MANUAL_REVIEW", "REJECTED"],
        default=["APPROVED", "MANUAL_REVIEW", "REJECTED"]
    )

with col3:
    aff_filter = st.multiselect(
        "Filter by Affordability",
        ["AFFORDABLE", "MARGINAL", "NOT_AFFORDABLE"],
        default=["AFFORDABLE", "MARGINAL", "NOT_AFFORDABLE"]
    )

# Filter data
filtered_apps = data["applications"].copy()

if search_term:
    filtered_apps = filtered_apps[filtered_apps["application_id"].str.contains(search_term, na=False)]

filtered_apps = filtered_apps[filtered_apps["current_status"].isin(status_filter)]

# Add affordability filter
filtered_with_aff = filtered_apps.merge(
    data["affordability"][["application_id", "affordability_status"]],
    on="application_id",
    how="left"
)
filtered_with_aff = filtered_with_aff[filtered_with_aff["affordability_status"].isin(aff_filter)]

st.divider()

# ============================================================================
# APPLICATION LIST
# ============================================================================

st.markdown(f"### 📋 Applications ({len(filtered_with_aff)} found)")

if len(filtered_with_aff) == 0:
    st.info("No applications match your filters.")
else:
    for idx, app in filtered_with_aff.head(20).iterrows():
        # Get decision details
        decision = data["decisions"][data["decisions"]["application_id"] == app["application_id"]]
        affordability = data["affordability"][data["affordability"]["application_id"] == app["application_id"]]

        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 1.5, 1.5])

            with col1:
                st.markdown(f"**{app['application_id']}** | {app['applicant_id']}")
                st.write(f"Amount: ₹{app['requested_amount']:,.0f} | Term: {app['requested_term_months']} months")

            with col2:
                status_emoji = {"APPROVED": "✅", "REJECTED": "❌", "MANUAL_REVIEW": "⏳"}
                st.write(f"{status_emoji.get(app['current_status'], '?')} **{app['current_status']}**")

            with col3:
                if len(affordability) > 0:
                    aff_status = affordability.iloc[0]["affordability_status"]
                    aff_emoji = {"AFFORDABLE": "✓", "MARGINAL": "⚠", "NOT_AFFORDABLE": "✗"}
                    st.write(f"{aff_emoji.get(aff_status, '?')} {aff_status}")

            # Decision details (expandable)
            if len(decision) > 0:
                decision_row = decision.iloc[0]

                with st.expander(f"📋 Decision Details", expanded=False):
                    col_a, col_b = st.columns([1, 2])

                    with col_a:
                        st.write("**Outcome**")
                        st.code(decision_row["decision_outcome"])

                        st.write("**Primary Reason**")
                        st.code(decision_row["primary_reason"])

                    with col_b:
                        st.write("**Triggered Rules**")
                        rules = json.loads(decision_row["triggered_rules"]) if isinstance(decision_row["triggered_rules"], str) else []
                        for rule in rules:
                            st.write(f"  • `{rule}`")

                    if len(affordability) > 0:
                        aff = affordability.iloc[0]
                        st.divider()
                        st.write("**Affordability Metrics**")
                        col_x, col_y, col_z = st.columns(3)
                        with col_x:
                            st.metric("Monthly Income", f"₹{aff['total_monthly_income']:,.0f}")
                        with col_y:
                            st.metric("Proposed EMI", f"₹{aff['proposed_emi']:,.0f}")
                        with col_z:
                            st.metric("DTI", f"{aff['debt_to_income_ratio']:.2%}")

st.divider()

# ============================================================================
# DECISION RULE GUIDE
# ============================================================================

with st.expander("📚 Decision Rules Guide", expanded=False):
    st.markdown("""
    **8-Rule Precedence Engine** (checked in order, first match wins)

    1. **RULE_TERM_RANGE**: Requested term outside product limits → **REJECT**
    2. **RULE_AMOUNT_RANGE**: Requested amount outside product limits → **REJECT**
    3. **RULE_MISSING_INCOME**: No verified income records → **MANUAL_REVIEW**
    4. **RULE_UNVERIFIED_INCOME**: Income status is UNVERIFIED/PENDING → **MANUAL_REVIEW**
    5. **RULE_MISSING_DOCUMENTS**: Critical docs (ID, income) missing/rejected → **MANUAL_REVIEW**
    6. **RULE_DTI_ACCEPTABLE**: DTI ≤ 40% → **APPROVE**
    7. **RULE_DTI_MARGINAL**: 40% < DTI ≤ 50% → **MANUAL_REVIEW**
    8. **RULE_DTI_HIGH**: DTI > 50% → **REJECT**

    **Affordability Status**:
    - AFFORDABLE: DTI ≤ 40%
    - MARGINAL: 40% < DTI ≤ 50%
    - NOT_AFFORDABLE: DTI > 50%
    """)

st.divider()

st.caption("🤖 Dashboard Concept 2 of 3: Underwriting Workbench | Application Detail & Rule Trace Focus")

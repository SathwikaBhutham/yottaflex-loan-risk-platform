#!/usr/bin/env python3
"""
YottaFlex Underwriting Dashboard - FINAL PRODUCTION VERSION
Professional banking interface for application search, affordability details,
rule outcomes, and decision trace. Production-ready with enhanced styling.

Connected to actual generated data (seed: 20261112)
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="YottaFlex Underwriting Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "YottaFlex Loan Risk Platform v1.0"}
)

# ============================================================================
# PROFESSIONAL STYLING - BANKING INTERFACE
# ============================================================================

st.markdown("""
    <style>
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #102A43 0%, #0D1F33 100%);
        border-right: 2px solid #0F766E;
    }
    [data-testid="stSidebar"] * { color: white; }
    [data-testid="stSidebarNav"] { padding-top: 2rem; }

    /* Main Content */
    .block-container { padding-top: 2rem; }

    /* Cards and Containers */
    .detail-card {
        background: linear-gradient(135deg, #F5F7FA 0%, #FFFFFF 100%);
        border-left: 5px solid #0F766E;
        padding: 18px;
        margin-bottom: 14px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.08);
        transition: all 0.3s ease;
    }

    .detail-card:hover {
        box-shadow: 0 4px 12px rgba(16, 42, 67, 0.12);
        transform: translateY(-2px);
    }

    .app-card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #E5EAEF;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.08);
        margin-bottom: 18px;
        transition: all 0.3s ease;
    }

    .app-card:hover {
        box-shadow: 0 4px 16px rgba(16, 42, 67, 0.12);
        border-color: #0F766E;
    }

    /* Status Colors */
    .status-approved {
        color: #10B981;
        font-weight: 700;
        font-size: 16px;
        background: #D1FAE5;
        padding: 8px 16px;
        border-radius: 6px;
        display: inline-block;
    }

    .status-review {
        color: #F59E0B;
        font-weight: 700;
        font-size: 16px;
        background: #FEF3C7;
        padding: 8px 16px;
        border-radius: 6px;
        display: inline-block;
    }

    .status-rejected {
        color: #EF4444;
        font-weight: 700;
        font-size: 16px;
        background: #FEE2E2;
        padding: 8px 16px;
        border-radius: 6px;
        display: inline-block;
    }

    .aff-affordable {
        color: #10B981;
        font-weight: 700;
        font-size: 16px;
        background: #D1FAE5;
        padding: 8px 16px;
        border-radius: 6px;
        display: inline-block;
    }

    .aff-marginal {
        color: #F59E0B;
        font-weight: 700;
        font-size: 16px;
        background: #FEF3C7;
        padding: 8px 16px;
        border-radius: 6px;
        display: inline-block;
    }

    .aff-not {
        color: #EF4444;
        font-weight: 700;
        font-size: 16px;
        background: #FEE2E2;
        padding: 8px 16px;
        border-radius: 6px;
        display: inline-block;
    }

    /* Section Headers */
    .section-header {
        font-size: 20px;
        font-weight: 800;
        color: #102A43;
        margin-top: 24px;
        margin-bottom: 16px;
        border-bottom: 3px solid #0F766E;
        padding-bottom: 12px;
    }

    /* Rule Boxes */
    .rule-box {
        background: linear-gradient(135deg, #F5F7FA 0%, #FFFFFF 100%);
        border-left: 5px solid #0F766E;
        padding: 16px;
        margin: 12px 0;
        border-radius: 10px;
        box-shadow: 0 1px 4px rgba(16, 42, 67, 0.05);
        transition: all 0.3s ease;
    }

    .rule-box:hover {
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.08);
    }

    .rule-reject { border-left-color: #EF4444 !important; }
    .rule-review { border-left-color: #F59E0B !important; }
    .rule-approve { border-left-color: #10B981 !important; }

    /* Metrics */
    .metric-highlight {
        background: #D1F4F0;
        color: #0F766E;
        padding: 14px 18px;
        border-radius: 8px;
        font-weight: 700;
        margin: 10px 0;
        border-left: 4px solid #0F766E;
    }

    .metric-label {
        font-size: 11px;
        color: #596274;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #102A43;
        line-height: 1.2;
    }

    /* Filter Bar */
    .filter-container {
        background: linear-gradient(135deg, #F5F7FA 0%, #FFFFFF 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E5EAEF;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.05);
    }

    /* Info Boxes */
    .info-box {
        background: #D1F4F0;
        border-left: 4px solid #0F766E;
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
        color: #0F766E;
        font-size: 14px;
        line-height: 1.6;
    }

    /* Data Table */
    .dataframe { font-size: 13px; }
    .dataframe th { background: #D1F4F0 !important; color: #102A43 !important; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

data_dir = Path(__file__).parent / "data"

@st.cache_data
def load_data():
    """Load all project data"""
    try:
        return {
            "applications": pd.read_csv(data_dir / "loan_applications.csv"),
            "decisions": pd.read_csv(data_dir / "decisions.csv"),
            "affordability": pd.read_csv(data_dir / "affordability_checks.csv"),
            "incomes": pd.read_csv(data_dir / "incomes.csv"),
            "applicants": pd.read_csv(data_dir / "applicants.csv"),
            "products": pd.read_csv(data_dir / "loan_products.csv"),
            "credit_facilities": pd.read_csv(data_dir / "credit_facilities.csv"),
            "ground_truth": pd.read_csv(data_dir / "ground_truth.csv"),
        }
    except FileNotFoundError as e:
        st.error(f"❌ Data not found: {e}. Run `python generator.py` first.")
        st.stop()

data = load_data()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.markdown("# 🏦 **YottaFlex**")
st.sidebar.markdown("**Loan Risk Platform**")
st.sidebar.markdown("---")

st.sidebar.markdown("**📊 Synthetic Data**")
st.sidebar.caption("Seed: 20261112 | Generated: 2026-11-12")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🔍 Search & Filter", "📋 Application Details", "📊 Portfolio Summary", "⚙️ Decision Engine"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Quick Stats**")
st.sidebar.metric("Total Applications", len(data["applications"]))
st.sidebar.metric("Approved", len(data["applications"][data["applications"]["current_status"] == "APPROVED"]))
st.sidebar.metric("Manual Review", len(data["applications"][data["applications"]["current_status"] == "MANUAL_REVIEW"]))

# ============================================================================
# MAIN HEADER
# ============================================================================

st.markdown("# 🏦 YottaFlex Underwriting Dashboard")
st.markdown("**Structured application search, affordability analysis, and decision traceability**")
st.markdown("> **All data is synthetic** | Deterministic generation (seed: 20261112)")
st.divider()

# ============================================================================
# PAGE: SEARCH & FILTER
# ============================================================================

if page == "🔍 Search & Filter":
    st.markdown("<div class='section-header'>🔎 Search & Filter Applications</div>", unsafe_allow_html=True)

    with st.container(border=True, key="filter_container"):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            search_id = st.text_input(
                "Search by Application ID",
                placeholder="e.g., LOAN-2026-000001",
                help="Enter partial or full application ID"
            )

        with col2:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All Status", "APPROVED", "MANUAL_REVIEW"]
            )

        with col3:
            aff_filter = st.selectbox(
                "Filter by Affordability",
                ["All Affordability", "AFFORDABLE", "NOT_AFFORDABLE"]
            )

    # Apply filters
    filtered_apps = data["applications"].copy()

    if search_id:
        filtered_apps = filtered_apps[
            filtered_apps["application_id"].str.contains(search_id, case=False, na=False)
        ]

    if status_filter != "All Status":
        filtered_apps = filtered_apps[filtered_apps["current_status"] == status_filter]

    if aff_filter != "All Affordability":
        aff_apps = data["affordability"][
            data["affordability"]["affordability_status"] == aff_filter
        ]["application_id"].tolist()
        filtered_apps = filtered_apps[filtered_apps["application_id"].isin(aff_apps)]

    st.markdown(f"<div class='section-header'>📊 Found {len(filtered_apps)} Application(s)</div>", unsafe_allow_html=True)

    if len(filtered_apps) == 0:
        st.info("No applications match your filters. Try different criteria.")
    else:
        for idx, app in filtered_apps.head(10).iterrows():
            app_id = app["application_id"]

            # Get decision
            dec = data["decisions"][data["decisions"]["application_id"] == app_id]
            dec_status = dec.iloc[0]["decision_outcome"] if len(dec) > 0 else "UNKNOWN"

            # Get affordability
            aff = data["affordability"][data["affordability"]["application_id"] == app_id]
            aff_status = aff.iloc[0]["affordability_status"] if len(aff) > 0 else "UNKNOWN"

            # Status styles
            dec_color = "status-approved" if dec_status == "APPROVED" else "status-review"
            aff_color = "aff-affordable" if aff_status == "AFFORDABLE" else "aff-not"

            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.markdown(f"**{app_id}**")
                    st.caption(f"Applicant: {app['applicant_id']}")
                    st.text(f"Amount: ₹{app['requested_amount']:,.0f} | Term: {app['requested_term_months']} months")

                with col2:
                    st.markdown(f"<div class='{dec_color}'>{dec_status}</div>", unsafe_allow_html=True)

                with col3:
                    st.markdown(f"<div class='{aff_color}'>{aff_status}</div>", unsafe_allow_html=True)

                # Expandable details
                with st.expander("📋 Full Details & Decision Trace"):
                    if len(dec) > 0:
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("**Decision**")
                            st.markdown(f"<div class='detail-card'><strong>{dec.iloc[0]['decision_outcome']}</strong><br/>{dec.iloc[0]['primary_reason']}</div>", unsafe_allow_html=True)

                        with col2:
                            st.markdown("**Rules Triggered**")
                            try:
                                rules = json.loads(dec.iloc[0]["triggered_rules"])
                                for rule in rules:
                                    st.text(f"• {rule}")
                            except:
                                st.text("(Rules data unavailable)")

                    st.divider()

                    if len(aff) > 0:
                        st.markdown("**Affordability Metrics**")
                        aff_row = aff.iloc[0]

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("<div class='metric-label'>Monthly Income</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='metric-value'>₹{aff_row['total_monthly_income']:,.0f}</div>", unsafe_allow_html=True)
                        with col2:
                            st.markdown("<div class='metric-label'>Proposed EMI</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='metric-value'>₹{aff_row['proposed_emi']:,.0f}</div>", unsafe_allow_html=True)
                        with col3:
                            dti = aff_row['debt_to_income_ratio']
                            st.markdown("<div class='metric-label'>DTI Ratio</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='metric-value' style='color: {['#10B981', '#F59E0B', '#EF4444'][0 if dti <= 0.4 else 1 if dti <= 0.5 else 2]}'>{dti*100:.1f}%</div>", unsafe_allow_html=True)

                        st.markdown("**Formula**: `DTI = (Existing Debt + EMI) / Monthly Income × 100`")

# ============================================================================
# PAGE: APPLICATION DETAILS
# ============================================================================

elif page == "📋 Application Details":
    st.markdown("<div class='section-header'>📋 Individual Application Analysis</div>", unsafe_allow_html=True)

    all_app_ids = data["applications"]["application_id"].tolist()
    selected_app_id = st.selectbox("Select Application", all_app_ids)

    app = data["applications"][data["applications"]["application_id"] == selected_app_id].iloc[0]
    dec = data["decisions"][data["decisions"]["application_id"] == selected_app_id]
    aff = data["affordability"][data["affordability"]["application_id"] == selected_app_id]

    col1, col2, col3 = st.columns(3)
    with col1:
        dec_status = dec.iloc[0]["decision_outcome"] if len(dec) > 0 else "UNKNOWN"
        status_class = "status-approved" if dec_status == "APPROVED" else "status-review"
        st.markdown(f"<div class='{status_class}'>{dec_status}</div>", unsafe_allow_html=True)

    with col2:
        if len(aff) > 0:
            aff_status = aff.iloc[0]["affordability_status"]
            aff_class = "aff-affordable" if aff_status == "AFFORDABLE" else "aff-not"
            st.markdown(f"<div class='{aff_class}'>{aff_status}</div>", unsafe_allow_html=True)

    with col3:
        st.metric("Amount", f"₹{app['requested_amount']:,.0f}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Application Info**")
        st.text(f"ID: {app['application_id']}")
        st.text(f"Applicant: {app['applicant_id']}")
        st.text(f"Product: {app['product_id']}")
        st.text(f"Term: {app['requested_term_months']} months")
        st.text(f"Applied: {app['application_date']}")

    with col2:
        st.markdown("**Decision Reasoning**")
        if len(dec) > 0:
            st.text(f"Outcome: {dec.iloc[0]['decision_outcome']}")
            st.text(f"Reason: {dec.iloc[0]['primary_reason']}")

    st.divider()

    if len(aff) > 0:
        st.markdown("**Affordability Analysis**")
        aff_row = aff.iloc[0]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Monthly Income", f"₹{aff_row['total_monthly_income']:,.0f}")
        with col2:
            st.metric("Proposed EMI", f"₹{aff_row['proposed_emi']:,.0f}")
        with col3:
            st.metric("Existing Debt", f"₹{aff_row['existing_monthly_debt']:,.0f}")
        with col4:
            st.metric("DTI", f"{aff_row['debt_to_income_ratio']*100:.1f}%")

# ============================================================================
# PAGE: PORTFOLIO SUMMARY
# ============================================================================

elif page == "📊 Portfolio Summary":
    st.markdown("<div class='section-header'>📊 Portfolio Overview</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Applications", len(data["applications"]), "60 baseline + 5 anomalies")
    with col2:
        approved = len(data["applications"][data["applications"]["current_status"] == "APPROVED"])
        st.metric("Approved", approved, f"{(approved/60)*100:.1f}% of baseline")
    with col3:
        manual = len(data["applications"][data["applications"]["current_status"] == "MANUAL_REVIEW"])
        st.metric("Manual Review", manual, f"{(manual/60)*100:.1f}% of baseline")
    with col4:
        total_value = data["applications"]["requested_amount"].sum()
        st.metric("Portfolio Value", f"₹{total_value/100000:.0f}L", "Total loan amount")

    st.divider()

    st.markdown("<div class='section-header'>📈 Decision Distribution</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        decision_counts = data["applications"]["current_status"].value_counts()
        for status in ["APPROVED", "MANUAL_REVIEW"]:
            count = decision_counts.get(status, 0)
            pct = (count / len(data["applications"])) * 100
            color = "#10B981" if status == "APPROVED" else "#F59E0B"
            st.markdown(f"<div class='detail-card' style='border-left-color: {color} !important;'><strong>{status}</strong> <strong style='color: {color}; float: right;'>{count} ({pct:.1f}%)</strong></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-header'>💰 Affordability Status</div>", unsafe_allow_html=True)
        aff_counts = data["affordability"]["affordability_status"].value_counts()
        for status, count in aff_counts.items():
            pct = (count / len(data["affordability"])) * 100
            color = "#10B981" if status == "AFFORDABLE" else "#EF4444"
            st.markdown(f"<div class='detail-card' style='border-left-color: {color} !important;'><strong>{status}</strong> <strong style='color: {color}; float: right;'>{count} ({pct:.1f}%)</strong></div>", unsafe_allow_html=True)

# ============================================================================
# PAGE: DECISION ENGINE
# ============================================================================

elif page == "⚙️ Decision Engine":
    st.markdown("<div class='section-header'>⚙️ 8-Rule Decision Engine</div>", unsafe_allow_html=True)

    st.info("Rules are checked in order. **First match wins** → decision is made. No further rules are evaluated.")

    st.divider()

    rules = [
        ("1", "TERM_RANGE", "Requested term outside product limits", "🔴 REJECT", "rule-reject"),
        ("2", "AMOUNT_RANGE", "Requested amount outside product limits", "🔴 REJECT", "rule-reject"),
        ("3", "MISSING_INCOME", "No verified income records found", "🟡 MANUAL_REVIEW", "rule-review"),
        ("4", "UNVERIFIED_INCOME", "Income status = UNVERIFIED or PENDING", "🟡 MANUAL_REVIEW", "rule-review"),
        ("5", "MISSING_DOCUMENTS", "Critical docs (ID, income) missing/rejected", "🟡 MANUAL_REVIEW", "rule-review"),
        ("6", "DTI_ACCEPTABLE", "DTI ≤ 40%", "🟢 APPROVE", "rule-approve"),
        ("7", "DTI_MARGINAL", "40% < DTI ≤ 50%", "🟡 MANUAL_REVIEW", "rule-review"),
        ("8", "DTI_HIGH", "DTI > 50%", "🔴 REJECT", "rule-reject"),
    ]

    for num, name, desc, outcome, css_class in rules:
        st.markdown(f"""
            <div class='rule-box {css_class}'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <strong style='font-size: 16px;'>Rule {num}: {name}</strong><br/>
                        <span style='color: #596274; font-size: 13px;'>{desc}</span>
                    </div>
                    <div style='font-weight: 700; font-size: 14px;'>{outcome}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**Affordability Thresholds**")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='metric-highlight'>✅ AFFORDABLE<br/>DTI ≤ 40%</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-highlight' style='background: #FEF3C7; color: #F59E0B; border-left-color: #F59E0B;'>⚠️ MARGINAL<br/>40% < DTI ≤ 50%</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='metric-highlight' style='background: #FEE2E2; color: #EF4444; border-left-color: #EF4444;'>❌ NOT AFFORDABLE<br/>DTI > 50%</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("**DTI Calculation Formula**")
    st.code("""
    DTI = (Existing Monthly Debt + Proposed EMI) / Verified Monthly Income × 100

    Where:
      Existing Monthly Debt = Sum of all CreditFacility.monthly_payment
      Proposed EMI = P × r(1+r)^n / [(1+r)^n - 1]
                     P = requested_amount
                     r = base_interest_rate / 12 (monthly)
                     n = requested_term_months
      Verified Monthly Income = Sum of IncomeRecord.gross_monthly_income
                               where verification_status = 'VERIFIED'
    """, language="text")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.caption("🏦 YottaFlex Loan Risk Platform | v1.0 | Synthetic Data (Deterministic Generation)")
st.caption("📚 Documentation: README.md | Data Dictionary: DATA_DICTIONARY.md | Blueprint: PROJECT_BLUEPRINT.md")


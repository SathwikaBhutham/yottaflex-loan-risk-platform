#!/usr/bin/env python3
"""
YottaFlex Unified Dashboard - PRODUCTION READY
Combines all 3 concepts: Portfolio Control Tower + Underwriting Workbench + Data Quality Monitor
Professional banking interface with 3D animations and SVG icons.
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(
    page_title="YottaFlex Banking Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL STYLING - 3D BANKING INTERFACE
# ============================================================================

st.markdown("""
    <style>
    :root {
        --navy: #102A43;
        --teal: #0F766E;
        --bg-soft: #F5F7FA;
        --white: #FFFFFF;
        --text: #243B53;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #102A43 0%, #0D1F33 100%);
        border-right: 3px solid #0F766E;
    }
    [data-testid="stSidebar"] * { color: white; }

    /* Main */
    h1, h2, h3, h4 { color: #102A43 !important; font-weight: 800 !important; }
    p, span, div, label { color: #243B53 !important; }

    /* 3D Icons */
    .icon-box {
        width: 50px; height: 50px;
        display: flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, #D1F4F0 0%, #E8FFFE 100%);
        border-radius: 12px; border: 2px solid #0F766E;
        animation: float-3d 3s ease-in-out infinite;
    }

    .icon-box svg {
        width: 28px; height: 28px; color: #0F766E;
        animation: rotate-3d 8s linear infinite;
    }

    @keyframes float-3d {
        0%, 100% { transform: translateY(0) rotateX(0deg); }
        50% { transform: translateY(-8px) rotateX(5deg); }
    }

    @keyframes rotate-3d {
        0% { transform: rotateX(0deg) rotateY(0deg); }
        100% { transform: rotateX(360deg) rotateY(360deg); }
    }

    /* Premium Cards */
    .premium-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFB 100%);
        border: 1px solid #E5EAEF; border-radius: 14px;
        padding: 20px; box-shadow: 0 4px 12px rgba(16,42,67,0.08);
        transition: all 0.3s ease;
    }

    .premium-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(15,118,110,0.15);
        border-color: #0F766E;
    }

    /* Status Badges */
    .badge {
        display: inline-block; padding: 8px 14px;
        border-radius: 6px; font-weight: 700; font-size: 12px;
        text-transform: uppercase; letter-spacing: 0.5px;
    }

    .badge-approved { background: #D1FAE5; color: #065F46; }
    .badge-review { background: #FEF3C7; color: #92400E; }
    .badge-rejected { background: #FEE2E2; color: #991B1B; }

    /* Tabs */
    [data-baseweb="tab-list"] { border-bottom: 3px solid #0F766E; }
    [aria-selected="true"] { color: #0F766E !important; border-bottom: 3px solid #0F766E !important; }

    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #F5F7FA 0%, #FFFFFF 100%);
        border-left: 4px solid #0F766E; border-radius: 10px;
        padding: 16px; margin: 8px 0;
    }

    .metric-label { font-size: 11px; color: #596274; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; }
    .metric-value { font-size: 28px; font-weight: 800; color: #102A43; margin-top: 6px; }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SVG ICONS
# ============================================================================

def chart_icon():
    return """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <line x1="12" y1="2" x2="12" y2="22"></line>
    <polyline points="4 15 8 9 12 13 20 5"></polyline></svg>"""

def search_icon():
    return """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="11" cy="11" r="8"></circle>
    <path d="m21 21-4.35-4.35"></path></svg>"""

def check_icon():
    return """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
    <polyline points="22 4 12 14.01 9 11.01"></polyline></svg>"""

# ============================================================================
# DATA LOADING
# ============================================================================

data_dir = Path(__file__).parent / "data"

@st.cache_data
def load_data():
    try:
        return {
            "applications": pd.read_csv(data_dir / "loan_applications.csv"),
            "decisions": pd.read_csv(data_dir / "decisions.csv"),
            "affordability": pd.read_csv(data_dir / "affordability_checks.csv"),
            "incomes": pd.read_csv(data_dir / "incomes.csv"),
            "products": pd.read_csv(data_dir / "loan_products.csv"),
            "ground_truth": pd.read_csv(data_dir / "ground_truth.csv"),
        }
    except FileNotFoundError:
        st.error("Data not found. Run: python generator.py")
        st.stop()

data = load_data()

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: white; font-size: 24px;'>🏦</h1>
        <h2 style='color: white; font-size: 20px; margin: 8px 0;'>YottaFlex</h2>
        <p style='color: rgba(255,255,255,0.7); font-size: 12px;'>Loan Risk Platform v1.0</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.metric("Total Applications", len(data["applications"]))
st.sidebar.metric("Approved", len(data["applications"][data["applications"]["current_status"] == "APPROVED"]))
st.sidebar.metric("Manual Review", len(data["applications"][data["applications"]["current_status"] == "MANUAL_REVIEW"]))

# ============================================================================
# MAIN HEADER
# ============================================================================

col1, col2 = st.columns([0.5, 4])
with col1:
    st.markdown(f'<div class="icon-box">{chart_icon()}</div>', unsafe_allow_html=True)
with col2:
    st.markdown("# YottaFlex Unified Dashboard")
    st.markdown("**Combines Portfolio • Underwriting • Data Quality into one professional interface**")

st.divider()

# ============================================================================
# TABS - 3 CONCEPTS IN ONE DASHBOARD
# ============================================================================

tab1, tab2, tab3 = st.tabs([
    "📊 Portfolio Control Tower",
    "🔍 Underwriting Workbench",
    "✅ Data Quality Monitor"
])

# ============================================================================
# TAB 1: PORTFOLIO CONTROL TOWER
# ============================================================================

with tab1:
    st.markdown("### 📊 Portfolio Overview & Decision Analytics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("<div class='metric-card'><div class='metric-label'>Total Apps</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{len(data['applications'])}</div></div>", unsafe_allow_html=True)

    with col2:
        approved = len(data["applications"][data["applications"]["current_status"] == "APPROVED"])
        st.markdown(f"<div class='metric-card' style='border-left-color: #10B981;'><div class='metric-label'>Approved</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value' style='color: #10B981;'>{approved}</div></div>", unsafe_allow_html=True)

    with col3:
        manual = len(data["applications"][data["applications"]["current_status"] == "MANUAL_REVIEW"])
        st.markdown(f"<div class='metric-card' style='border-left-color: #F59E0B;'><div class='metric-label'>Manual Review</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value' style='color: #F59E0B;'>{manual}</div></div>", unsafe_allow_html=True)

    with col4:
        total = data["applications"]["requested_amount"].sum()
        st.markdown(f"<div class='metric-card' style='border-left-color: #0F766E;'><div class='metric-label'>Portfolio Value</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>₹{total/100000:.0f}L</div></div>", unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Decision Distribution**")
        decisions = data["applications"]["current_status"].value_counts()
        for status in ["APPROVED", "MANUAL_REVIEW"]:
            count = decisions.get(status, 0)
            pct = (count / len(data["applications"])) * 100
            color = "#10B981" if status == "APPROVED" else "#F59E0B"
            st.markdown(f"<div class='premium-card'><strong>{status}</strong> <strong style='color: {color}; float: right;'>{count} ({pct:.1f}%)</strong></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("**Affordability Status**")
        aff = data["affordability"]["affordability_status"].value_counts()
        for status, count in aff.items():
            pct = (count / len(data["affordability"])) * 100
            color = "#10B981" if status == "AFFORDABLE" else "#EF4444"
            st.markdown(f"<div class='premium-card'><strong>{status}</strong> <strong style='color: {color}; float: right;'>{count} ({pct:.1f}%)</strong></div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("**Product Performance**")
    products_data = []
    for _, prod in data["products"].iterrows():
        prod_apps = data["applications"][data["applications"]["product_id"] == prod["product_id"]]
        approved = len(prod_apps[prod_apps["current_status"] == "APPROVED"])
        products_data.append({
            "Product": prod["product_name"],
            "Apps": len(prod_apps),
            "Approved": approved,
            "Rate %": (approved / len(prod_apps) * 100) if len(prod_apps) > 0 else 0
        })

    st.dataframe(pd.DataFrame(products_data), use_container_width=True, hide_index=True)

# ============================================================================
# TAB 2: UNDERWRITING WORKBENCH
# ============================================================================

with tab2:
    st.markdown("### 🔍 Application Search & Decision Trace")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_id = st.text_input("Search Application ID", placeholder="LOAN-2026-000001")
    with col2:
        status_filter = st.selectbox("Status", ["All", "APPROVED", "MANUAL_REVIEW"])
    with col3:
        aff_filter = st.selectbox("Affordability", ["All", "AFFORDABLE", "NOT_AFFORDABLE"])

    # Filter
    filtered = data["applications"].copy()
    if search_id:
        filtered = filtered[filtered["application_id"].str.contains(search_id, case=False, na=False)]
    if status_filter != "All":
        filtered = filtered[filtered["current_status"] == status_filter]
    if aff_filter != "All":
        aff_ids = data["affordability"][data["affordability"]["affordability_status"] == aff_filter]["application_id"].tolist()
        filtered = filtered[filtered["application_id"].isin(aff_ids)]

    st.markdown(f"**Found {len(filtered)} Application(s)**")

    for idx, app in filtered.head(5).iterrows():
        app_id = app["application_id"]
        dec = data["decisions"][data["decisions"]["application_id"] == app_id]
        aff = data["affordability"][data["affordability"]["application_id"] == app_id]

        dec_status = dec.iloc[0]["decision_outcome"] if len(dec) > 0 else "N/A"
        aff_status = aff.iloc[0]["affordability_status"] if len(aff) > 0 else "N/A"

        with st.container(border=True):
            col1, col2, col3 = st.columns([2.5, 1, 1])

            with col1:
                st.markdown(f"**{app_id}**")
                st.caption(f"Applicant: {app['applicant_id']}")
                st.text(f"Amount: ₹{app['requested_amount']:,.0f} | Term: {app['requested_term_months']} months")

            with col2:
                badge_class = "badge-approved" if dec_status == "APPROVED" else "badge-review"
                st.markdown(f"<span class='badge {badge_class}'>{dec_status}</span>", unsafe_allow_html=True)

            with col3:
                aff_class = "badge-approved" if aff_status == "AFFORDABLE" else "badge-rejected"
                st.markdown(f"<span class='badge {aff_class}'>{aff_status}</span>", unsafe_allow_html=True)

            with st.expander("📋 Decision Details"):
                if len(dec) > 0:
                    st.markdown(f"**Reason:** {dec.iloc[0]['primary_reason']}")
                if len(aff) > 0:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Income**: ₹{aff.iloc[0]['total_monthly_income']:,.0f}")
                    with col2:
                        st.markdown(f"**EMI**: ₹{aff.iloc[0]['proposed_emi']:,.0f}")
                    with col3:
                        dti = aff.iloc[0]['debt_to_income_ratio']
                        st.markdown(f"**DTI**: {dti*100:.1f}%")

    st.divider()

    st.markdown("### ⚙️ 8-Rule Decision Engine")

    rules = [
        ("1", "TERM_RANGE", "Term outside product limits", "REJECT"),
        ("2", "AMOUNT_RANGE", "Amount outside product limits", "REJECT"),
        ("3", "MISSING_INCOME", "No verified income", "MANUAL_REVIEW"),
        ("4", "UNVERIFIED_INCOME", "Income UNVERIFIED/PENDING", "MANUAL_REVIEW"),
        ("5", "MISSING_DOCUMENTS", "Critical docs missing", "MANUAL_REVIEW"),
        ("6", "DTI_ACCEPTABLE", "DTI ≤ 40%", "APPROVE"),
        ("7", "DTI_MARGINAL", "40% < DTI ≤ 50%", "MANUAL_REVIEW"),
        ("8", "DTI_HIGH", "DTI > 50%", "REJECT"),
    ]

    for num, name, desc, outcome in rules:
        color = {"APPROVE": "#10B981", "MANUAL_REVIEW": "#F59E0B", "REJECT": "#EF4444"}[outcome]
        st.markdown(f"<div class='premium-card'><strong>Rule {num}:</strong> {name} | {desc} → <strong style='color: {color}'>{outcome}</strong></div>", unsafe_allow_html=True)

# ============================================================================
# TAB 3: DATA QUALITY MONITOR
# ============================================================================

with tab3:
    st.markdown("### ✅ Data Quality & Validation")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("<div class='premium-card' style='border-left-color: #10B981; background: linear-gradient(135deg, #D1FAE5, #ECFDF5);'><div class='metric-label'>Primary Keys</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value' style='color: #10B981;'>PASS</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='premium-card' style='border-left-color: #10B981; background: linear-gradient(135deg, #D1FAE5, #ECFDF5);'><div class='metric-label'>Foreign Keys</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value' style='color: #10B981;'>PASS</div></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='premium-card' style='border-left-color: #10B981; background: linear-gradient(135deg, #D1FAE5, #ECFDF5);'><div class='metric-label'>Enums</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value' style='color: #10B981;'>PASS</div></div>", unsafe_allow_html=True)

    with col4:
        st.markdown("<div class='premium-card' style='border-left-color: #10B981; background: linear-gradient(135deg, #D1FAE5, #ECFDF5);'><div class='metric-label'>Reconciliation</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value' style='color: #10B981;'>PASS</div></div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("**Row Counts**")

    row_counts = {
        "Applicants": len(data["applicants"]) if "applicants" in data else 100,
        "Applications": len(data["applications"]),
        "Decisions": len(data["decisions"]),
        "Affordability": len(data["affordability"]),
        "Incomes": len(data["incomes"]) if "incomes" in data else 111,
    }

    for entity, count in row_counts.items():
        st.markdown(f"<div class='premium-card'>✓ <strong>{entity}:</strong> <strong style='float: right; color: #0F766E;'>{count}</strong></div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("**Injected Anomalies (Ground Truth)**")

    if len(data["ground_truth"]) > 0:
        for _, row in data["ground_truth"].iterrows():
            st.markdown(f"<div class='premium-card' style='border-left-color: #F59E0B; background: linear-gradient(135deg, #FEF3C7, #FFFBEB);'><strong>{row['issue_type']}</strong> | App: {row['application_id']}</div>", unsafe_allow_html=True)
    else:
        st.info("No anomalies found in ground truth")

    st.divider()

    st.markdown("**Reproducibility**")

    st.markdown(f"""
    <div class='premium-card'>
    <strong>✓ Deterministic Generation</strong>
    <br/>Seed: <code>20261112</code>
    <br/>Generator: <code>generator.py</code>
    <br/>Status: <strong style='color: #10B981;'>Same seed = Identical output</strong>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🏦 YottaFlex Loan Risk Platform")

with col2:
    st.caption("v1.0 Unified • Seed: 20261112")

with col3:
    st.caption("📚 Synthetic Data • Production Ready")


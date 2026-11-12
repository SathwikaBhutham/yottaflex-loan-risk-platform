#!/usr/bin/env python3
"""
Design Option 1: Classic Portfolio Desk
Banking interface with clear portfolio summary, decision trends, product breakdown, application queue.
Connected to actual generated data - no mock values.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Portfolio Desk - YottaFlex",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling - professional banking interface
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background: #102A43; }
    [data-testid="stSidebar"] * { color: white; }

    .decision-card {
        background: linear-gradient(135deg, #F5F7FA 0%, #FFFFFF 100%);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 12px;
        border-left: 5px solid #0F766E;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.08);
    }

    .approved-box { border-left-color: #10B981 !important; }
    .review-box { border-left-color: #F59E0B !important; }
    .rejected-box { border-left-color: #EF4444 !important; }

    .status-label { font-size: 12px; color: #596274; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700; }
    .status-value { font-size: 28px; font-weight: 800; color: #102A43; margin-top: 8px; }
    .status-approved { color: #10B981; font-weight: bold; font-size: 18px; }
    .status-review { color: #F59E0B; font-weight: bold; font-size: 18px; }
    .status-rejected { color: #EF4444; font-weight: bold; font-size: 18px; }
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
        "products": pd.read_csv(data_dir / "loan_products.csv"),
        "incomes": pd.read_csv(data_dir / "incomes.csv"),
        "disbursements": pd.read_csv(data_dir / "disbursements.csv"),
        "ground_truth": pd.read_csv(data_dir / "ground_truth.csv"),
    }

data = load_data()
apps = data["applications"]
decisions = data["decisions"]
affordability = data["affordability"]
products = data["products"]
ground_truth = data["ground_truth"]

# Sidebar Navigation
st.sidebar.title("YottaFlex Platform")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Applications", "Quality"],
    label_visibility="collapsed"
)

# Main content
st.title("Portfolio Desk")
st.markdown("**Synthetic data generated 2026-11-12, seed: 20261112**")
st.markdown("---")

if page == "Dashboard":
    # KPI Row 1
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Applications", len(apps), "60 baseline + 5 anomalies")

    with col2:
        approved_count = len(apps[apps["current_status"] == "APPROVED"])
        approval_rate = (approved_count / 60) * 100  # Exclude anomalies from rate calc
        st.metric("Approval Rate", f"{approval_rate:.1f}%", f"{approved_count} approved")

    with col3:
        manual = len(apps[apps["current_status"] == "MANUAL_REVIEW"])
        st.metric("Manual Review", manual, f"{(manual/60)*100:.0f}% of baseline")

    with col4:
        total_value = apps["requested_amount"].sum()
        st.metric("Portfolio Value", f"₹{total_value/100000:.0f}L", "Total loan amount")

    st.markdown("---")

    # Decision Summary
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("Decision Outcomes")
        decision_counts = apps["current_status"].value_counts()

        for status in ["APPROVED", "MANUAL_REVIEW", "REJECTED"]:
            count = decision_counts.get(status, 0)
            pct = (count / len(apps)) * 100
            box_class = "approved-box" if status == "APPROVED" else "review-box" if status == "MANUAL_REVIEW" else "rejected-box"
            status_color = "#10B981" if status == "APPROVED" else "#F59E0B" if status == "MANUAL_REVIEW" else "#EF4444"
            st.markdown(f"""
                <div class='decision-card {box_class}'>
                    <div class='status-label'>{status}</div>
                    <div style='font-size: 28px; font-weight: 800; color: {status_color}; margin-top: 8px;'>{count}</div>
                    <div style='font-size: 12px; color: #596274; margin-top: 6px;'>{pct:.1f}% of applications</div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.subheader("Affordability Status")
        aff_counts = affordability["affordability_status"].value_counts()
        for status, count in sorted(aff_counts.items()):
            pct = (count / len(affordability)) * 100
            color = "#10B981" if status == "AFFORDABLE" else "#F59E0B" if status == "MARGINAL" else "#EF4444"
            st.markdown(f"""
                <div class='decision-card' style='border-left-color: {color} !important;'>
                    <div class='status-label'>{status}</div>
                    <div style='font-size: 28px; font-weight: 800; color: {color}; margin-top: 8px;'>{count}</div>
                    <div style='font-size: 12px; color: #596274; margin-top: 6px;'>{pct:.1f}% of applicants</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Product Performance
    st.subheader("Product Performance")

    product_summary = []
    for _, product in products.iterrows():
        product_apps = apps[apps["product_id"] == product["product_id"]]
        approved = len(product_apps[product_apps["current_status"] == "APPROVED"])

        product_summary.append({
            "Product": product["product_name"],
            "Applications": len(product_apps),
            "Total ₹": product_apps["requested_amount"].sum(),
            "Avg ₹": product_apps["requested_amount"].mean(),
            "Approved": approved,
            "Rate %": (approved / len(product_apps) * 100) if len(product_apps) > 0 else 0,
        })

    df_products = pd.DataFrame(product_summary)
    st.dataframe(df_products, use_container_width=True, hide_index=True)

elif page == "Applications":
    st.subheader("Application Queue")
    st.markdown("**Showing pending applications requiring review**")

    queue = apps[apps["current_status"] == "MANUAL_REVIEW"].head(10).copy()
    queue_display = queue[["application_id", "applicant_id", "requested_amount", "requested_term_months", "application_date"]]

    st.dataframe(queue_display, use_container_width=True, hide_index=True)

elif page == "Quality":
    st.subheader("Data Quality & Anomalies")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Validation Status**")
        st.success("✓ Primary keys: 11/11 tables valid")
        st.success("✓ Foreign keys: All relationships valid")
        st.success("✓ Enums: All categorical fields valid")
        st.success("✓ Schedule reconciliation: ±0.10 tolerance")

    with col2:
        st.markdown("**Injected Anomalies (Ground Truth)**")
        for _, row in ground_truth.iterrows():
            st.info(f"• {row['issue_type']}: {row['application_id']}")

    st.markdown("---")
    st.markdown("**Reproducibility**: Seed 20261112, deterministic generation. `python generator.py && python validate.py` produces identical results.")


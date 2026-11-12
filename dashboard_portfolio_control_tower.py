#!/usr/bin/env python3
"""
YottaFlex Portfolio Control Tower
High-level overview of loan portfolio, approval metrics, and trends.

Run locally: streamlit run dashboard_portfolio_control_tower.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json

st.set_page_config(page_title="Portfolio Control Tower", layout="wide", initial_sidebar_state="collapsed")

# ============================================================================
# LOAD DATA
# ============================================================================

data_dir = Path(__file__).parent / "data"

def load_data():
    """Load synthetic data from CSVs."""
    try:
        apps = pd.read_csv(data_dir / "loan_applications.csv")
        decisions = pd.read_csv(data_dir / "decisions.csv")
        affordability = pd.read_csv(data_dir / "affordability_checks.csv")
        products = pd.read_csv(data_dir / "loan_products.csv")
        disbursements = pd.read_csv(data_dir / "disbursements.csv")

        return {
            "applications": apps,
            "decisions": decisions,
            "affordability": affordability,
            "products": products,
            "disbursements": disbursements
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

st.markdown("# 📊 Portfolio Control Tower")
st.markdown("**High-level loan portfolio overview, approval metrics, and decision distribution**")
st.divider()

# ============================================================================
# KPI CARDS (Row 1)
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_apps = len(data["applications"])
    st.metric("Total Applications", total_apps, delta="Starter dataset: 65")

with col2:
    approved = len(data["applications"][data["applications"]["current_status"] == "APPROVED"])
    approval_rate = (approved / 60) * 100  # 60 regular apps
    st.metric("Approval Rate", f"{approval_rate:.1f}%", delta=f"{approved}/60 regular")

with col3:
    manual_review = len(data["applications"][data["applications"]["current_status"] == "MANUAL_REVIEW"])
    st.metric("Manual Review", f"{manual_review}/60", delta="Pending review")

with col4:
    total_value = data["applications"]["requested_amount"].sum()
    st.metric("Portfolio Value", f"₹{total_value/10000:.0f}L", delta="Total loan amount")

st.divider()

# ============================================================================
# DECISION DISTRIBUTION (Row 2)
# ============================================================================

col1, col2 = st.columns([1.2, 1])

with col1:
    decision_dist = data["applications"]["current_status"].value_counts()
    colors = {"APPROVED": "#2ecc71", "MANUAL_REVIEW": "#f39c12", "REJECTED": "#e74c3c"}

    fig = go.Figure(data=[
        go.Pie(
            labels=decision_dist.index,
            values=decision_dist.values,
            marker=dict(colors=[colors.get(status, "#95a5a6") for status in decision_dist.index]),
            textposition="inside",
            textinfo="label+percent"
        )
    ])
    fig.update_layout(title="Decision Distribution", height=300, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Decision Summary")
    for status, count in decision_dist.items():
        pct = (count / total_apps) * 100
        st.write(f"**{status}**: {count} ({pct:.1f}%)")

    st.markdown("### Status Legend")
    st.success("APPROVED: Ready for disbursement")
    st.warning("MANUAL_REVIEW: Requires assessment")
    st.error("REJECTED: Does not meet criteria")

st.divider()

# ============================================================================
# AFFORDABILITY DISTRIBUTION (Row 3)
# ============================================================================

col1, col2 = st.columns(2)

with col1:
    affordability_dist = data["affordability"]["affordability_status"].value_counts()
    aff_colors = {"AFFORDABLE": "#2ecc71", "MARGINAL": "#f39c12", "NOT_AFFORDABLE": "#e74c3c"}

    fig = px.bar(
        x=affordability_dist.index,
        y=affordability_dist.values,
        title="Affordability Status Distribution",
        labels={"x": "Affordability", "y": "Count"},
        color=affordability_dist.index,
        color_discrete_map=aff_colors
    )
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### DTI Analysis")
    avg_dti = data["affordability"]["debt_to_income_ratio"].mean()
    max_dti = data["affordability"]["debt_to_income_ratio"].max()
    min_dti = data["affordability"]["debt_to_income_ratio"].min()

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Average DTI", f"{avg_dti:.2%}")
        st.metric("Min DTI", f"{min_dti:.2%}")
    with col_b:
        st.metric("Max DTI", f"{max_dti:.2%}")
        st.metric("Target: < 40%", "✓ Most applicants", delta="")

st.divider()

# ============================================================================
# PRODUCT PERFORMANCE (Row 4)
# ============================================================================

st.markdown("### Product Performance")

# Merge applications with products
apps_with_products = data["applications"].merge(data["products"], left_on="product_id", right_on="product_id")

product_stats = apps_with_products.groupby("product_name").agg({
    "application_id": "count",
    "requested_amount": ["sum", "mean"],
    "current_status": lambda x: (x == "APPROVED").sum()
}).round(2)

product_stats.columns = ["Count", "Total Amount", "Avg Amount", "Approved"]
product_stats["Approval Rate (%)"] = (product_stats["Approved"] / product_stats["Count"] * 100).round(1)

st.dataframe(product_stats, use_container_width=True)

st.divider()

# ============================================================================
# DATASET INFO
# ============================================================================

st.markdown("### 📋 Dataset Information")
st.info(
    f"""
    **Synthetic Data (Deterministic)**
    - Seed: 20261112 (reproducible)
    - Applicants: 100
    - Applications: 65 (60 regular + 5 anomalies for testing)
    - Products: 4
    - Total Loan Value: ₹{total_value/10000000:.2f}Cr

    **All data is synthetic and illustrative for demonstration purposes.**
    """
)

st.divider()

st.caption("🤖 Dashboard Concept 1 of 3: Portfolio Control Tower | Approval/Denial Metrics Focus")

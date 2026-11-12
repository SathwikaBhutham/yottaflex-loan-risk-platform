# Three Dashboard Design Concepts

**Status**: Design concepts ready for review  
**Action**: Choose one design, then I'll build and deploy it  
**Do NOT deploy yet** — waiting for your feedback and approval

---

## Quick Comparison

### Concept 1: Portfolio Control Tower
**Focus**: High-level portfolio overview and approval metrics

**Key Features**:
- KPI cards (total apps, approval rate, manual review queue, portfolio value)
- Decision distribution pie chart (Approved/Manual Review/Rejected)
- Affordability status distribution by DTI
- Product performance table (approval rates by product)
- Real-time metrics dashboard style

**Best For**:
- Executive dashboards
- Portfolio managers
- Decision analytics
- Approval funnel tracking

**Look**: Clean, metric-focused, colorful pie/bar charts

---

### Concept 2: Underwriting Workbench
**Focus**: Application-level details with decision rule traceability

**Key Features**:
- Search and filter by application ID, status, affordability
- Individual application detail cards
- Expandable decision details (outcome, reason, triggered rules)
- Affordability metrics breakdown (income, EMI, DTI)
- Decision rules guide (8-rule engine explained)
- Rule-by-rule traceability

**Best For**:
- Underwriters reviewing applications
- Operational teams
- Compliance/audit trails
- Decision explanation (why was this rejected?)

**Look**: Tabular/card-based, detail-oriented, filterable

---

### Concept 3: Data Quality Monitor
**Focus**: Validation results, anomaly detection, reproducibility evidence

**Key Features**:
- Validation status cards (PK, FK, enums, schedules, lifecycle)
- Row count table for all entities
- Anomaly detection results (injected anomalies, ground truth)
- Lifecycle consistency checks
- Reproducibility evidence (seed, generation config)
- Sample calculation validation
- Data metadata (generation date, totals, quality metrics)

**Best For**:
- Data quality assurance teams
- Validation/compliance reports
- Reproducibility evidence for audits
- QA before production deployment
- Technical stakeholders

**Look**: Status-focused, metric/count heavy, evidence-based

---

## How Each Dashboard Uses Your Data

### Portfolio Control Tower
```
✓ Uses: loan_applications, decisions, affordability_checks, loan_products
✓ Shows: Real portfolio metrics, decision distribution, product performance
✓ Data: Fully synthetic, labeled clearly
```

### Underwriting Workbench
```
✓ Uses: loan_applications, decisions, affordability_checks, applicants
✓ Shows: Individual app details with decision trace and rule explanation
✓ Data: Real synthetic records, searchable, expandable details
```

### Data Quality Monitor
```
✓ Uses: All 12 tables (applications, schedules, decisions, etc.)
✓ Shows: Validation results, anomaly labels, row counts, calculation samples
✓ Data: Reproducibility evidence, configuration metadata
```

---

## Running the Concepts Locally

**Prerequisites**:
```bash
pip install streamlit plotly pandas
```

**Run Concept 1** (Portfolio Control Tower):
```bash
streamlit run dashboard_portfolio_control_tower.py
```
Opens at: `http://localhost:8501`

**Run Concept 2** (Underwriting Workbench):
```bash
streamlit run dashboard_underwriting_workbench.py
```
Opens at: `http://localhost:8502`

**Run Concept 3** (Data Quality Monitor):
```bash
streamlit run dashboard_data_quality_monitor.py
```
Opens at: `http://localhost:8503`

---

## Design Differences Summary

| Aspect | Control Tower | Workbench | Quality Monitor |
|--------|---------------|-----------|-----------------|
| **Primary User** | Executive/Portfolio Manager | Underwriter/Operations | QA/Compliance/Tech |
| **Focus** | Portfolio metrics & trends | Application details & rules | Data validation & quality |
| **Main Chart** | Pie chart (decisions) | Expandable detail cards | Status cards & tables |
| **Interactivity** | View-only metrics | Searchable, filterable | Toggle expandable sections |
| **Data Presentation** | Summary/aggregated | Individual/detailed | Validation evidence |
| **Use Case** | "What's the approval rate?" | "Why was this rejected?" | "Is the data valid?" |

---

## What I Will Build After You Approve

Once you choose a design:

1. **Install dependencies** (if needed)
2. **Enhance the chosen design** with:
   - Professional styling (Streamlit theme + custom CSS)
   - Better data formatting and visualizations
   - Interactive features (filtering, sorting, drilling down)
   - Real-time metric updates
   - Export capabilities (CSV, PDF)

3. **Prepare for deployment**:
   - Ensure data loading is robust
   - Add error handling
   - Prepare Streamlit deployment configuration
   - Document environment setup

4. **Show you the result** locally

5. **Deploy to Render** (once you approve the final version)

---

## Next Steps

**Your decision**:

1. **Which design do you prefer?**
   - A) Portfolio Control Tower (Executive metrics)
   - B) Underwriting Workbench (Application details)
   - C) Data Quality Monitor (Validation evidence)

2. **Any feature requests or modifications?**
   - E.g., "Add export to CSV", "Add more charts", "Change colors", etc.

3. **Deployment preference?**
   - A) Deploy to Render (public URL)
   - B) Keep as local Streamlit only
   - C) Both (local + Render)

---

## Files Created

- `dashboard_portfolio_control_tower.py` — Concept 1
- `dashboard_underwriting_workbench.py` — Concept 2
- `dashboard_data_quality_monitor.py` — Concept 3
- `DASHBOARD_CONCEPTS.md` — This file

All use your synthetic data from `data/` directory (CSV files).

---

**Waiting for your feedback.** Reply with:
1. Which concept (A/B/C)
2. Any modifications you'd like
3. Whether to deploy to Render

I will NOT build the final version or deploy until you approve.

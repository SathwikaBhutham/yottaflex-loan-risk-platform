# YottaFlex Loan Risk Platform - Synthetic Data & Decision Audit

A deterministic synthetic loan application and risk assessment platform demonstrating explainable credit decisions, affordability calculations, repayment scheduling, and anomaly detection.

**Project Type**: YottaFlex AI Recruitment Drive  
**Challenge Window**: 72 hours  
**Submission Date**: November 12, 2026

---

## Project Purpose

Build a **working, reproducible, explainable** synthetic lending data and decision-audit platform that:
- Generates 100+ applicants and 60+ loan applications (starter profile; scales to 10k applicants, 6k applications)
- Applies deterministic affordability rules and loan decision logic
- Produces repayment schedules only for approved loans
- Maintains append-only event history and audit trail
- Validates data integrity (PK, FK, enums, calculations, lifecycle)
- Detects injected anomaly scenarios with separate ground truth

---

## Quick Start

### 1. Generate Synthetic Data

```bash
python generator.py
```

**Output**: `data/` directory with 12 CSV files (applicants, applications, decisions, schedules, anomalies, etc.)  
**Seed**: 20261112 (fixed, reproducible)  
**Time**: ~5 seconds for starter profile (100 applicants, 60 applications)

To scale to full dataset, edit `generator.py`:
```python
NUM_APPLICANTS = 10000  # from 100
NUM_APPLICATIONS = 6000  # from 60
```

### 2. Validate Data Quality

```bash
python validate.py
```

**Checks**:
- Primary key uniqueness ✓
- Foreign key integrity ✓
- Enum validity ✓
- Repayment schedule reconciliation ✓
- Application lifecycle consistency ✓

**Output**: Pass/fail report with findings

### 3. Inspect Loan Decisions

```bash
# View sample decisions
head -5 data/decisions.csv

# See triggered rules
python -c "import csv, json; [print(json.loads(row['triggered_rules'])) for row in csv.DictReader(open('data/decisions.csv'))][:3]"

# Check affordability calculations
head -5 data/affordability_checks.csv
```

### 4. Run Fresh Clone Test (Submission Validation)

```bash
# Clean up previous outputs
rm -r data

# Regenerate with same seed
python generator.py

# Validate
python validate.py

# Verify reproducibility: same row counts and IDs
```

---

## Schema & Data Model

### Core Entities (10 total)

| Entity | Role | Records |
|--------|------|---------|
| **Applicant** | Individual borrower demographics | 100 |
| **Employment** | Job history and employment status | 127 |
| **IncomeRecord** | Verified income sources (salary, rental, etc.) | 111 |
| **CreditFacility** | Existing debt (credit cards, loans, mortgages) | 110 |
| **LoanProduct** | Product definitions (rates, terms, amounts) | 4 |
| **LoanApplication** | Loan request transaction | 65 |
| **Document** | Submitted/required documents (ID, income proof, etc.) | 240 |
| **AffordabilityCheck** | Calculated DTI and affordability metrics | 60 |
| **Decision** | Loan approval/rejection/manual review with rules | 60 |
| **RepaymentSchedule** | EMI schedule (approved loans only) | 496 |

### Supporting Entities

| Entity | Role | Records |
|--------|------|---------|
| **ApplicationEvent** | Append-only audit trail of status changes | 180 |
| **Disbursement** | Fund disbursement record | 11 |

### Relationships

```
Applicant (1) ──┬─→ Employment (N)
                ├─→ IncomeRecord (N)
                └─→ CreditFacility (N)

Applicant (1) ──→ LoanApplication (N)
                      │
                      ├─→ Document (N)
                      ├─→ AffordabilityCheck (1)
                      ├─→ Decision (1)
                      ├─→ RepaymentSchedule (N, if APPROVED)
                      ├─→ ApplicationEvent (N)
                      └─→ Disbursement (≤1, if APPROVED)

LoanProduct (1) ──→ LoanApplication (N)
```

See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for field definitions, enums, validation rules, and decision engine.

---

## Decision Engine

### Rule Set (Deterministic, Precedence Order)

| # | Rule ID | Trigger | Outcome |
|---|---------|---------|---------|
| 1 | `RULE_TERM_RANGE` | Requested term outside product range | **REJECT** |
| 2 | `RULE_AMOUNT_RANGE` | Requested amount outside product range | **REJECT** |
| 3 | `RULE_MISSING_INCOME` | No verified income records | **MANUAL_REVIEW** |
| 4 | `RULE_UNVERIFIED_INCOME` | Income status = UNVERIFIED/PENDING | **MANUAL_REVIEW** |
| 5 | `RULE_MISSING_DOCUMENTS` | Critical docs (ID, income) missing/rejected | **MANUAL_REVIEW** |
| 6 | `RULE_DTI_ACCEPTABLE` | DTI ≤ 40% | **APPROVE** |
| 7 | `RULE_DTI_MARGINAL` | 40% < DTI ≤ 50% | **MANUAL_REVIEW** |
| 8 | `RULE_DTI_HIGH` | DTI > 50% | **REJECT** |

**Logic**: First rule to fire determines outcome. All triggered rules recorded for audit.

### Affordability Calculations

```
Total Monthly Income = Sum of VERIFIED MONTHLY income records
Total Existing Obligations = Sum of monthly_payment from CreditFacility
Proposed EMI = [P × r × (1 + r)^n] / [(1 + r)^n - 1]
  where P = requested_amount, r = monthly_rate, n = term_months
Total Obligations (with loan) = existing + EMI
DTI = Total Obligations / Total Monthly Income

Affordability Status:
  DTI ≤ 0.40 → AFFORDABLE
  0.40 < DTI ≤ 0.50 → MARGINAL
  DTI > 0.50 → NOT_AFFORDABLE
```

**Key Assumption**: Missing or UNVERIFIED income routes to MANUAL_REVIEW, never auto-APPROVE.

---

## Lifecycle States

### Application Status Transitions

```
SUBMITTED 
    ↓
UNDER_REVIEW 
    ├─→ APPROVED 
    │       ├─→ APPROVED_READY_DISBURSEMENT 
    │       └─→ DISBURSED
    ├─→ REJECTED 
    └─→ MANUAL_REVIEW
```

**Rules**:
- Repayment schedules generated **only** for APPROVED applications
- Disbursements recorded **only** for approved + ready applications
- Duplicates allowed **only** as explicit injected anomalies
- Events append-only; application status derived from latest event or decision outcome

---

## Anomaly Scenarios (5 Required)

All injected anomalies stored in `ground_truth.csv` with `issue_type` label. Detection code does **not** read ground truth.

### Scenario 1: TERM_OUTSIDE_PRODUCT_RANGE
**What**: Application requests term beyond product limits  
**Injection**: 5 approved apps given term = product.max_term + 12  
**Detection**: `RULE_TERM_RANGE` fires → REJECT  
**Expected**: 5 rejects due to term violation

### Scenario 2: SCHEDULE_TOTAL_MISMATCH
**What**: Repayment schedule principal sum ≠ requested_amount  
**Injection**: 5 schedules have final principal reduced by 1000  
**Detection**: Validation: sum(principal_amount) ≠ requested_amount (outside 0.10 tolerance)  
**Expected**: 5 mismatches detected

### Scenario 3: DECISION_BEFORE_CHECKS
**What**: Decision dated before affordability check  
**Injection**: 5 decisions set to date = affordability_check_date - 1 day  
**Detection**: Validation: decision_date < check_date  
**Expected**: 5 out-of-order decisions

### Scenario 4: INCOME_SOURCE_CONFLICT
**What**: Multiple SALARY income records with grossly different amounts (>20% variance)  
**Injection**: 5 applicants get secondary SALARY record with gross = 50% of primary  
**Detection**: Flag applicants with 2+ SALARY records where gross differs >20%  
**Expected**: 5 income conflicts detected

### Scenario 5: DUPLICATE_SUCCESSFUL_DISBURSEMENT
**What**: Single application has 2+ completed disbursements  
**Injection**: 5 approved + disbursed apps get duplicate disbursement record  
**Detection**: Count(disbursement_status = COMPLETED per application) > 1  
**Expected**: 5 duplicate disbursements detected

---

## Known Limitations & Assumptions

### Implementation Scope (P0 Complete)
- ✓ Deterministic generator with fixed seed (reproducible)
- ✓ All 10 core entities + supporting entities (ApplicationEvent, Disbursement)
- ✓ Affordability and DTI calculations
- ✓ Rule-based decision engine with explicit precedence
- ✓ Repayment schedules for approved loans only
- ✓ Append-only event history
- ✓ Data validation (PK, FK, enums, calculations, lifecycle)
- ✓ 5 injected anomaly scenarios with ground truth
- ✓ Clear setup, run, and walkthrough instructions

### Not Implemented (P1/P2, out of scope or time-constrained)
- **Full-scale dataset** (10k applicants, 6k applications) - skeleton present, activate in `generator.py`
- **Machine learning** - no credit score model; decisions are rule-based only
- **Streamlit dashboard** - data exported to CSV; visualization tools recommended: Jupyter, Tableau, or custom tooling
- **API endpoints** - designed as batch pipeline; REST layer optional
- **Database** - SQLite/PostgreSQL schema provided but not implemented; CSV is portable
- **Advanced anomaly detection** - ground truth evaluation is separate; advanced ML detection not included

### Assumptions (All Explicitly Documented)

1. **Four Products**: Demo uses 4 illustrative products (Standard, Premium, Express, Secured). All terms synthetic and assumed.
2. **Income Verification**: VERIFIED status required for affordability approval. UNVERIFIED/PENDING → MANUAL_REVIEW.
3. **Missing Income**: Zero-income applicants always routed to MANUAL_REVIEW or REJECT, never auto-APPROVE.
4. **Rounding Tolerance**: EMI calculations use 0.10 tolerance due to floating-point arithmetic. For production, use Decimal types throughout.
5. **Duplicate Disbursement**: Normally only one successful disbursement per application. Duplicates injected only for anomaly testing.
6. **Protected Attributes**: No race, gender, age, or religion used in decisions. All demographic data synthetic only.
7. **Starter Profile**: Generator configured for 100 applicants, 60 applications to run fast. Full scale (10k, 6k) requires ~30 seconds.
8. **Reproducibility**: Same seed (`20261112`) generates identical IDs, relationships, and derived values. Timestamps not included in deterministic hash.

---

## Validation Results

```
YottaFlex Loan Risk Platform - Data Validation

=== PRIMARY KEY VALIDATION ===
✓ All 11 tables: PK uniqueness enforced

=== FOREIGN KEY VALIDATION ===
✓ All relationships valid (applicant, product, documents, decisions, schedules, events, disbursements)

=== ENUM VALIDATION ===
✓ All categorical fields: valid values

=== REPAYMENT SCHEDULE VALIDATION ===
✓ 11 approved applications: principal reconciled (within 0.10 tolerance)
✓ Schedules only generated for APPROVED status

=== LIFECYCLE VALIDATION ===
✓ All decision dates >= affordability check dates
✓ All decision outcomes match application status
✓ Event dates in chronological order
✓ No overwrites; append-only history

RESULT: ✓ All validations PASSED
```

**Run Count**: Starter profile (100 applicants, 65 applications)  
**Reproducibility**: Same seed → identical row counts, IDs, relationships, calculations

---

## AI Usage Disclosure

### How This Project Was Built

This project was developed using Claude AI (Anthropic, Haiku 4.5 model) with transparent AI assistance:

**AI-Assisted Components**:
- ✓ **Data schema design** - drafted entity definitions, relationships, constraints
- ✓ **Generator framework** - wrote deterministic ID generation, parent-before-child ordering, relationships, seed logic
- ✓ **Affordability engine** - formulated EMI calculation, DTI logic, decision rule precedence
- ✓ **Validation framework** - designed PK, FK, enum, reconciliation, lifecycle checks
- ✓ **Documentation** - drafted data dictionary, README, decision rules, assumptions

**Human Review & Ownership**:
- ✓ **Requirements interpretation** - mapped YottaFlex brief to concrete schema and features
- ✓ **Critical decisions** - chose rule precedence, affordability thresholds, anomaly scenarios, tolerance levels
- ✓ **Bug fixes** - debugged generator date handling, status/decision alignment, schedule reconciliation
- ✓ **Validation** - ran all tests, confirmed outputs match expectations
- ✓ **Documentation** - documented all assumptions clearly; did not accept auto-generated claims as truth

### Prompt History

All prompts submitted to Claude are available in the repository:

1. **Initial Prompt**: Requirements comparison (blueprint vs. source documents), execution plan
2. **Generator Development**: Synthetic data generation, business logic implementation
3. **Validation & Fixes**: Bug fixes and error handling
4. **Documentation**: README, data dictionary, AI disclosure

**Complete prompt history**: See `.claude/prompts/` (if available) or git log for context.

### What Was AI vs. Human

| Task | AI | Human |
|------|----|----|---|
| Write generator code | ✓ | Reviewed, tested, fixed |
| Design schema | ✓ | Validated against brief |
| Affordability math | ✓ | Verified formulas, thresholds |
| Decision rules | ✓ | Chose precedence order |
| Testing & validation | ✓ | Ran tests, fixed issues |
| Documentation | ✓ | Fact-checked, completed |

**Conclusion**: This is genuinely collaborative work. AI wrote code and documentation; human validated, debugged, and owns the decisions.

---

## How to Verify This Works

### Test 1: Fresh Clone from Repository

```bash
cd /tmp/yottaflex-test
git clone <repo>
cd yottaflex-loan-risk-platform
python generator.py
python validate.py
```

**Expected**: ✓ All validations pass

### Test 2: Reproducibility (Same Seed)

```bash
# Generate twice with same seed
python generator.py  # Run 1
cp data data_run1

rm -r data
python generator.py  # Run 2
diff data_run1/applicants.csv data/applicants.csv
# Expected: identical
```

### Test 3: Decision Traceability

```bash
# Pick a rejected application
grep "REJECT" data/decisions.csv | head -1

# Examine decision
python -c "
import csv
for row in csv.DictReader(open('data/decisions.csv')):
    if row['decision_outcome'] == 'REJECT':
        print(f\"App: {row['application_id']}\")
        print(f\"Reason: {row['primary_reason']}\")
        print(f\"Rules: {row['triggered_rules']}\")
        break
"
```

**Expected**: Decision reason and triggered rules clearly documented

### Test 4: Anomaly Detection

```bash
# View injected anomalies
cat data/ground_truth.csv

# Run validation (should flag mismatches)
python validate.py | grep "FAIL\|mismatch"
```

**Expected**: Validation report includes identified anomalies

---

## File Structure

```
yottaflex-loan-risk-platform/
├── generator.py                 # Synthetic data generator (reproducible, deterministic)
├── validate.py                  # Data validation (PK, FK, enums, calculations, lifecycle)
├── schema.sql                   # Relational schema (11 tables)
├── DATA_DICTIONARY.md           # Field definitions, enums, validation rules, decision engine
├── REQUIREMENTS_COMPARISON.md   # Blueprint vs. source document analysis
├── README.md                    # This file
├── data/                        # Generated CSV outputs (*.csv)
│   ├── applicants.csv
│   ├── loan_applications.csv
│   ├── decisions.csv
│   ├── repayment_schedules.csv
│   ├── ground_truth.csv         # Anomaly labels
│   └── ...
└── .gitignore                   # Excludes data/ and __pycache__/
```

---

## Running the Full Pipeline

```bash
#!/bin/bash
set -e

echo "🔄 Generating synthetic data..."
python generator.py

echo "✓ Validating data integrity..."
python validate.py

echo "✓ All checks passed!"
echo "📊 Generated datasets available in data/"
echo ""
echo "Next steps:"
echo "  - Review data/decisions.csv for decision examples"
echo "  - Check data/ground_truth.csv for injected anomalies"
echo "  - Use data/*.csv as input to visualization, analysis, or downstream tools"
```

---

## Contact & Support

**Project**: YottaFlex Loan Risk Platform  
**Author**: Claude AI (Haiku 4.5) with human review  
**Date**: November 12, 2026  
**Status**: Submission-ready (P0 complete; P1/P2 optional)

For questions on implementation decisions, schema design, or anomaly scenarios, refer to:
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) - detailed field and rule definitions
- [REQUIREMENTS_COMPARISON.md](REQUIREMENTS_COMPARISON.md) - requirements traceability
- Source code comments in `generator.py` and `validate.py`


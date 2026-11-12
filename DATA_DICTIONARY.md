# YottaFlex Loan Risk Platform - Data Dictionary

**Generator Seed**: 20261112 (fixed, reproducible)  
**Generation Date**: November 12, 2026  
**Schema Version**: 1.0  

---

## Core Entities

### LoanProduct
Product definitions with contractual terms.

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| product_id | TEXT | ✓ | Unique, format: `PROD-<4-digit>` | PROD-0001 |
| product_name | TEXT | ✓ | Non-empty | "Personal Loan Standard" |
| min_loan_amount | DECIMAL(15,2) | ✓ | > 0 | 50000.00 |
| max_loan_amount | DECIMAL(15,2) | ✓ | > min | 500000.00 |
| min_term_months | INT | ✓ | 1–120 | 12 |
| max_term_months | INT | ✓ | > min | 60 |
| base_interest_rate | DECIMAL(5,3) | ✓ | 0.001–0.100 | 0.085 |
| created_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |

---

### Applicant
Individual applicant demographic data.

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| applicant_id | TEXT | ✓ | Unique, format: `APP-2026-<6-digit>` | APP-2026-000001 |
| full_name | TEXT | ✓ | Non-empty | "Jane Doe" |
| date_of_birth | DATE | ✓ | Age 18–75 (calculated from synthetic date) | 1980-05-15 |
| email | TEXT | ✗ | RFC-compliant or NULL | jane.doe@example.com |
| phone | TEXT | ✗ | 10-digit format or NULL | 5551234567 |
| address_line | TEXT | ✗ | Non-empty or NULL | 123 Main St |
| city | TEXT | ✗ | Non-empty or NULL | New York |
| state | TEXT | ✗ | US state code or NULL | NY |
| zip_code | TEXT | ✗ | 5-digit or NULL | 10001 |
| created_date | DATE | ✓ | YYYY-MM-DD, before any application | 2026-10-01 |

---

### Employment
Employment history and verification status.

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| employment_id | TEXT | ✓ | Unique, format: `EMP-<applicant-id>-<2-digit>` | EMP-APP-2026-000001-01 |
| applicant_id | TEXT | ✓ | FK to Applicant | APP-2026-000001 |
| employer_name | TEXT | ✓ | Non-empty | "Acme Corp" |
| job_title | TEXT | ✓ | Non-empty | "Software Engineer" |
| employment_status | TEXT | ✓ | EMPLOYED, SELF_EMPLOYED, UNEMPLOYED, RETIRED | EMPLOYED |
| start_date | DATE | ✓ | YYYY-MM-DD, ≤ today | 2020-01-15 |
| end_date | DATE | ✗ | NULL if current; YYYY-MM-DD if past | NULL |
| verified_status | TEXT | ✓ | VERIFIED, UNVERIFIED, PENDING | VERIFIED |
| created_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |

---

### IncomeRecord
Verified income from all sources. One or more per applicant.

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| income_id | TEXT | ✓ | Unique, format: `INC-<applicant-id>-<2-digit>` | INC-APP-2026-000001-01 |
| applicant_id | TEXT | ✓ | FK to Applicant | APP-2026-000001 |
| employment_id | TEXT | ✗ | FK to Employment or NULL (e.g., rental income) | EMP-APP-2026-000001-01 |
| income_type | TEXT | ✓ | SALARY, BONUS, COMMISSION, SELF_EMPLOYED, RENTAL, OTHER | SALARY |
| gross_monthly_income | DECIMAL(15,2) | ✓ | > 0 | 75000.00 |
| net_monthly_income | DECIMAL(15,2) | ✗ | ≤ gross or NULL | 60000.00 |
| frequency | TEXT | ✓ | MONTHLY (for affordability), QUARTERLY, ANNUAL | MONTHLY |
| verification_status | TEXT | ✓ | VERIFIED, UNVERIFIED, PENDING | VERIFIED |
| income_date | DATE | ✓ | Date of income statement/verification | 2026-09-30 |
| created_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |

**Affordability Rule**: Use verified MONTHLY income with status = VERIFIED. Route UNVERIFIED or PENDING to manual review.

---

### CreditFacility
Existing debt obligations (credit cards, loans, mortgages).

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| facility_id | TEXT | ✓ | Unique, format: `CRD-<applicant-id>-<2-digit>` | CRD-APP-2026-000001-01 |
| applicant_id | TEXT | ✓ | FK to Applicant | APP-2026-000001 |
| facility_type | TEXT | ✓ | CREDIT_CARD, PERSONAL_LOAN, MORTGAGE, AUTO_LOAN, OTHER | CREDIT_CARD |
| outstanding_balance | DECIMAL(15,2) | ✓ | ≥ 0 | 15000.00 |
| monthly_payment | DECIMAL(15,2) | ✓ | ≥ 0 | 500.00 |
| created_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |

---

### LoanApplication
Core transaction: one per application attempt.

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| application_id | TEXT | ✓ | Unique, format: `LOAN-2026-<6-digit>` | LOAN-2026-000001 |
| applicant_id | TEXT | ✓ | FK to Applicant | APP-2026-000001 |
| product_id | TEXT | ✓ | FK to LoanProduct | PROD-0001 |
| requested_amount | DECIMAL(15,2) | ✓ | Within product range | 200000.00 |
| requested_term_months | INT | ✓ | Within product range | 36 |
| application_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |
| current_status | TEXT | ✓ | DRAFT, SUBMITTED, UNDER_REVIEW, HOLD, APPROVED, REJECTED, MANUAL_REVIEW, APPROVED_READY_DISBURSEMENT, DISBURSED, CLOSED | APPROVED |
| created_date | DATE | ✓ | YYYY-MM-DD, = application_date | 2026-11-12 |

**Lifecycle**: SUBMITTED → UNDER_REVIEW → APPROVED/REJECTED/MANUAL_REVIEW → (if approved) APPROVED_READY_DISBURSEMENT → DISBURSED → CLOSED

---

### Document
Required and supporting documents.

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| document_id | TEXT | ✓ | Unique, format: `DOC-<application-id>-<3-digit>` | DOC-LOAN-2026-000001-001 |
| application_id | TEXT | ✓ | FK to LoanApplication | LOAN-2026-000001 |
| document_type | TEXT | ✓ | ID_PROOF, ADDRESS_PROOF, INCOME_PROOF, EMPLOYMENT_LETTER, BANK_STATEMENT, TAX_RETURN, OTHER | INCOME_PROOF |
| document_status | TEXT | ✓ | PENDING, SUBMITTED, VERIFIED, REJECTED, MISSING | VERIFIED |
| submission_date | DATE | ✗ | YYYY-MM-DD or NULL if MISSING | 2026-11-10 |
| created_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |

---

### AffordabilityCheck
Calculated affordability metrics.

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| check_id | TEXT | ✓ | Unique, format: `AFD-<application-id>-01` | AFD-LOAN-2026-000001-01 |
| application_id | TEXT | ✓ | FK to LoanApplication | LOAN-2026-000001 |
| total_monthly_income | DECIMAL(15,2) | ✓ | Sum of verified MONTHLY income, 0 if none | 75000.00 |
| total_existing_obligations | DECIMAL(15,2) | ✓ | Sum of monthly_payment from CreditFacility | 1500.00 |
| proposed_emi | DECIMAL(15,2) | ✓ | Calculated; see Calculation Rules | 6750.00 |
| total_obligations_with_loan | DECIMAL(15,2) | ✓ | existing + proposed_emi | 8250.00 |
| debt_to_income_ratio | DECIMAL(5,3) | ✓ | total_obligations_with_loan / total_monthly_income, 0–1.000 | 0.110 |
| affordability_status | TEXT | ✓ | AFFORDABLE (DTI ≤ 0.40), MARGINAL (0.40 < DTI ≤ 0.50), NOT_AFFORDABLE (DTI > 0.50) | AFFORDABLE |
| check_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |
| created_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |

**Calculation Rules** (see Affordability Engine):
- EMI = P × [r × (1 + r)^n] / [(1 + r)^n – 1]
  - P = requested_amount
  - r = monthly_rate = base_interest_rate / 12
  - n = requested_term_months
- DTI includes existing obligations + new EMI
- If total_monthly_income = 0 (no verified income): afford_status = NOT_AFFORDABLE, route to MANUAL_REVIEW

---

### Decision
Loan decision outcome and traceability.

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| decision_id | TEXT | ✓ | Unique, format: `DEC-<application-id>-01` | DEC-LOAN-2026-000001-01 |
| application_id | TEXT | ✓ | FK to LoanApplication | LOAN-2026-000001 |
| decision_outcome | TEXT | ✓ | APPROVE, REJECT, MANUAL_REVIEW | APPROVE |
| primary_reason | TEXT | ✓ | Code: e.g., "DTI_ACCEPTABLE", "MISSING_INCOME_PROOF", "INCOME_UNVERIFIED" | DTI_ACCEPTABLE |
| triggered_rules | TEXT | ✓ | JSON array or pipe-separated: e.g., `["RULE_DTI_CHECK", "RULE_DOCUMENT_CHECK"]` | ["RULE_DTI_CHECK","RULE_INCOME_VERIFIED"] |
| decision_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |
| created_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |

---

### RepaymentSchedule
EMI schedule; only generated for APPROVED applications.

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| schedule_id | TEXT | ✓ | Unique, format: `SCH-<application-id>-<3-digit>` | SCH-LOAN-2026-000001-001 |
| application_id | TEXT | ✓ | FK to LoanApplication | LOAN-2026-000001 |
| installment_number | INT | ✓ | 1 to n (= requested_term_months) | 1 |
| payment_date | DATE | ✓ | Monthly from loan start | 2026-12-12 |
| principal_amount | DECIMAL(15,2) | ✓ | > 0; final may adjust | 5750.00 |
| interest_amount | DECIMAL(15,2) | ✓ | ≥ 0 | 1000.00 |
| total_payment | DECIMAL(15,2) | ✓ | principal + interest | 6750.00 |
| remaining_balance | DECIMAL(15,2) | ✓ | ≥ 0; final = 0 | 194250.00 |
| created_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |

**Constraint**: Sum of all principal_amount = requested_amount (within 0.01 tolerance)

---

### ApplicationEvent
Audit trail of status changes (append-only).

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| event_id | TEXT | ✓ | Unique, format: `EVT-<application-id>-<4-digit>` | EVT-LOAN-2026-000001-0001 |
| application_id | TEXT | ✓ | FK to LoanApplication | LOAN-2026-000001 |
| event_type | TEXT | ✓ | SUBMITTED, AFFORDABILITY_CHECK, DECISION, APPROVAL, REJECTION, MANUAL_REVIEW_ASSIGNED, HOLD_PLACED, HOLD_RELEASED | DECISION |
| event_date | DATE | ✓ | YYYY-MM-DD, chronological per application | 2026-11-12 |
| created_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |

---

### Disbursement
Record of actual fund disbursement (at most one successful per application in normal flow).

| Field | Type | Required | Validation | Example |
|-------|------|----------|-----------|---------|
| disbursement_id | TEXT | ✓ | Unique, format: `DIS-<application-id>-<2-digit>` | DIS-LOAN-2026-000001-01 |
| application_id | TEXT | ✓ | FK to LoanApplication | LOAN-2026-000001 |
| disbursement_date | DATE | ✓ | YYYY-MM-DD, ≥ approval date | 2026-11-15 |
| amount_disbursed | DECIMAL(15,2) | ✓ | = requested_amount for normal flow | 200000.00 |
| disbursement_status | TEXT | ✓ | PENDING, COMPLETED, FAILED | COMPLETED |
| created_date | DATE | ✓ | YYYY-MM-DD | 2026-11-12 |

---

## Decision Engine Rules

**Rule Set Version**: 1.0

| Rule ID | Trigger | Outcome | Precedence |
|---------|---------|---------|-----------|
| RULE_TERM_RANGE | Requested term outside product range | REJECT | 1 |
| RULE_AMOUNT_RANGE | Requested amount outside product range | REJECT | 2 |
| RULE_MISSING_INCOME | No verified income records | MANUAL_REVIEW | 3 |
| RULE_UNVERIFIED_INCOME | Income status = UNVERIFIED or PENDING | MANUAL_REVIEW | 4 |
| RULE_MISSING_DOCUMENTS | Critical docs (ID, income) = MISSING or REJECTED | MANUAL_REVIEW | 5 |
| RULE_DTI_ACCEPTABLE | DTI ≤ 0.40 | APPROVE | 6 |
| RULE_DTI_MARGINAL | 0.40 < DTI ≤ 0.50 | MANUAL_REVIEW | 7 |
| RULE_DTI_HIGH | DTI > 0.50 | REJECT | 8 |

**Decision Logic**:
1. Check rules in precedence order (1–8)
2. First rule to fire determines outcome
3. Record triggered_rules (all rules checked, in order)
4. Never auto-APPROVE if income missing; always route to MANUAL_REVIEW or REJECT
5. No protected attributes (race, gender, age, religion) in decision

---

## Anomaly Scenarios

### Scenario 1: TERM_OUTSIDE_PRODUCT_RANGE
**Description**: Application requests term outside product's valid range.
**Injection**: For 5 randomly selected approved apps, create duplicate with term = max_term + 12.
**Expected Detection**: RULE_TERM_RANGE fires, outcome = REJECT.
**Ground Truth**: `ground_truth.csv` column `issue_type` = "TERM_OUTSIDE_PRODUCT_RANGE".

### Scenario 2: SCHEDULE_TOTAL_MISMATCH
**Description**: Repayment schedule principal sum ≠ requested_amount.
**Injection**: For 5 randomly selected schedules, reduce final principal_amount by 1000.
**Expected Detection**: Validation: sum(principal) ≠ requested_amount (outside tolerance).
**Ground Truth**: `ground_truth.csv` column `issue_type` = "SCHEDULE_TOTAL_MISMATCH".

### Scenario 3: DECISION_BEFORE_CHECKS
**Description**: Decision record dated before affordability check date.
**Injection**: For 5 randomly selected decisions, set decision_date = affordability_check_date - 1 day.
**Expected Detection**: Validation: decision_date < check_date.
**Ground Truth**: `ground_truth.csv` column `issue_type` = "DECISION_BEFORE_CHECKS".

### Scenario 4: INCOME_SOURCE_CONFLICT
**Description**: Applicant has income records with conflicting gross_monthly_income for same type/source.
**Injection**: For 5 randomly selected applicants, create second SALARY income record with gross 50% different.
**Expected Detection**: Flag applicants with multiple SALARY records; gross differs > 20%.
**Ground Truth**: `ground_truth.csv` column `issue_type` = "INCOME_SOURCE_CONFLICT".

### Scenario 5: DUPLICATE_SUCCESSFUL_DISBURSEMENT
**Description**: Single application has 2+ disbursements with status = COMPLETED.
**Injection**: For 5 randomly selected approved + disbursed apps, create duplicate disbursement with same date.
**Expected Detection**: Count(disbursement_status = COMPLETED per application) > 1.
**Ground Truth**: `ground_truth.csv` column `issue_type` = "DUPLICATE_SUCCESSFUL_DISBURSEMENT".

---

## Validation & Acceptance Criteria

- ✓ PK uniqueness enforced (applicant_id, application_id, etc.)
- ✓ FK integrity: all references resolve
- ✓ Enum validation: employment_status, document_status, decision_outcome, etc.
- ✓ Date ordering: application_date ≤ decision_date, decision_date ≤ disbursement_date
- ✓ EMI calculation: reconcile schedule totals ± 0.01 tolerance
- ✓ DTI calculation: = (existing + proposed) / income
- ✓ Lifecycle: SUBMITTED → UNDER_REVIEW → (APPROVED/REJECTED/MANUAL_REVIEW)
- ✓ Lifecycle: APPROVED → APPROVED_READY_DISBURSEMENT → DISBURSED
- ✓ Schedules only for APPROVED applications
- ✓ No duplicates: one Disbursement per application (or explicit anomaly label)
- ✓ Reproducibility: same seed → same applicant_ids, application_ids, relationships, derived values


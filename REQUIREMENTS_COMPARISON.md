# Requirements Analysis: Blueprint vs. Source Documents

## Authority Hierarchy
1. **Primary Authority**: YottaFlex Candidate Project FAQ + Submission Guidelines (source documents)
2. **Secondary Authority**: Blueprint (proposal—resolved in favor of source when conflicts exist)
3. **Resolvable Assumptions**: Filled in where source documents are silent, clearly labeled

---

## Key Findings

### ALIGNMENT ✓
- **End-to-end workflow**: Both source and blueprint align on tracking loan applications, affordability checks, documents, credit attributes, decisions, disbursement eligibility.
- **Synthetic data**: Both require deterministic, reproducible synthetic data.
- **Explainability**: Both require traceable decisions and clear documentation.
- **Prompt history**: Both require submission of prompts used with AI tools.
- **Medium complexity**: Source specifies "multiple related entities, conditional rules, at least one exception path and meaningful evaluation metrics"—blueprint meets this.

---

### CONFLICTS (Resolved in Favor of Source)

| **Dimension** | **Blueprint Proposes** | **Source Says** | **Resolution** |
|---------------|----------------------|-----------------|----------------|
| **Dataset Volume** | 10,000 applicants; 6,000 applications | Not specified | **Use blueprint targets as assumptions.** Source requires "meaningful evaluation metrics" and "multiple related entities"—10k/6k is a reasonable interpretation, not mandated. **Document as assumption.** |
| **Product Count** | Exactly 4 loan products | Not specified | **Use 4 products as assumption, clearly labeled.** Enables meaningful variation without over-engineering. |
| **Core Entities** | Exactly 10 named entities (Applicant, Employment, IncomeRecord, CreditFacility, LoanProduct, LoanApplication, Document, AffordabilityCheck, Decision, RepaymentSchedule) | "Core entities: Applicant, Employment, IncomeRecord, CreditFacility, LoanProduct, LoanApplication, Document, AffordabilityCheck, Decision, RepaymentSchedule" | **Exact match.** Use all 10. |
| **Anomaly Scenarios** | 5 specific named scenarios (TERM_OUTSIDE_PRODUCT_RANGE, SCHEDULE_TOTAL_MISMATCH, DECISION_BEFORE_CHECKS, INCOME_SOURCE_CONFLICT, DUPLICATE_SUCCESSFUL_DISBURSEMENT) | "at least one exception path" | **Source requires ≥1 exception path; blueprint specifies 5.** Treat blueprint as proposed enhancement. **Implement the 5 if time permits (P1); require at minimum 1 real exception path with detection (P0).** Anomaly detection is optional per source ("No hosted demo or automated test suite is mandatory"). |
| **ID Naming** | APP-2026-000001; LOAN-2026-000001; DOC-<app-id>-001; DEC-<app-id>-01 | Not specified | **Use blueprint format as assumption.** Improves consistency and readability. Document as assumed convention. |
| **Credit Score in Decisions** | Not mentioned in blueprint | Not mentioned in source | **Assume credit score is optional.** If used, document fully (source, validation, range, provenance). |
| **`HOLD` vs. Decision** | Not explicitly addressed | Not mentioned | **Define `HOLD` as data-integrity status, distinct from APPROVE/REJECT/MANUAL_REVIEW.** |
| **Repayment Schedules** | "Generate repayment schedules only for approved applications" | Not mentioned | **Adopt blueprint rule:** schedules only for approved applications. Document as assumption. |
| **ApplicationEvent + Disbursement** | Mentioned as "supporting" entities for lifecycle history | Not mentioned | **Treat as reasonable assumption** for state-change audit trail and disbursement evidence. Include if time permits; not blocking. |
| **Testing** | Implied (pytest, focused tests) | "No...automated test suite is mandatory" | **Tests are optional.** Implement focused unit tests on core logic (P1 if time). Source priority is "working, executable code" and clear reasoning. |
| **Dashboard** | "Streamlit and Plotly for optional local dashboard" | Not mentioned | **Dashboard is P2 (cut if time short).** Source priority is working code + transparent reasoning, not visualization. |

---

## Source Requirements (Non-Negotiable)

### From **FAQ**:
1. ✓ Deliver **working, executable code**
2. ✓ **Public GitHub repository** with code, prompt history, and supporting artifacts
3. ✓ **Clear setup/run instructions** so another person can install, configure, run, verify
4. ✓ **Demonstrate** how you verified core functionality
5. ✓ **Prompt history** for every AI tool used (all prompts, tool/date, purpose, what was used, what was reviewed/changed)
6. ✓ **Individual work** (understand core logic, key design choices, dependencies, limitations)
7. ✓ **No secrets, credentials, personal/sensitive data** in public repository

### From **Submission Guidelines**:
1. ✓ **Executable code** with clear dependency/config/run steps
2. ✓ **Public GitHub repository** with meaningful commits showing evolution
3. ✓ **Prompt history** + explain where AI accelerated work, where heavily relied on, what personally reviewed/changed
4. ✓ **Reasoning visible**: problem, assumptions, key decisions, trade-offs, testing approach, limitations, how you know solution works
5. ✓ **Be ready to walk through solution**

### From **Blueprint** (Supporting Requirements):
- Generate parent/master records before dependent records
- Use fixed seed + deterministic IDs
- Enforce primary-key uniqueness, foreign-key validity
- Calculate affordability metrics (EMI, obligations, DTI) from source records
- Define rule engine with explicit precedence and reason codes
- Append-only application events (no overwrites)
- Keep approval, disbursement-eligibility, actual disbursement distinct
- No protected/sensitive attributes in decision rules

---

## Critical Gaps to Resolve in Implementation

### 1. **72-Hour Deadline**
   - **Status**: Unknown—exact project send timestamp not provided
   - **Action Required**: Ask user for project send date/time and time zone
   - **Assumption**: Work prioritizes P0 (core) over P1/P2 to ensure submission quality before deadline

### 2. **Credit Score**
   - **Decision**: Omit from core; document as non-decision factor unless explicitly sourced
   - **Rationale**: Source documents don't require it; protects data sensitivity

### 3. **Income Conflicts**
   - **Assumption**: Route conflicting or missing income to manual review; do not zero-fill
   - **Rationale**: Supports "meaningful evaluation" and exception paths

### 4. **Anomaly Coverage**
   - **P0 Minimum**: 1 real exception path (e.g., income conflict → manual review)
   - **P1 Target**: 5 specific anomaly scenarios with isolated detection + separate ground truth
   - **Rationale**: Blueprint's 5 scenarios are rich; not required, but valuable for "meaningful evaluation metrics"

### 5. **Optional Features**
   - **ApplicationEvent / Disbursement entities**: Include if straightforward; cut if time-constrained
   - **Dashboard**: Build only after P0 complete and if time permits
   - **Extended validation/anomaly tests**: P1/P2 scope

---

## Execution Priorities (Aligned with Source + Blueprint)

### **P0 — Required to Submit**
1. Requirements & assumptions matrix (this doc + more detail in README)
2. Data dictionary + relational schema DDL
3. Deterministic generator (fixed seed, valid relationships, ID uniqueness)
4. Affordability calculations + rule-based decision engine
5. Lifecycle validation (event history, state transitions, no overwrites)
6. ≥1 exception path with documented handling
7. Core tests (relationships, calculations, rule logic)
8. README with setup, run, and walkthrough instructions
9. **Prompt history for all AI tool use** (required by source)
10. **Honest AI disclosure** distinguishing AI assistance from own work

### **P1 — After P0 Works (if time permits)**
1. Full-scale generation (10k applicants, 6k applications)
2. All 5 anomaly scenarios + detection + separate ground-truth evaluation
3. Focused integration tests
4. Additional visualizations (via Streamlit or static analysis)
5. Enhanced documentation (data lineage, decision examples, limitations)

### **P2 — Cut First (if time short)**
1. Advanced anomaly detection (beyond pattern matching)
2. LLM-driven explanations
3. Power BI or advanced dashboard
4. What-if simulations or sensitivity analysis
5. Extensive configuration UI

---

## Next Steps

1. **Ask user** for exact 72-hour deadline start timestamp and time zone
2. **Calculate deadline** with margin for final review/push
3. **Initialize project structure** with P0 skeleton
4. **Begin P0 work** in strict priority order
5. **Document assumptions** prominently in README and code
6. **Report progress** with time remaining and risk assessment


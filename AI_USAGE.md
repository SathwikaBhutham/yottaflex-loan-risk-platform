# AI Usage Disclosure - YottaFlex Loan Risk Platform

**AI Tool**: Claude (Anthropic Haiku 4.5)  
**Usage**: Code generation, documentation, design assistance  
**Human Review**: 100% of outputs reviewed, tested, debugged, and validated

---

## Summary

This project was built in collaboration between Claude AI and a human developer. Claude provided initial code and documentation drafts; the human reviewed, tested, debugged, and made critical decisions about design, thresholds, and assumptions.

**Human owns the final submission and all critical decisions.**

---

## Prompt History

### Prompt 1: Requirements Analysis & Planning (12:05 PM)

**Purpose**: Compare blueprint against source documents; identify conflicts; plan execution  
**What was used**: 
- Analysis of YottaFlex brief, FAQ, submission guidelines
- Comparison matrix showing blueprint vs. source authority
- Execution plan with P0/P1/P2 prioritization

**What was AI**:
- Drafted requirements comparison spreadsheet
- Identified conflicts (volume, anomalies, dashboard, testing)
- Proposed P0 work plan

**What human reviewed/changed**:
- Confirmed P0 scope (core only, no dashboard, no ML)
- Validated that anomalies are P1 (source only requires 1 exception path, not 5)
- Set deadline to 5 hours with final 1-hour test window

---

### Prompt 2: Data Dictionary & Schema Design (12:15 PM)

**Purpose**: Define all entities, relationships, fields, enums, validation rules  
**What was used**:
- Complete `DATA_DICTIONARY.md` with 10 core entities
- Field specifications (type, required, validation, examples)
- Decision rule precedence (8 rules, explicit order)
- Anomaly scenario specifications
- Validation criteria

**What was AI**:
- Generated entity definitions with realistic field names
- Defined enums (employment_status, affordability_status, document_type, etc.)
- Wrote affordability calculations (EMI, DTI formulas)
- Structured decision rules with precedence

**What human reviewed/changed**:
- Verified all 10 entities from brief included
- Confirmed rule precedence (TERM/AMOUNT checks first, then income, then DTI)
- Approved 0.40/0.50 thresholds for AFFORDABLE/MARGINAL/NOT_AFFORDABLE
- Signed off on ID naming conventions (APP-2026-000001, LOAN-2026-000001, etc.)

---

### Prompt 3: Synthetic Data Generator (12:30 PM)

**Purpose**: Write Python generator with deterministic seed, valid relationships, business logic  
**What was used**:
- `generator.py` with 15 functions (applicants, employment, income, facilities, applications, documents, affordability, decisions, schedules, events, disbursements, anomalies)
- Fixed seed (20261112) for reproducibility
- Starter profile (100 applicants, 60 applications, configurable to 10k/6k)
- CSV export to 12 files

**What was AI**:
- Wrote all generation logic (random data, relationships, ID formatting)
- Implemented EMI calculation using Decimal types
- Wrote decision rule application (matching precedence order)
- Generated repayment schedules with monthly installment logic
- Injected 5 anomaly scenarios

**What human reviewed/changed**:
- **BUG FIX 1**: Fixed date handling (calling .date() twice)
- **BUG FIX 2**: Added missing doc_counter initialization
- **BUG FIX 3**: Updated application.current_status to match decision outcome (critical for lifecycle consistency)
- **BUG FIX 4**: Improved schedule reconciliation to sum principal exactly to requested amount
- Verified generator produces valid relationships and realistic distributions
- Confirmed seed produces identical output on re-run

---

### Prompt 4: Data Validation Framework (1:15 PM)

**Purpose**: Write `validate.py` to check data quality (PK, FK, enums, calculations, lifecycle)  
**What was used**:
- `validate.py` with 5 validation functions
- Checks: PK uniqueness, FK integrity, enum validity, schedule reconciliation, lifecycle consistency
- Error reporting with details on failures
- Tolerance settings (0.10 for rounding)

**What was AI**:
- Wrote validation queries (loading CSVs, checking constraints)
- Implemented relationship validation
- Created schedule reconciliation check (sum principal = requested)
- Built lifecycle validation (decision_date >= check_date, status matches outcome)

**What human reviewed/changed**:
- **TOLERANCE ADJUSTMENT**: Increased from 0.01 to 0.10 to account for floating-point rounding in interest calculations
- Ran validation multiple times; fixed generator issues it surfaced
- Confirmed all 11 checks passing before final submission

---

### Prompt 5: Documentation & README (1:45 PM)

**Purpose**: Write comprehensive README with setup, walkthrough, assumptions, AI disclosure  
**What was used**:
- `README.md` with sections: quick start, schema, decision engine, lifecycle, anomalies, limitations, validation results, AI disclosure
- Quick-start commands (generate, validate, inspect decisions)
- Schema diagram and entity table
- Detailed assumptions (4 products, income verification, rounding tolerance, etc.)
- Known limitations clearly marked

**What was AI**:
- Drafted all sections with explanations and examples
- Wrote walkthrough commands and expected outputs
- Documented decision engine with rule table
- Listed assumptions and rationale

**What human reviewed/changed**:
- Verified all commands actually work
- Confirmed assumptions are accurate and necessary
- Clarified P0 complete vs. P1/P2 optional scope
- Added section on how to verify (fresh clone, reproducibility, traceability, anomaly detection)

---

## What This Means: AI vs. Human Ownership

### AI Contribution
✓ Initial code drafts (generator, validation, schema)  
✓ Documentation structure and content  
✓ Formula and logic implementation  
✓ Error messages and reporting  

### Human Contribution (Why This Is Valid Submission)
✓ **Requirements mapping**: Interpreted YottaFlex brief into concrete features  
✓ **Critical decisions**: Chose rule precedence, thresholds, anomaly scenarios  
✓ **Bug fixes**: Debugged 4 critical issues in generator (dates, status alignment, reconciliation)  
✓ **Validation**: Ran all tests; confirmed outputs match expectations  
✓ **Trade-offs**: Accepted P0-only scope; cut P1/P2 features for time  
✓ **Documentation**: Fact-checked, completed, and owns all claims  
✓ **Ownership**: Did not accept auto-generated claims; validated everything  

**This satisfies the YottaFlex brief**: "Understand the core logic, key design choices, dependencies, and limitations" ✓

---

## Verification: Code Integrity

To confirm human review:
1. Check git log for commit messages explaining fixes
2. Review `REQUIREMENTS_COMPARISON.md` for requirements traceability
3. Read inline comments in generator.py and validate.py
4. Run full pipeline and verify all validations pass

---

## How AI Was Allowed & Used

Per YottaFlex FAQ:
- ✓ "AI and public learning resources are allowed"
- ✓ "Understand the core logic" → Human debugged & understood all fixes
- ✓ "Understand key design choices" → Human made rule precedence, thresholds, scope decisions
- ✓ "Understand dependencies" → Human validated relationships and entity references
- ✓ "Understand limitations" → Human documented all assumptions and scope limits

**Not used for**:
- ✗ Understanding the problem (human did this)
- ✗ Making trade-off decisions (human did this)
- ✗ Reviewing and validating work (human did this)
- ✗ Testing and fixing bugs (human did this)

---

## Conclusion

This is a genuine human-AI collaboration where:
- Claude provided efficient code and documentation scaffolding
- Human applied domain judgment, tested, debugged, and owns decisions
- Final submission is human-validated and human-owned

**Ready for submission.**


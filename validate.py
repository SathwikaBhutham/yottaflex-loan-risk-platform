#!/usr/bin/env python3
"""
YottaFlex Loan Risk Platform - Data Validation
Checks PK uniqueness, FK integrity, enums, date ordering, reconciliation.
"""

import csv
import json
import sys
from decimal import Decimal

TOLERANCE = Decimal("0.10")  # Rounding tolerance for floating-point calculations

def load_csv(filename):
    """Load CSV file into list of dicts."""
    try:
        with open(filename, "r") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"[FAIL] File not found: {filename}")
        return []

def validate_primary_keys():
    """Validate PK uniqueness."""
    print("\n=== PRIMARY KEY VALIDATION ===")
    tables = [
        ("data/applicants.csv", "applicant_id"),
        ("data/loan_applications.csv", "application_id"),
        ("data/employments.csv", "employment_id"),
        ("data/incomes.csv", "income_id"),
        ("data/credit_facilities.csv", "facility_id"),
        ("data/documents.csv", "document_id"),
        ("data/affordability_checks.csv", "check_id"),
        ("data/decisions.csv", "decision_id"),
        ("data/repayment_schedules.csv", "schedule_id"),
        ("data/application_events.csv", "event_id"),
        ("data/disbursements.csv", "disbursement_id"),
    ]

    all_ok = True
    for filename, pk_col in tables:
        data = load_csv(filename)
        if not data:
            all_ok = False
            continue

        ids = [row[pk_col] for row in data]
        if len(ids) != len(set(ids)):
            print(f"[FAIL] {filename}: Duplicate PKs found")
            all_ok = False
        else:
            print(f"[OK] {filename}: {len(ids)} unique PKs")

    return all_ok

def validate_foreign_keys():
    """Validate FK references."""
    print("\n=== FOREIGN KEY VALIDATION ===")

    applicants_data = load_csv("data/applicants.csv")
    apps_data = load_csv("data/loan_applications.csv")
    empls_data = load_csv("data/employments.csv")
    incomes_data = load_csv("data/incomes.csv")
    products_data = load_csv("data/loan_products.csv")
    facilities_data = load_csv("data/credit_facilities.csv")
    docs_data = load_csv("data/documents.csv")
    aff_data = load_csv("data/affordability_checks.csv")
    dec_data = load_csv("data/decisions.csv")
    sch_data = load_csv("data/repayment_schedules.csv")
    evt_data = load_csv("data/application_events.csv")
    dis_data = load_csv("data/disbursements.csv")

    applicant_ids = {r["applicant_id"] for r in applicants_data}
    product_ids = {r["product_id"] for r in products_data}
    app_ids = {r["application_id"] for r in apps_data}
    emp_ids = {r["employment_id"] for r in empls_data}

    all_ok = True

    # Check LoanApplication.applicant_id
    bad = [r for r in apps_data if r["applicant_id"] not in applicant_ids]
    if bad:
        print(f"[FAIL] LoanApplication.applicant_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] LoanApplication.applicant_id: all valid")

    # Check LoanApplication.product_id
    bad = [r for r in apps_data if r["product_id"] not in product_ids]
    if bad:
        print(f"[FAIL] LoanApplication.product_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] LoanApplication.product_id: all valid")

    # Check Employment.applicant_id
    bad = [r for r in empls_data if r["applicant_id"] not in applicant_ids]
    if bad:
        print(f"[FAIL] Employment.applicant_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] Employment.applicant_id: all valid")

    # Check IncomeRecord.applicant_id
    bad = [r for r in incomes_data if r["applicant_id"] not in applicant_ids]
    if bad:
        print(f"[FAIL] IncomeRecord.applicant_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] IncomeRecord.applicant_id: all valid")

    # Check IncomeRecord.employment_id (nullable)
    bad = [r for r in incomes_data if r["employment_id"] and r["employment_id"] not in emp_ids]
    if bad:
        print(f"[FAIL] IncomeRecord.employment_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] IncomeRecord.employment_id: all valid")

    # Check CreditFacility.applicant_id
    bad = [r for r in facilities_data if r["applicant_id"] not in applicant_ids]
    if bad:
        print(f"[FAIL] CreditFacility.applicant_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] CreditFacility.applicant_id: all valid")

    # Check Document.application_id
    bad = [r for r in docs_data if r["application_id"] not in app_ids]
    if bad:
        print(f"[FAIL] Document.application_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] Document.application_id: all valid")

    # Check AffordabilityCheck.application_id
    bad = [r for r in aff_data if r["application_id"] not in app_ids]
    if bad:
        print(f"[FAIL] AffordabilityCheck.application_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] AffordabilityCheck.application_id: all valid")

    # Check Decision.application_id
    bad = [r for r in dec_data if r["application_id"] not in app_ids]
    if bad:
        print(f"[FAIL] Decision.application_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] Decision.application_id: all valid")

    # Check RepaymentSchedule.application_id
    bad = [r for r in sch_data if r["application_id"] not in app_ids]
    if bad:
        print(f"[FAIL] RepaymentSchedule.application_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] RepaymentSchedule.application_id: all valid")

    # Check ApplicationEvent.application_id
    bad = [r for r in evt_data if r["application_id"] not in app_ids]
    if bad:
        print(f"[FAIL] ApplicationEvent.application_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] ApplicationEvent.application_id: all valid")

    # Check Disbursement.application_id
    bad = [r for r in dis_data if r["application_id"] not in app_ids]
    if bad:
        print(f"[FAIL] Disbursement.application_id: {len(bad)} invalid FKs")
        all_ok = False
    else:
        print(f"[OK] Disbursement.application_id: all valid")

    return all_ok

def validate_enums():
    """Validate enum fields."""
    print("\n=== ENUM VALIDATION ===")

    apps_data = load_csv("data/loan_applications.csv")
    empls_data = load_csv("data/employments.csv")
    incomes_data = load_csv("data/incomes.csv")
    facilities_data = load_csv("data/credit_facilities.csv")
    docs_data = load_csv("data/documents.csv")
    aff_data = load_csv("data/affordability_checks.csv")
    dec_data = load_csv("data/decisions.csv")

    all_ok = True

    valid_app_status = {"DRAFT", "SUBMITTED", "UNDER_REVIEW", "HOLD", "APPROVED", "REJECTED", "MANUAL_REVIEW", "APPROVED_READY_DISBURSEMENT", "DISBURSED", "CLOSED"}
    bad = [r for r in apps_data if r["current_status"] not in valid_app_status]
    if bad:
        print(f"[FAIL] LoanApplication.current_status: {len(bad)} invalid")
        all_ok = False
    else:
        print(f"[OK] LoanApplication.current_status: all valid")

    valid_emp_status = {"EMPLOYED", "SELF_EMPLOYED", "UNEMPLOYED", "RETIRED"}
    bad = [r for r in empls_data if r["employment_status"] not in valid_emp_status]
    if bad:
        print(f"[FAIL] Employment.employment_status: {len(bad)} invalid")
        all_ok = False
    else:
        print(f"[OK] Employment.employment_status: all valid")

    valid_verify = {"VERIFIED", "UNVERIFIED", "PENDING"}
    bad = [r for r in empls_data if r["verified_status"] not in valid_verify]
    if bad:
        print(f"[FAIL] Employment.verified_status: {len(bad)} invalid")
        all_ok = False
    else:
        print(f"[OK] Employment.verified_status: all valid")

    valid_income_type = {"SALARY", "BONUS", "COMMISSION", "SELF_EMPLOYED", "RENTAL", "OTHER"}
    bad = [r for r in incomes_data if r["income_type"] not in valid_income_type]
    if bad:
        print(f"[FAIL] IncomeRecord.income_type: {len(bad)} invalid")
        all_ok = False
    else:
        print(f"[OK] IncomeRecord.income_type: all valid")

    valid_facility = {"CREDIT_CARD", "PERSONAL_LOAN", "MORTGAGE", "AUTO_LOAN", "OTHER"}
    bad = [r for r in facilities_data if r["facility_type"] not in valid_facility]
    if bad:
        print(f"[FAIL] CreditFacility.facility_type: {len(bad)} invalid")
        all_ok = False
    else:
        print(f"[OK] CreditFacility.facility_type: all valid")

    valid_doc_type = {"ID_PROOF", "ADDRESS_PROOF", "INCOME_PROOF", "EMPLOYMENT_LETTER", "BANK_STATEMENT", "TAX_RETURN", "OTHER"}
    bad = [r for r in docs_data if r["document_type"] not in valid_doc_type]
    if bad:
        print(f"[FAIL] Document.document_type: {len(bad)} invalid")
        all_ok = False
    else:
        print(f"[OK] Document.document_type: all valid")

    valid_doc_status = {"PENDING", "SUBMITTED", "VERIFIED", "REJECTED", "MISSING"}
    bad = [r for r in docs_data if r["document_status"] not in valid_doc_status]
    if bad:
        print(f"[FAIL] Document.document_status: {len(bad)} invalid")
        all_ok = False
    else:
        print(f"[OK] Document.document_status: all valid")

    valid_aff_status = {"AFFORDABLE", "MARGINAL", "NOT_AFFORDABLE"}
    bad = [r for r in aff_data if r["affordability_status"] not in valid_aff_status]
    if bad:
        print(f"[FAIL] AffordabilityCheck.affordability_status: {len(bad)} invalid")
        all_ok = False
    else:
        print(f"[OK] AffordabilityCheck.affordability_status: all valid")

    valid_decision = {"APPROVE", "REJECT", "MANUAL_REVIEW"}
    bad = [r for r in dec_data if r["decision_outcome"] not in valid_decision]
    if bad:
        print(f"[FAIL] Decision.decision_outcome: {len(bad)} invalid")
        all_ok = False
    else:
        print(f"[OK] Decision.decision_outcome: all valid")

    return all_ok

def validate_schedules():
    """Validate repayment schedule reconciliation."""
    print("\n=== REPAYMENT SCHEDULE VALIDATION ===")

    apps_data = load_csv("data/loan_applications.csv")
    sch_data = load_csv("data/repayment_schedules.csv")

    all_ok = True

    # Group schedules by application
    schedules_by_app = {}
    for row in sch_data:
        app_id = row["application_id"]
        if app_id not in schedules_by_app:
            schedules_by_app[app_id] = []
        schedules_by_app[app_id].append(row)

    # Check each application has schedules only if APPROVED
    app_by_id = {row["application_id"]: row for row in apps_data}

    for app_id, scheds in schedules_by_app.items():
        app = app_by_id.get(app_id)
        if app and app["current_status"] != "APPROVED":
            print(f"[FAIL] {app_id}: has schedules but status is {app['current_status']}")
            all_ok = False

    # Check principal reconciliation
    bad_apps = []
    for app_id, scheds in schedules_by_app.items():
        app = app_by_id.get(app_id)
        if not app:
            continue

        total_principal = sum(Decimal(s["principal_amount"]) for s in scheds)
        requested = Decimal(str(app["requested_amount"]))

        if abs(total_principal - requested) > TOLERANCE:
            bad_apps.append((app_id, total_principal, requested))

    if bad_apps:
        print(f"[FAIL] {len(bad_apps)} schedules with principal mismatch")
        for app_id, total, requested in bad_apps[:3]:
            print(f"  {app_id}: sum={float(total):.2f}, requested={float(requested):.2f}")
        all_ok = False
    else:
        print(f"[OK] {len(schedules_by_app)} applications: principal reconciled")

    return all_ok

def validate_lifecycles():
    """Validate application lifecycle and decision consistency."""
    print("\n=== LIFECYCLE VALIDATION ===")

    apps_data = load_csv("data/loan_applications.csv")
    dec_data = load_csv("data/decisions.csv")
    aff_data = load_csv("data/affordability_checks.csv")
    evt_data = load_csv("data/application_events.csv")

    all_ok = True

    apps_by_id = {row["application_id"]: row for row in apps_data}
    decisions_by_app = {row["application_id"]: row for row in dec_data}
    aff_by_app = {row["application_id"]: row for row in aff_data}

    # Check decision dates >= affordability check dates
    bad = []
    for app_id, dec in decisions_by_app.items():
        aff = aff_by_app.get(app_id)
        if aff and dec["decision_date"] < aff["check_date"]:
            bad.append((app_id, aff["check_date"], dec["decision_date"]))

    if bad:
        print(f"[FAIL] {len(bad)} decisions dated before affordability checks")
        all_ok = False
    else:
        print(f"[OK] All decision dates >= affordability check dates")

    # Check application status aligns with decision outcome
    mismatches = []
    for app_id, app in apps_by_id.items():
        dec = decisions_by_app.get(app_id)
        if not dec:
            continue

        status = app["current_status"]
        outcome = dec["decision_outcome"]

        if outcome == "APPROVE" and status != "APPROVED":
            mismatches.append((app_id, "outcome=APPROVE but status=" + status))
        elif outcome == "REJECT" and status != "REJECTED":
            mismatches.append((app_id, "outcome=REJECT but status=" + status))
        elif outcome == "MANUAL_REVIEW" and status != "MANUAL_REVIEW":
            mismatches.append((app_id, "outcome=MANUAL_REVIEW but status=" + status))

    if mismatches:
        print(f"[FAIL] {len(mismatches)} status/decision outcome mismatches")
        all_ok = False
    else:
        print(f"[OK] All decision outcomes match application status")

    # Check event ordering
    events_by_app = {}
    for row in evt_data:
        app_id = row["application_id"]
        if app_id not in events_by_app:
            events_by_app[app_id] = []
        events_by_app[app_id].append(row)

    bad_ordering = 0
    for app_id, events in events_by_app.items():
        for i in range(len(events) - 1):
            if events[i]["event_date"] > events[i+1]["event_date"]:
                bad_ordering += 1
                break

    if bad_ordering:
        print(f"[FAIL] {bad_ordering} applications with out-of-order events")
        all_ok = False
    else:
        print(f"[OK] All event dates in chronological order")

    return all_ok

def main():
    """Run all validations."""
    print("YottaFlex Loan Risk Platform - Data Validation")
    print("=" * 50)

    results = []
    results.append(validate_primary_keys())
    results.append(validate_foreign_keys())
    results.append(validate_enums())
    results.append(validate_schedules())
    results.append(validate_lifecycles())

    print("\n" + "=" * 50)
    if all(results):
        print("[OK] All validations PASSED")
        return 0
    else:
        print("[FAIL] Some validations FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())

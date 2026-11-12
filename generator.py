#!/usr/bin/env python3
"""
YottaFlex Loan Risk Platform - Synthetic Data Generator
Fixed seed: 20261112, reproducible and deterministic.
"""

import csv
import json
import math
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Configuration
SEED = 20261112
NUM_APPLICANTS = 100  # Starter profile; set to 10000 for full
NUM_APPLICATIONS = 60  # Starter profile; set to 6000 for full
BASE_DATE = datetime(2026, 10, 1)
FINAL_DATE = datetime(2026, 11, 12)

# Products (4 total)
PRODUCTS = [
    {"id": "PROD-0001", "name": "Personal Loan Standard", "min": 50000, "max": 500000, "min_term": 12, "max_term": 60, "rate": 0.085},
    {"id": "PROD-0002", "name": "Personal Loan Premium", "min": 100000, "max": 1000000, "min_term": 12, "max_term": 84, "rate": 0.070},
    {"id": "PROD-0003", "name": "Quick Loan Express", "min": 25000, "max": 250000, "min_term": 6, "max_term": 36, "rate": 0.095},
    {"id": "PROD-0004", "name": "Secured Loan", "min": 75000, "max": 750000, "min_term": 24, "max_term": 120, "rate": 0.060},
]

# Synthetic names and employers (small pool for reproducibility)
FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "Michael", "Jennifer", "William", "Linda"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
EMPLOYERS = ["Acme Corp", "TechFlow Inc", "Global Services Ltd", "Innovate Systems", "Stellar Finance", "Core Industries"]
JOB_TITLES = ["Software Engineer", "Manager", "Analyst", "Specialist", "Coordinator", "Associate"]

class Generator:
    def __init__(self, seed=SEED, num_applicants=NUM_APPLICANTS, num_applications=NUM_APPLICATIONS):
        self.seed = seed
        self.num_applicants = num_applicants
        self.num_applications = num_applications
        random.seed(seed)

        self.applicants = []
        self.employments = []
        self.incomes = []
        self.facilities = []
        self.applications = []
        self.documents = []
        self.affordability_checks = []
        self.decisions = []
        self.schedules = []
        self.events = []
        self.disbursements = []

        self.app_counter = 0
        self.emp_counter = {}
        self.income_counter = {}
        self.cred_counter = {}
        self.doc_counter = {}
        self.aff_counter = {}
        self.dec_counter = {}
        self.sch_counter = {}
        self.evt_counter = {}
        self.dis_counter = {}

        self.anomalies = {"scenarios": [], "ground_truth": []}

    def random_name(self):
        """Generate synthetic full name."""
        return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

    def random_date_between(self, start, end):
        """Random date between start and end."""
        delta = end - start
        return start + timedelta(days=random.randint(0, delta.days))

    def generate_applicants(self):
        """Generate master applicant records."""
        for i in range(1, self.num_applicants + 1):
            app_id = f"APP-2026-{i:06d}"
            dob = self.random_date_between(datetime(1950, 1, 1), datetime(2008, 12, 31)).date()
            created = self.random_date_between(BASE_DATE, FINAL_DATE).date()

            self.applicants.append({
                "applicant_id": app_id,
                "full_name": self.random_name(),
                "date_of_birth": dob.isoformat(),
                "email": f"user{i}@example.com",
                "phone": f"555{1000000 + i:07d}",
                "address_line": f"{random.randint(1, 999)} Main St",
                "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
                "state": random.choice(["NY", "CA", "IL", "TX", "AZ"]),
                "zip_code": f"{random.randint(10000, 99999)}",
                "created_date": created.isoformat(),
            })
            self.emp_counter[app_id] = 0
            self.income_counter[app_id] = 0
            self.cred_counter[app_id] = 0
            self.doc_counter[app_id] = 0

    def generate_employment(self):
        """Generate employment records (1-2 per applicant)."""
        for applicant in self.applicants:
            app_id = applicant["applicant_id"]
            num_jobs = random.choice([1, 1, 1, 2])  # 75% have 1 job

            for j in range(1, num_jobs + 1):
                self.emp_counter[app_id] += 1
                emp_id = f"EMP-{app_id}-{self.emp_counter[app_id]:02d}"
                start = self.random_date_between(datetime(2010, 1, 1), datetime(2024, 12, 31)).date()
                current = random.choice([True, True, True, False])  # 75% current
                end = None if current else start + timedelta(days=random.randint(180, 1800))

                self.employments.append({
                    "employment_id": emp_id,
                    "applicant_id": app_id,
                    "employer_name": random.choice(EMPLOYERS),
                    "job_title": random.choice(JOB_TITLES),
                    "employment_status": "EMPLOYED" if current else "UNEMPLOYED",
                    "start_date": start.isoformat(),
                    "end_date": end.isoformat() if end else None,
                    "verified_status": random.choice(["VERIFIED", "VERIFIED", "VERIFIED", "UNVERIFIED"]),
                    "created_date": FINAL_DATE.date().isoformat(),
                })

    def generate_income(self):
        """Generate income records (1-3 per applicant, mostly VERIFIED)."""
        for applicant in self.applicants:
            app_id = applicant["applicant_id"]

            # Primary income (SALARY, 95% chance)
            if random.random() < 0.95:
                self.income_counter[app_id] += 1
                inc_id = f"INC-{app_id}-{self.income_counter[app_id]:02d}"
                gross = Decimal(random.randint(30, 150)) * Decimal("1000")
                net = gross * Decimal(random.uniform(0.75, 0.90))

                emp_id = None
                for e in self.employments:
                    if e["applicant_id"] == app_id and e["employment_status"] == "EMPLOYED":
                        emp_id = e["employment_id"]
                        break

                self.incomes.append({
                    "income_id": inc_id,
                    "applicant_id": app_id,
                    "employment_id": emp_id,
                    "income_type": "SALARY",
                    "gross_monthly_income": float(gross),
                    "net_monthly_income": float(net),
                    "frequency": "MONTHLY",
                    "verification_status": random.choice(["VERIFIED", "VERIFIED", "VERIFIED", "UNVERIFIED", "PENDING"]),
                    "income_date": (FINAL_DATE - timedelta(days=random.randint(0, 60))).date().isoformat(),
                    "created_date": FINAL_DATE.date().isoformat(),
                })

            # Secondary income (15% of applicants)
            if random.random() < 0.15:
                self.income_counter[app_id] += 1
                inc_id = f"INC-{app_id}-{self.income_counter[app_id]:02d}"
                self.incomes.append({
                    "income_id": inc_id,
                    "applicant_id": app_id,
                    "employment_id": None,
                    "income_type": random.choice(["RENTAL", "COMMISSION", "BONUS"]),
                    "gross_monthly_income": float(Decimal(random.randint(5, 50)) * Decimal("1000")),
                    "net_monthly_income": None,
                    "frequency": "MONTHLY",
                    "verification_status": random.choice(["VERIFIED", "UNVERIFIED", "PENDING"]),
                    "income_date": (FINAL_DATE - timedelta(days=random.randint(0, 90))).date().isoformat(),
                    "created_date": FINAL_DATE.date().isoformat(),
                })

    def generate_credit_facilities(self):
        """Generate existing debt (0-3 per applicant)."""
        for applicant in self.applicants:
            app_id = applicant["applicant_id"]
            num_facilities = random.choice([0, 0, 0, 1, 1, 2, 3])  # Most have 0-1

            for _ in range(num_facilities):
                self.cred_counter[app_id] += 1
                fac_id = f"CRD-{app_id}-{self.cred_counter[app_id]:02d}"
                balance = Decimal(random.randint(5, 200)) * Decimal("1000")
                payment = balance / Decimal(random.randint(12, 48))

                self.facilities.append({
                    "facility_id": fac_id,
                    "applicant_id": app_id,
                    "facility_type": random.choice(["CREDIT_CARD", "PERSONAL_LOAN", "AUTO_LOAN"]),
                    "outstanding_balance": float(balance),
                    "monthly_payment": float(payment),
                    "created_date": FINAL_DATE.date().isoformat(),
                })

    def generate_applications(self):
        """Generate loan applications with linked products and statuses."""
        for i in range(1, self.num_applications + 1):
            applicant = random.choice(self.applicants)
            app_id = applicant["applicant_id"]
            product = random.choice(PRODUCTS)

            loan_id = f"LOAN-2026-{i:06d}"
            req_amount = float(Decimal(random.randint(1, 10)) * Decimal(product["min"]) / Decimal("10"))
            req_amount = max(product["min"], min(req_amount, product["max"]))
            req_term = random.randint(product["min_term"], product["max_term"])
            app_date = self.random_date_between(BASE_DATE, FINAL_DATE).date()

            # Randomly assign outcome (60% APPROVED, 20% REJECTED, 20% MANUAL_REVIEW)
            outcome_rand = random.random()
            if outcome_rand < 0.60:
                status = "APPROVED"
            elif outcome_rand < 0.80:
                status = "REJECTED"
            else:
                status = "MANUAL_REVIEW"

            self.applications.append({
                "application_id": loan_id,
                "applicant_id": app_id,
                "product_id": product["id"],
                "requested_amount": req_amount,
                "requested_term_months": req_term,
                "application_date": app_date.isoformat(),
                "current_status": status,
                "created_date": app_date.isoformat(),
            })

    def generate_documents(self):
        """Generate document records (90% submissions)."""
        doc_types = ["ID_PROOF", "ADDRESS_PROOF", "INCOME_PROOF", "EMPLOYMENT_LETTER"]

        for app in self.applications:
            app_id = app["application_id"]
            if app_id not in self.doc_counter:
                self.doc_counter[app_id] = 0
            for doc_type in doc_types:
                self.doc_counter[app_id] += 1
                doc_id = f"DOC-{app_id}-{self.doc_counter[app_id]:03d}"

                if random.random() < 0.90:
                    status = random.choice(["VERIFIED", "VERIFIED", "VERIFIED", "PENDING", "REJECTED"])
                    submission = (datetime.fromisoformat(app["application_date"]) + timedelta(days=random.randint(0, 5))).date().isoformat()
                else:
                    status = "MISSING"
                    submission = None

                self.documents.append({
                    "document_id": doc_id,
                    "application_id": app_id,
                    "document_type": doc_type,
                    "document_status": status,
                    "submission_date": submission,
                    "created_date": FINAL_DATE.date().isoformat(),
                })

    def calculate_emi(self, principal, annual_rate, months):
        """Calculate EMI using standard formula."""
        if annual_rate == 0 or months == 0:
            return principal / months if months > 0 else 0

        monthly_rate = annual_rate / 12
        emi = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        return emi

    def generate_affordability_checks(self):
        """Calculate affordability metrics for all applications."""
        for app in self.applications:
            loan_id = app["application_id"]
            app_id = app["applicant_id"]

            # Get total verified monthly income
            total_income = 0
            has_verified = False
            for inc in self.incomes:
                if inc["applicant_id"] == app_id and inc["verification_status"] == "VERIFIED" and inc["frequency"] == "MONTHLY":
                    total_income += inc["gross_monthly_income"]
                    has_verified = True

            # Get total existing obligations
            total_obligations = sum(f["monthly_payment"] for f in self.facilities if f["applicant_id"] == app_id)

            # Calculate proposed EMI
            product = next(p for p in PRODUCTS if p["id"] == app["product_id"])
            emi = self.calculate_emi(app["requested_amount"], product["rate"], app["requested_term_months"])

            # Calculate DTI
            total_with_loan = total_obligations + emi
            dti = total_with_loan / total_income if total_income > 0 else 1.0

            if dti <= 0.40:
                aff_status = "AFFORDABLE"
            elif dti <= 0.50:
                aff_status = "MARGINAL"
            else:
                aff_status = "NOT_AFFORDABLE"

            self.aff_counter[loan_id] = 1
            aff_id = f"AFD-{loan_id}-01"

            self.affordability_checks.append({
                "check_id": aff_id,
                "application_id": loan_id,
                "total_monthly_income": total_income,
                "total_existing_obligations": total_obligations,
                "proposed_emi": round(emi, 2),
                "total_obligations_with_loan": round(total_with_loan, 2),
                "debt_to_income_ratio": round(dti, 3),
                "affordability_status": aff_status,
                "check_date": FINAL_DATE.date().isoformat(),
                "created_date": FINAL_DATE.date().isoformat(),
            })

    def generate_decisions(self):
        """Apply decision rules deterministically."""
        for app in self.applications:
            loan_id = app["application_id"]
            product = next(p for p in PRODUCTS if p["id"] == app["product_id"])
            aff = next(a for a in self.affordability_checks if a["application_id"] == loan_id)

            # Get documents
            docs = [d for d in self.documents if d["application_id"] == loan_id]

            # Get income
            incomes = [i for i in self.incomes if i["applicant_id"] == app["applicant_id"]]

            # Apply rules in precedence order
            triggered_rules = []
            outcome = "APPROVE"
            reason = "NO_ISSUES"

            # Rule 1: Term range
            if app["requested_term_months"] < product["min_term"] or app["requested_term_months"] > product["max_term"]:
                triggered_rules.append("RULE_TERM_RANGE")
                outcome = "REJECT"
                reason = "TERM_OUT_OF_RANGE"

            # Rule 2: Amount range
            elif app["requested_amount"] < product["min"] or app["requested_amount"] > product["max"]:
                triggered_rules.append("RULE_AMOUNT_RANGE")
                outcome = "REJECT"
                reason = "AMOUNT_OUT_OF_RANGE"

            # Rule 3: Missing income
            elif not incomes or all(i["verification_status"] != "VERIFIED" for i in incomes):
                triggered_rules.append("RULE_MISSING_INCOME")
                outcome = "MANUAL_REVIEW"
                reason = "NO_VERIFIED_INCOME"

            # Rule 4: Unverified income
            elif any(i["verification_status"] in ["UNVERIFIED", "PENDING"] for i in incomes):
                triggered_rules.append("RULE_UNVERIFIED_INCOME")
                outcome = "MANUAL_REVIEW"
                reason = "INCOME_UNVERIFIED"

            # Rule 5: Missing critical documents
            elif any(d["document_status"] == "MISSING" or d["document_status"] == "REJECTED"
                     for d in docs if d["document_type"] in ["ID_PROOF", "INCOME_PROOF"]):
                triggered_rules.append("RULE_MISSING_DOCUMENTS")
                outcome = "MANUAL_REVIEW"
                reason = "CRITICAL_DOCS_MISSING"

            # Rule 6-8: DTI checks (only if previous checks pass)
            else:
                if aff["affordability_status"] == "AFFORDABLE":
                    triggered_rules.append("RULE_DTI_ACCEPTABLE")
                    outcome = "APPROVE"
                    reason = "DTI_ACCEPTABLE"
                elif aff["affordability_status"] == "MARGINAL":
                    triggered_rules.append("RULE_DTI_MARGINAL")
                    outcome = "MANUAL_REVIEW"
                    reason = "DTI_MARGINAL"
                else:
                    triggered_rules.append("RULE_DTI_HIGH")
                    outcome = "REJECT"
                    reason = "DTI_TOO_HIGH"

            # Update application status to match decision
            status_map = {"APPROVE": "APPROVED", "REJECT": "REJECTED", "MANUAL_REVIEW": "MANUAL_REVIEW"}
            app["current_status"] = status_map[outcome]

            self.dec_counter[loan_id] = 1
            dec_id = f"DEC-{loan_id}-01"

            self.decisions.append({
                "decision_id": dec_id,
                "application_id": loan_id,
                "decision_outcome": outcome,
                "primary_reason": reason,
                "triggered_rules": json.dumps(triggered_rules),
                "decision_date": FINAL_DATE.date().isoformat(),
                "created_date": FINAL_DATE.date().isoformat(),
            })

    def generate_repayment_schedules(self):
        """Generate schedules only for APPROVED applications."""
        for app in self.applications:
            if app["current_status"] != "APPROVED":
                continue

            loan_id = app["application_id"]
            product = next(p for p in PRODUCTS if p["id"] == app["product_id"])

            principal = Decimal(str(app["requested_amount"]))
            months = app["requested_term_months"]
            monthly_rate = Decimal(str(product["rate"])) / Decimal("12")

            if monthly_rate == 0:
                emi = principal / Decimal(months)
            else:
                factor = (1 + monthly_rate) ** months
                emi = principal * (monthly_rate * factor) / (factor - 1)

            balance = principal
            app_date = datetime.fromisoformat(app["application_date"])
            total_principal_paid = Decimal("0")

            for month in range(1, months + 1):
                self.sch_counter[loan_id] = month
                sch_id = f"SCH-{loan_id}-{month:03d}"
                payment_date = (app_date + timedelta(days=30 * month)).date()

                interest = balance * monthly_rate
                principal_payment = emi - interest

                # Final adjustment: ensure principal sums exactly
                if month == months:
                    principal_payment = principal - total_principal_paid
                else:
                    total_principal_paid += principal_payment

                balance -= principal_payment

                self.schedules.append({
                    "schedule_id": sch_id,
                    "application_id": loan_id,
                    "installment_number": month,
                    "payment_date": payment_date.isoformat(),
                    "principal_amount": float(round(principal_payment, 2)),
                    "interest_amount": float(round(interest, 2)),
                    "total_payment": float(round(principal_payment + interest, 2)),
                    "remaining_balance": max(0, float(round(balance, 2))),
                    "created_date": FINAL_DATE.date().isoformat(),
                })

    def generate_events(self):
        """Generate append-only application events."""
        for app in self.applications:
            loan_id = app["application_id"]
            app_date = datetime.fromisoformat(app["application_date"]).date()

            event_seq = 1

            # Submission event
            self.evt_counter[loan_id] = event_seq
            evt_id = f"EVT-{loan_id}-{event_seq:04d}"
            self.events.append({
                "event_id": evt_id,
                "application_id": loan_id,
                "event_type": "SUBMITTED",
                "event_date": app_date.isoformat(),
                "created_date": FINAL_DATE.date().isoformat(),
            })
            event_seq += 1

            # Affordability check event
            self.evt_counter[loan_id] = event_seq
            evt_id = f"EVT-{loan_id}-{event_seq:04d}"
            self.events.append({
                "event_id": evt_id,
                "application_id": loan_id,
                "event_type": "AFFORDABILITY_CHECK",
                "event_date": app_date.isoformat(),
                "created_date": FINAL_DATE.date().isoformat(),
            })
            event_seq += 1

            # Decision event
            decision = next(d for d in self.decisions if d["application_id"] == loan_id)
            event_type_map = {
                "APPROVE": "DECISION",
                "REJECT": "DECISION",
                "MANUAL_REVIEW": "MANUAL_REVIEW_ASSIGNED",
            }

            self.evt_counter[loan_id] = event_seq
            evt_id = f"EVT-{loan_id}-{event_seq:04d}"
            self.events.append({
                "event_id": evt_id,
                "application_id": loan_id,
                "event_type": event_type_map.get(decision["decision_outcome"], "DECISION"),
                "event_date": app_date.isoformat(),
                "created_date": FINAL_DATE.date().isoformat(),
            })

    def generate_disbursements(self):
        """Generate disbursement records for APPROVED applications."""
        for app in self.applications:
            if app["current_status"] != "APPROVED":
                continue

            loan_id = app["application_id"]
            self.dis_counter[loan_id] = 1
            dis_id = f"DIS-{loan_id}-01"

            dis_date = (datetime.fromisoformat(app["application_date"]) + timedelta(days=random.randint(3, 10))).date()

            self.disbursements.append({
                "disbursement_id": dis_id,
                "application_id": loan_id,
                "disbursement_date": dis_date.isoformat(),
                "amount_disbursed": app["requested_amount"],
                "disbursement_status": "COMPLETED",
                "created_date": FINAL_DATE.date().isoformat(),
            })

    def inject_anomalies(self):
        """Inject 5 anomaly scenarios into baseline."""
        # Scenario 1: TERM_OUTSIDE_PRODUCT_RANGE
        approved_apps = [a for a in self.applications if a["current_status"] == "APPROVED"]
        for app in approved_apps[:min(5, len(approved_apps))]:
            product = next(p for p in PRODUCTS if p["id"] == app["product_id"])
            anomaly_app = app.copy()
            anomaly_app["application_id"] = f"LOAN-2026-{90000 + len(self.anomalies['scenarios']):06d}"
            anomaly_app["requested_term_months"] = product["max_term"] + 12
            self.applications.append(anomaly_app)
            self.anomalies["scenarios"].append({"app_id": anomaly_app["application_id"], "type": "TERM_OUTSIDE_PRODUCT_RANGE"})
            self.anomalies["ground_truth"].append({"application_id": anomaly_app["application_id"], "issue_type": "TERM_OUTSIDE_PRODUCT_RANGE"})

    def export_csv(self, output_dir="data"):
        """Export all tables to CSV."""
        import os
        os.makedirs(output_dir, exist_ok=True)

        exports = [
            ("loan_products.csv", [{"product_id": p["id"], "product_name": p["name"], "min_loan": p["min"],
                                    "max_loan": p["max"], "min_term": p["min_term"], "max_term": p["max_term"],
                                    "rate": p["rate"], "created_date": FINAL_DATE.date().isoformat()} for p in PRODUCTS]),
            ("applicants.csv", self.applicants),
            ("employments.csv", self.employments),
            ("incomes.csv", self.incomes),
            ("credit_facilities.csv", self.facilities),
            ("loan_applications.csv", self.applications),
            ("documents.csv", self.documents),
            ("affordability_checks.csv", self.affordability_checks),
            ("decisions.csv", self.decisions),
            ("repayment_schedules.csv", self.schedules),
            ("application_events.csv", self.events),
            ("disbursements.csv", self.disbursements),
            ("ground_truth.csv", self.anomalies["ground_truth"]),
        ]

        for filename, data in exports:
            if not data:
                continue
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"[OK] {filename}: {len(data)} rows")

    def run(self):
        """Execute full generation pipeline."""
        print("Generating synthetic loan data...")
        self.generate_applicants()
        print(f"[OK] {len(self.applicants)} applicants")

        self.generate_employment()
        print(f"[OK] {len(self.employments)} employment records")

        self.generate_income()
        print(f"[OK] {len(self.incomes)} income records")

        self.generate_credit_facilities()
        print(f"[OK] {len(self.facilities)} credit facilities")

        self.generate_applications()
        print(f"[OK] {len(self.applications)} loan applications")

        self.generate_documents()
        print(f"[OK] {len(self.documents)} documents")

        self.generate_affordability_checks()
        print(f"[OK] {len(self.affordability_checks)} affordability checks")

        self.generate_decisions()
        print(f"[OK] {len(self.decisions)} decisions")

        self.generate_repayment_schedules()
        print(f"[OK] {len(self.schedules)} schedule records")

        self.generate_events()
        print(f"[OK] {len(self.events)} application events")

        self.generate_disbursements()
        print(f"[OK] {len(self.disbursements)} disbursements")

        self.inject_anomalies()
        print(f"[OK] {len(self.anomalies['scenarios'])} anomalies injected")

        return self

if __name__ == "__main__":
    gen = Generator()
    gen.run()
    gen.export_csv()
    print("\n[OK] Generation complete!")

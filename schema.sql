-- YottaFlex Loan Risk Platform - Schema Definition
-- Fixed seed: 20261112, reproducible synthetic data
-- All IDs are deterministically generated, never auto-increment

CREATE TABLE LoanProduct (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    min_loan_amount DECIMAL(15,2) NOT NULL,
    max_loan_amount DECIMAL(15,2) NOT NULL,
    min_term_months INT NOT NULL,
    max_term_months INT NOT NULL,
    base_interest_rate DECIMAL(5,3) NOT NULL,
    created_date DATE NOT NULL
);

CREATE TABLE Applicant (
    applicant_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    email TEXT,
    phone TEXT,
    address_line TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    created_date DATE NOT NULL
);

CREATE TABLE Employment (
    employment_id TEXT PRIMARY KEY,
    applicant_id TEXT NOT NULL,
    employer_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    employment_status TEXT NOT NULL CHECK (employment_status IN ('EMPLOYED', 'SELF_EMPLOYED', 'UNEMPLOYED', 'RETIRED')),
    start_date DATE NOT NULL,
    end_date DATE,
    verified_status TEXT NOT NULL CHECK (verified_status IN ('VERIFIED', 'UNVERIFIED', 'PENDING')),
    created_date DATE NOT NULL,
    FOREIGN KEY (applicant_id) REFERENCES Applicant(applicant_id)
);

CREATE TABLE IncomeRecord (
    income_id TEXT PRIMARY KEY,
    applicant_id TEXT NOT NULL,
    employment_id TEXT,
    income_type TEXT NOT NULL CHECK (income_type IN ('SALARY', 'BONUS', 'COMMISSION', 'SELF_EMPLOYED', 'RENTAL', 'OTHER')),
    gross_monthly_income DECIMAL(15,2) NOT NULL,
    net_monthly_income DECIMAL(15,2),
    frequency TEXT NOT NULL CHECK (frequency IN ('MONTHLY', 'QUARTERLY', 'ANNUAL')),
    verification_status TEXT NOT NULL CHECK (verification_status IN ('VERIFIED', 'UNVERIFIED', 'PENDING')),
    income_date DATE NOT NULL,
    created_date DATE NOT NULL,
    FOREIGN KEY (applicant_id) REFERENCES Applicant(applicant_id),
    FOREIGN KEY (employment_id) REFERENCES Employment(employment_id)
);

CREATE TABLE CreditFacility (
    facility_id TEXT PRIMARY KEY,
    applicant_id TEXT NOT NULL,
    facility_type TEXT NOT NULL CHECK (facility_type IN ('CREDIT_CARD', 'PERSONAL_LOAN', 'MORTGAGE', 'AUTO_LOAN', 'OTHER')),
    outstanding_balance DECIMAL(15,2) NOT NULL,
    monthly_payment DECIMAL(15,2) NOT NULL,
    created_date DATE NOT NULL,
    FOREIGN KEY (applicant_id) REFERENCES Applicant(applicant_id)
);

CREATE TABLE LoanApplication (
    application_id TEXT PRIMARY KEY,
    applicant_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    requested_amount DECIMAL(15,2) NOT NULL,
    requested_term_months INT NOT NULL,
    application_date DATE NOT NULL,
    current_status TEXT NOT NULL CHECK (current_status IN ('DRAFT', 'SUBMITTED', 'UNDER_REVIEW', 'HOLD', 'APPROVED', 'REJECTED', 'MANUAL_REVIEW', 'APPROVED_READY_DISBURSEMENT', 'DISBURSED', 'CLOSED')),
    created_date DATE NOT NULL,
    FOREIGN KEY (applicant_id) REFERENCES Applicant(applicant_id),
    FOREIGN KEY (product_id) REFERENCES LoanProduct(product_id)
);

CREATE TABLE Document (
    document_id TEXT PRIMARY KEY,
    application_id TEXT NOT NULL,
    document_type TEXT NOT NULL CHECK (document_type IN ('ID_PROOF', 'ADDRESS_PROOF', 'INCOME_PROOF', 'EMPLOYMENT_LETTER', 'BANK_STATEMENT', 'TAX_RETURN', 'OTHER')),
    document_status TEXT NOT NULL CHECK (document_status IN ('PENDING', 'SUBMITTED', 'VERIFIED', 'REJECTED', 'MISSING')),
    submission_date DATE,
    created_date DATE NOT NULL,
    FOREIGN KEY (application_id) REFERENCES LoanApplication(application_id)
);

CREATE TABLE AffordabilityCheck (
    check_id TEXT PRIMARY KEY,
    application_id TEXT NOT NULL,
    total_monthly_income DECIMAL(15,2) NOT NULL,
    total_existing_obligations DECIMAL(15,2) NOT NULL,
    proposed_emi DECIMAL(15,2) NOT NULL,
    total_obligations_with_loan DECIMAL(15,2) NOT NULL,
    debt_to_income_ratio DECIMAL(5,3) NOT NULL,
    affordability_status TEXT NOT NULL CHECK (affordability_status IN ('AFFORDABLE', 'MARGINAL', 'NOT_AFFORDABLE')),
    check_date DATE NOT NULL,
    created_date DATE NOT NULL,
    FOREIGN KEY (application_id) REFERENCES LoanApplication(application_id)
);

CREATE TABLE Decision (
    decision_id TEXT PRIMARY KEY,
    application_id TEXT NOT NULL,
    decision_outcome TEXT NOT NULL CHECK (decision_outcome IN ('APPROVE', 'REJECT', 'MANUAL_REVIEW')),
    primary_reason TEXT NOT NULL,
    triggered_rules TEXT NOT NULL,
    decision_date DATE NOT NULL,
    created_date DATE NOT NULL,
    FOREIGN KEY (application_id) REFERENCES LoanApplication(application_id)
);

CREATE TABLE RepaymentSchedule (
    schedule_id TEXT PRIMARY KEY,
    application_id TEXT NOT NULL,
    installment_number INT NOT NULL,
    payment_date DATE NOT NULL,
    principal_amount DECIMAL(15,2) NOT NULL,
    interest_amount DECIMAL(15,2) NOT NULL,
    total_payment DECIMAL(15,2) NOT NULL,
    remaining_balance DECIMAL(15,2) NOT NULL,
    created_date DATE NOT NULL,
    FOREIGN KEY (application_id) REFERENCES LoanApplication(application_id)
);

CREATE TABLE ApplicationEvent (
    event_id TEXT PRIMARY KEY,
    application_id TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('SUBMITTED', 'AFFORDABILITY_CHECK', 'DECISION', 'APPROVAL', 'REJECTION', 'MANUAL_REVIEW_ASSIGNED', 'HOLD_PLACED', 'HOLD_RELEASED')),
    event_date DATE NOT NULL,
    created_date DATE NOT NULL,
    FOREIGN KEY (application_id) REFERENCES LoanApplication(application_id)
);

CREATE TABLE Disbursement (
    disbursement_id TEXT PRIMARY KEY,
    application_id TEXT NOT NULL,
    disbursement_date DATE NOT NULL,
    amount_disbursed DECIMAL(15,2) NOT NULL,
    disbursement_status TEXT NOT NULL CHECK (disbursement_status IN ('PENDING', 'COMPLETED', 'FAILED')),
    created_date DATE NOT NULL,
    FOREIGN KEY (application_id) REFERENCES LoanApplication(application_id)
);

import numpy as np

class Loan:
    def __init__(self, lender, borrower, amount, interest_rate, term):
        self.lender = lender
        self.borrower = borrower
        self.amount = amount
        self.interest_rate = interest_rate
        self.term = term
        self.balance = amount
        self.payments_made = 0
        self.missed_payments = 0
        self.is_active = True
        self.total_interest_paid = 0

    def reset(self):
        self.balance = self.amount
        self.payments_made = 0
        self.missed_payments = 0
        self.is_active = True
        self.total_interest_paid = 0

    def monthly_payment(self):
        r = self.interest_rate / 12
        return (self.amount * r * (1 + r) ** self.term) / ((1 + r) ** self.term - 1)

    def make_payment(self):
        if self.is_active:
            payment = self.monthly_payment()
            if self.borrower.make_payment(self):
                self.balance -= payment
                self.payments_made += 1
                interest_portion = self.balance * (self.interest_rate / 12)
                self.total_interest_paid += interest_portion
                if self.balance <= 0:
                    self.is_active = False
                return True
            else:
                self.missed_payments += 1
                return False
        return False

    def is_defaulted(self):
        return self.missed_payments >= 3 or self.borrower.debt_to_income_ratio() > 0.6

    def current_value(self):
        if self.is_defaulted():
            return self.balance * 0.5
        else:
            remaining_payments = self.term - self.payments_made
            return self.monthly_payment() * remaining_payments

    def risk_score(self):
        if self.is_defaulted():
            return 1.0
        
        dti_ratio = self.borrower.debt_to_income_ratio()
        payment_history = self.missed_payments / (self.payments_made + self.missed_payments + 1)
        credit_score_factor = 1 - (self.borrower.credit_score - 300) / 550
        term_factor = self.term / 60
        
        risk_score = (dti_ratio * 0.3 + payment_history * 0.3 + credit_score_factor * 0.2 + term_factor * 0.2)
        return min(risk_score, 1.0)

    def expected_return(self):
        if self.is_defaulted():
            return -self.balance * 0.5
        
        total_expected_payments = self.monthly_payment() * (self.term - self.payments_made)
        expected_loss = total_expected_payments * self.risk_score()
        return total_expected_payments - expected_loss - (self.balance - self.amount)

    def total_interest(self):
        return self.monthly_payment() * self.term - self.amount

    def __str__(self):
        return f"Loan: Amount=${self.amount}, Interest={self.interest_rate:.2%}, Term={self.term} months, Balance=${self.balance:.2f}, Risk Score={self.risk_score():.2f}"
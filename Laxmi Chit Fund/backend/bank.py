import datetime
from backend.database_utils import save_client_to_db
from backend.db_transaction import save_transaction, save_repayment
from backend.client import Client
from backend.database_utils import load_clients_from_db
from backend.database_utils import update_client_in_db

class Bank:
    def __init__(self):
        self.database = load_clients_from_db()
        self.current_client = None

    def client_login(self):
        uname = input("Username: ")
        pin = input("PIN: ")
        for c in self.database:
            if c.username == uname and c.pin == pin:
                self.current_client = c
                print(f"Welcome, {c.name}!")
                return
        print("Invalid login.")

    def logout_client(self):
        if self.current_client:
            print(f"Goodbye, {self.current_client.name}!")
        self.current_client = None

    def add_client(self):
        c = Client()
        c.client_details()
        self.database.append(c)
        save_client_to_db(c)
        print("New Client added.")

    def check_balance(self):
        if self.current_client:
            print(f"Balance: ₹{self.current_client.open_bal:.2f}")
        else:
            print("Login required.")

    def credit(self):
        if self.current_client:
            amt = float(input("Amount to credit: ₹"))
            self.current_client.open_bal += amt
            today = datetime.date.today()
            self.current_client.transactions.append(("Credit", amt, today))
            save_transaction(self.current_client.account_number, "Credit", amt, today)
            update_client_in_db(self.current_client)  # ✅ Update DB
            print("Credited.")
        else:
            print("Login required.")


    def debit(self):
        if self.current_client:
            amt = float(input("Amount to debit: ₹"))
            if amt <= self.current_client.open_bal:
                self.current_client.open_bal -= amt
                today = datetime.date.today()
                self.current_client.transactions.append(("Debit", amt, today))
                save_transaction(self.current_client.account_number, "Debit", amt, today)
                update_client_in_db(self.current_client)  # ✅
                print("Debited.")
            else:
                print("Insufficient balance.")
        else:
            print("Login required.")

    def delete_account(self):
        if self.current_client:
            self.database.remove(self.current_client)
            print("Account deleted.")
            self.logout_client()
        else:
            print("Login required.")

    def export_data(self, fname="client_data.txt"):
        with open(fname, "w") as f:
            for c in self.database:
                f.write(f"{c.name},{c.id},{c.open_bal}\n")
        print(f"Exported to {fname}")

    def apply_interest(self):
        rate = float(input("Interest rate %: "))
        for c in self.database:
            interest = c.open_bal * rate / 100
            c.open_bal += interest
            c.transactions.append(("Interest", interest, datetime.date.today()))
        print("Interest applied.")

    def apply_loan_interest(self):
        rate = float(input("Loan interest rate %: "))
        for c in self.database:
            if c.loan_balance > 0:
                interest = c.loan_balance * rate / 100
                c.loan_balance += interest
        print("Loan interest applied.")

    def request_loan(self):
        if self.current_client:
            if self.current_client.loan_balance > 0:
                return print("Existing loan active.")
            amt = float(input("Loan amount: ₹"))
            self.current_client.loan_request = amt
            print("Loan requested.")
        else:
            print("Login required.")

    def verify_details(self):
        if self.current_client:
            print("----- Personal Details -----")
            self.current_client.show_client_details()
        else:
            print("Login required.")

    def repay_loan(self):
        if self.current_client:
            c = self.current_client

            if c.loan_balance <= 0:
                return print("No outstanding loan.")

            amt = float(input(f"Repay amount (₹{c.loan_balance:.2f} due): ₹"))
            if amt > c.open_bal:
                return print("Insufficient balance.")

            c.loan_balance -= amt
            c.open_bal -= amt
            today = datetime.date.today()

            c.repayment_history.append((amt, today))
            c.transactions.append(("Loan Repayment", amt, today))

            save_transaction(c.account_number, "Loan Repayment", amt, today)
            save_repayment(c.account_number, amt, today)
            update_client_in_db(c)

            if c.loan_balance <= 0:
                c.loan_balance = 0
                print("Loan fully repaid.")
            else:
                print("Part repayment done.")
        else:
            print("Login required.")

    def view_repayment_history(self):
        if self.current_client:
            c = self.current_client
            if not c.repayment_history:
                return print("No repayment history found.")
            print(f"--- Repayment History for {c.name} ---")
            for amt, date in c.repayment_history:
                print(f"₹{amt:.2f} on {date}")
        else:
            print("Login required.")

    def auto_deduct_emi(self):
        today = datetime.date.today()

        for c in self.database:
            if c.loan_balance > 0 and c.loan_due_date and today >= c.loan_due_date:
                print(f"\nProcessing EMI for {c.name} (A/C: {c.account_number})")

                if c.open_bal >= c.loan_emi:
                    c.open_bal -= c.loan_emi
                    c.loan_balance -= c.loan_emi
                    c.repayment_history.append((c.loan_emi, today))
                    c.transactions.append(("EMI Deduction", c.loan_emi, today))

                    save_transaction(c.account_number, "EMI Deduction", c.loan_emi, today)
                    save_repayment(c.account_number, c.loan_emi, today)
                    update_client_in_db(c)

                    print(f"✅ EMI ₹{c.loan_emi:.2f} deducted from {c.name}")

                    if c.loan_balance <= 0:
                        c.loan_balance = 0
                        print(f"🎉 {c.name} has fully repaid the loan.")
                else:
                    print(f"⚠️  {c.name} has insufficient balance for EMI.")

                next_month = today.replace(day=28) + datetime.timedelta(days=4)
                c.loan_due_date = next_month.replace(day=1)

        print("✅ Monthly EMI deduction process completed.")


    def change_pin(self):
        if self.current_client:
            old = input("Enter old PIN: ")
            if old != self.current_client.pin:
                return print("❌ Incorrect PIN.")

            self.current_client.set_pin()  # 🔐 New PIN is set
            update_client_in_db(self.current_client)  # ✅ Update DB with new PIN
            print("✅ PIN updated successfully.")
        else:
            print("Login required.")

    def view_account_statement(self):
        if self.current_client:
            if not self.current_client.transactions:
                print("No transactions yet.")
                return
            print(f"--- Statement for {self.current_client.name} ---")
            for type_, amt, date in self.current_client.transactions:
                print(f"{date}: {type_} ₹{amt:.2f}")
        else:
            print("Login required.")

    def view_notifications(self):
        if self.current_client:
            if not self.current_client.notifications:
                print("No new notifications.")
            else:
                print("--- Notifications ---")
                for note in self.current_client.notifications:
                    print(f"- {note}")
                self.current_client.notifications.clear()
        else:
            print("Login required.")
import datetime

class Admin:
    def __init__(self, bank):
        self.admin_id = "admin"
        self.admin_password = "admin"
        self.is_logged_in = False
        self.bank = bank

    def admin_login(self):
        uid = input("Enter username: ").lower()
        pwd = input("Enter password: ").lower()
        if uid == self.admin_id and pwd == self.admin_password:
            self.is_logged_in = True
            print("---------- Access Granted ----------")
        else:
            print("---------- Access Denied ----------")
        return self.is_logged_in

    def show_database(self):
        if not self.is_logged_in:
            return print("Admin access required.")
        if not self.bank.database:
            return print("No clients in the database.")
        print("----- All Client Details -----")
        for c in self.bank.database:
            c.show_client_details()

    def delete_any_account(self):
        if not self.is_logged_in:
            return print("Admin access required.")
        aad = int(input("Enter aadhar number to delete: "))
        for c in self.bank.database:
            if c.id == aad:
                self.bank.database.remove(c)
                return print("Account deleted.")
        print("Client not found.")

    def review_loans(self):
        if not self.is_logged_in:
            return print("Admin access required.")
        pend = [c for c in self.bank.database if c.loan_request]
        if not pend:
            return print("No pending loans.")
        for c in pend:
            print(f"\n{c.name} requested loan ₹{c.loan_request}")
            max_allowed = c.open_bal * 5
            if c.loan_request > max_allowed:
                print(f"Exceeded limit ₹{max_allowed}, auto-rejected.")
                c.loan_request = None
                continue
            if input("Approve? (y/n): ").lower() == 'y':
                c.loan_balance = c.loan_request
                c.open_bal += c.loan_request
                c.loan_approved = True
                c.loan_due_date = datetime.date.today().replace(day=1)
                c.loan_emi = (c.loan_balance * 1.10) / 12
                print(f"Approved. ₹{c.loan_balance} added to balance. EMI: ₹{c.loan_emi:.2f}")
            else:
                print("Loan rejected.")
            c.loan_request = None

    def view_all_repayment_histories(self):
        if not self.is_logged_in:
            print("Admin access required.")
            return
        print("\n----- Repayment Histories of All Clients -----")
        for c in self.bank.database:
            print(f"\nClient: {c.name} | Aadhar: {c.id}")
            if c.repayment_history:
                for amt, date in c.repayment_history:
                    print(f"  ₹{amt:.2f} on {date}")
            else:
                print("  No repayments yet.")
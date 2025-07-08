import random

class Client:
    def __init__(self):
        self.account_number = random.randint(10**13, 10**14 - 1)
        self.username = None
        self.pin = None
        self.loan_request = None
        self.loan_approved = False
        self.loan_balance = 0.0
        self.loan_emi = 0.0
        self.loan_due_date = None
        self.repayment_history = []
        self.notifications = []
        self.transactions = []

    def client_details(self):
        self.name = input("Enter your name: ")
        self.gender = input("Enter your gender (M/F): ")
        self.id = int(input("Enter your aadhar number: "))
        self.ph_no = int(input("Enter your phone number: "))
        self.address = input("Enter your address: ")
        self.open_bal = float(input("Enter opening deposit: "))
        self.set_username()
        self.set_pin()

    def set_username(self):
        self.username = input("Set a unique username: ")

    def set_pin(self):
        while True:
            pin = input("Set your 4-digit PIN: ")
            if pin.isdigit() and len(pin) == 4:
                self.pin = pin
                return
            print("Invalid PIN. Must be 4 digits.")


    def show_client_details(self):
        print(f"Account Number: {self.account_number}")
        print(f"{self.name} | {self.gender} | Aadhar: {self.id}")
        print(f"Phone Number: {self.ph_no}, Address: {self.address}")
        print(f"Balance: ₹{self.open_bal:.2f}")
        if self.loan_balance > 0:
            print(f"Loan Balance: ₹{self.loan_balance:.2f}, EMI: ₹{self.loan_emi:.2f}")
        print("-" * 40)
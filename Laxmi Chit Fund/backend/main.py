from backend.bank import Bank
from backend.admin import Admin

bank = Bank()
admin = Admin(bank)

def client_menu():
    while True:
        if bank.current_client is None:
            print("\n--- Client Access ---")
            print("1. Open Account (Register)")
            print("2. Login")
            print("3. Back to Main Menu")
            choice = input("Choose: ")

            if choice == "1":
                bank.add_client()
            elif choice == "2":
                bank.client_login()
            elif choice == "3":
                break
            else:
                print("Invalid choice.")
        else:
            print(f"\n--- Welcome {bank.current_client.name} ---")
            print("1. Check Balance\n2. Credit Money\n3. Debit Money\n4. Delete Account")
            print("5. Request Loan\n6. Repay Loan\n7. View Personal Details")
            print("8. View Repayment History\n9. View Account Statement")
            print("10. Change PIN\n11. View Notifications\n12. Logout")

            choice = input("Choose: ")
            actions = {
                "1": bank.check_balance,
                "2": bank.credit,
                "3": bank.debit,
                "4": bank.delete_account,
                "5": bank.request_loan,
                "6": bank.repay_loan,
                "7": bank.verify_details,
                "8": bank.view_repayment_history,
                "9": bank.view_account_statement,
                "10": bank.change_pin,
                "11": bank.view_notifications,
                "12": bank.logout_client
            }

            if choice in actions:
                actions[choice]()
                if choice == "12":
                    continue
            else:
                print("Invalid choice.")

def admin_menu():
    if not admin.admin_login():
        return
    while True:
        print("\nAdmin Menu:")
        print("1. Show All Clients")
        print("2. Delete Account")
        print("3. Export Data")
        print("4. Apply Interest")
        print("5. Review Loans")
        print("6. Apply Loan Interest")
        print("7. Auto Deduct EMI")
        print("8. View All Repayment Histories")
        print("9. Back")

        choice = input("Choose: ")
        actions = {
            "1": admin.show_database,
            "2": admin.delete_any_account,
            "3": bank.export_data,
            "4": bank.apply_interest,
            "5": admin.review_loans,
            "6": bank.apply_loan_interest,
            "7": bank.auto_deduct_emi,
            "8": admin.view_all_repayment_histories
        }
        if choice in actions:
            actions[choice]()
        elif choice == "9":
            break
        else:
            print("Invalid choice.")

while True:
    print("\n===== Welcome To Laxmi Chit Fund Bank =====")
    print("1. Client Access\n2. Admin Login\n3. Exit")
    m = input("Choose: ")
    if m == "1":
        client_menu()
    elif m == "2":
        admin_menu()
    elif m == "3":
        print("Thanks for visiting Laxmi Chit Fund!")
        break
    else:
        print("Invalid selection.")
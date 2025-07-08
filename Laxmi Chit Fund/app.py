from flask import Flask, render_template, request, redirect, url_for, session
from backend.bank import Bank
from backend.admin import Admin
from backend.db_transaction import save_transaction, save_repayment
from backend.database_utils import update_client_in_db
from backend.client import Client
from backend.database_utils import save_client_to_db
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

bank = Bank()
admin = Admin(bank)

def get_current_client():
    if 'username' in session:
        return next((c for c in bank.database if c.username == session['username']), None)
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/client_login', methods=['GET', 'POST'])
def client_login():
    success = request.args.get('success') == '1'
    error = None

    if request.method == 'POST':
        uname = request.form['username']
        pin = request.form['pin']
        for c in bank.database:
            if c.username == uname and c.pin == pin:
                session['username'] = c.username
                return redirect(url_for('client_dashboard'))
        error = "Invalid credentials."

    return render_template('login.html', error=error, success=success)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        aadhar = int(request.form['aadhar'])

        # Check for duplicate username or aadhar
        for client in bank.database:
            if client.username == username:
                return render_template('register.html', error="Username already exists.")
            if client.id == aadhar:
                return render_template('register.html', error="Aadhar number already exists.")

        c = Client()
        c.name = request.form['name']
        c.gender = request.form['gender']
        c.id = aadhar
        c.ph_no = int(request.form['phone'])
        c.address = request.form['address']
        c.open_bal = float(request.form['balance'])
        c.username = username
        c.pin = request.form['pin']

        # Add safe defaults for DB fields
        c.loan_request = None
        c.loan_approved = False
        c.loan_balance = 0.0
        c.loan_emi = 0.0
        c.loan_due_date = None

        bank.database.append(c)
        save_client_to_db(c)

        return redirect(url_for('client_login', success='1'))
    return render_template('register.html')

@app.route('/client_dashboard')
def client_dashboard():
    client = get_current_client()
    if client:
        return render_template('client_dashboard.html', client=client)
    return redirect(url_for('client_login'))

@app.route('/credit', methods=['POST'])
def credit():
    client = get_current_client()
    if client:
        amt = float(request.form['amount'])
        client.open_bal += amt
        today = datetime.date.today()
        client.transactions.append(("Credit", amt, today))
        save_transaction(client.account_number, "Credit", amt, today)
        update_client_in_db(client)
        return redirect(url_for('client_dashboard'))
    return redirect(url_for('client_login'))

@app.route('/debit', methods=['POST'])
def debit():
    client = get_current_client()
    if client:
        amt = float(request.form['amount'])
        if amt > client.open_bal:
            return "Insufficient balance"
        client.open_bal -= amt
        today = datetime.date.today()
        client.transactions.append(("Debit", amt, today))
        save_transaction(client.account_number, "Debit", amt, today)
        update_client_in_db(client)
        return redirect(url_for('client_dashboard'))
    return redirect(url_for('client_login'))

@app.route('/apply_loan', methods=['POST'])
def apply_loan():
    client = get_current_client()
    if client:
        amount = float(request.form['loan_amount'])

        if client.loan_approved and client.loan_balance > 0:
            return "Loan denied: existing loan is still active."

        if client.loan_request:
            return "Loan request already submitted and pending approval."

        client.loan_request = amount
        update_client_in_db(client)
        return redirect(url_for('client_dashboard'))

    return redirect(url_for('client_login'))

@app.route('/repay_loan', methods=['POST'])
def repay_loan():
    client = get_current_client()
    if client:
        amt = float(request.form['amount'])
        if client.loan_balance <= 0:
            return "No loan to repay"
        if amt > client.open_bal:
            return "Insufficient balance"

        client.loan_balance -= amt
        client.open_bal -= amt
        today = datetime.date.today()
        client.repayment_history.append((amt, today))
        client.transactions.append(("Loan Repayment", amt, today))
        save_transaction(client.account_number, "Loan Repayment", amt, today)
        save_repayment(client.account_number, amt, today)
        update_client_in_db(client)
        return redirect(url_for('client_dashboard'))
    return redirect(url_for('client_login'))

@app.route('/admin/reset_loan', methods=['POST'])
def reset_loan():
    from backend.database_utils import update_client_in_db
    from backend.db_transaction import save_transaction
    import datetime

    acc_no = request.form['account_number']
    client = next((c for c in bank.database if str(c.account_number) == acc_no), None)

    if client and client.loan_approved:
        client.loan_balance = 0.0
        client.loan_approved = False
        client.loan_emi = 0.0
        client.loan_due_date = None

        save_transaction(client.account_number, "Loan Reset by Admin", 0, datetime.date.today())
        update_client_in_db(client)

    return redirect(url_for('admin_dashboard'))

@app.route('/statement')
def view_statement():
    client = get_current_client()
    if client:
        return render_template('statement.html', transactions=client.transactions, client=client)
    return redirect(url_for('client_login'))

@app.route('/notifications')
def notifications():
    client = get_current_client()
    if client:
        notes = client.notifications.copy()
        client.notifications.clear()
        return render_template('notifications.html', notifications=notes, client=client)
    return redirect(url_for('client_login'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    client = get_current_client()
    if client:
        bank.database.remove(client)
        update_client_in_db(client)  # Optional: soft delete or flag in DB
        session.clear()
        return "Account deleted. Thank you for banking with us."
    return redirect(url_for('client_login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin/approve_loan', methods=['POST'])
def approve_loan():
    from backend.database_utils import update_client_in_db
    from backend.db_transaction import save_transaction
    import datetime, math

    account_number = request.form['account_number']
    client = next((c for c in bank.database if str(c.account_number) == account_number), None)
    if client and client.loan_request and not client.loan_approved:
        client.loan_approved = True
        client.loan_balance += float(client.loan_request)

        P = client.loan_request
        annual_rate = 10
        N = 12
        R = annual_rate / 12 / 100
        emi = (P * R * (1 + R)**N) / ((1 + R)**N - 1)
        client.loan_emi = round(emi, 2)

        client.loan_due_date = datetime.date.today() + datetime.timedelta(days=30)

        client.loan_request = None

        save_transaction(client.account_number, "Loan Approved", P, datetime.date.today())
        update_client_in_db(client)

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete_client', methods=['POST'])
def delete_client():
    account_number = request.form['account_number']
    client = next((c for c in bank.database if str(c.account_number) == account_number), None)
    if client:
        bank.database.remove(client)
        update_client_in_db(client)  # Optionally mark deleted in DB
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        uid = request.form['username']
        pwd = request.form['password']
        
        # Admin credentials from your Admin class
        if uid == admin.admin_id and pwd == admin.admin_password:
            session['admin'] = True  # Mark admin as logged in
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid admin credentials."

    return render_template('admin_login.html', error=error)

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    import datetime
    today = datetime.date.today()

    return render_template('admin_dashboard.html', clients=bank.database, current_date=today)

@app.route('/admin/deduct_emis', methods=['POST'])
def deduct_emis():
    import datetime
    today = datetime.date.today()

    for client in bank.database:
        if client.loan_approved and client.loan_balance > 0:
            if client.loan_emi and client.open_bal >= client.loan_emi:
                client.loan_balance -= client.loan_emi
                client.open_bal -= client.loan_emi

                client.transactions.append(("EMI Deducted", client.loan_emi, today))

                client.repayment_history.append((client.loan_emi, today))

                from backend.db_transaction import save_transaction
                from backend.database_utils import update_client_in_db
                save_transaction(client.account_number, "EMI Deducted", client.loan_emi, today)
                update_client_in_db(client)

    return redirect(url_for('admin_dashboard'))

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/admin/apply_interest', methods=['POST'])
def apply_interest():
    from backend.db_transaction import save_transaction
    from backend.database_utils import update_client_in_db
    import datetime

    interest_rate = 5  # annual rate in %
    monthly_rate = interest_rate / 12 / 100
    today = datetime.date.today()

    for client in bank.database:
        interest = client.open_bal * monthly_rate
        client.open_bal += interest
        client.transactions.append(("Balance Interest", round(interest, 2), today))
        save_transaction(client.account_number, "Balance Interest", round(interest, 2), today)
        update_client_in_db(client)

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/apply_loan_interest', methods=['POST'])
def apply_loan_interest():
    from backend.db_transaction import save_transaction
    from backend.database_utils import update_client_in_db
    import datetime

    try:
        annual_rate = float(request.form['rate'])  # From admin form
    except (ValueError, KeyError):
        return "Invalid interest rate.", 400

    monthly_rate = annual_rate / 12 / 100
    today = datetime.date.today()

    for client in bank.database:
        if client.loan_approved and client.loan_balance > 0:
            interest = client.loan_balance * monthly_rate
            client.loan_balance += interest
            client.transactions.append(("Loan Interest", round(interest, 2), today))
            save_transaction(client.account_number, "Loan Interest", round(interest, 2), today)
            update_client_in_db(client)

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/apply_loan_interest_single', methods=['POST'])
def apply_loan_interest_single():
    from backend.db_transaction import save_transaction
    from backend.database_utils import update_client_in_db
    import datetime

    acc_no = request.form.get('account_number')
    try:
        annual_rate = float(request.form.get('rate'))
    except (TypeError, ValueError):
        return redirect(url_for('admin_dashboard', message="❌ Invalid interest rate."))

    client = next((c for c in bank.database if str(c.account_number) == acc_no), None)
    if not client:
        return redirect(url_for('admin_dashboard', message=f"❌ No client found with account number {acc_no}."))

    if not client.loan_approved or client.loan_balance <= 0:
        return redirect(url_for('admin_dashboard', message=f"❌ Client has no active loan to apply interest."))

    monthly_rate = annual_rate / 12 / 100
    interest = client.loan_balance * monthly_rate
    client.loan_balance += interest
    today = datetime.date.today()
    client.transactions.append(("Loan Interest", round(interest, 2), today))
    save_transaction(client.account_number, "Loan Interest", round(interest, 2), today)
    update_client_in_db(client)

    return redirect(url_for('admin_dashboard', message=f"✅ Interest of ₹{round(interest,2)} applied to {acc_no}"))

@app.route('/admin/verify_client', methods=['POST'])
def verify_client():
    acc_no = request.form.get('account_number')
    client = next((c for c in bank.database if str(c.account_number) == acc_no), None)

    if not client:
        return redirect(url_for('admin_dashboard', message=f"❌ No client found with account number {acc_no}."))

    # Send client info to a new verification template
    return render_template('verify_client.html', client=client)

@app.route('/admin/repayment_history/<account_number>')
def view_repayment_history(account_number):
    client = next((c for c in bank.database if str(c.account_number) == account_number), None)
    if not client:
        return redirect(url_for('admin_dashboard', message="❌ Client not found."))

    return render_template('repayment_history.html', client=client)

@app.route('/change_pin', methods=['POST'])
def change_pin():
    client = get_current_client()
    if not client:
        return redirect(url_for('client_login'))

    old_pin = request.form['old_pin']
    new_pin = request.form['new_pin']
    confirm_pin = request.form['confirm_pin']

    if old_pin != client.pin:
        return render_template('client_dashboard.html', client=client, message="Incorrect current PIN.")

    if new_pin != confirm_pin:
        return render_template('client_dashboard.html', client=client, message="New PINs do not match.")

    if len(new_pin) < 4:
        return render_template('client_dashboard.html', client=client, message="PIN must be at least 4 digits.")

    client.pin = new_pin
    update_client_in_db(client)

    return render_template('client_dashboard.html', client=client, message="PIN changed successfully (success)")

@app.route('/account_statement')
def account_statement():
    client = get_current_client()
    if not client:
        return redirect(url_for('client_login'))

    return render_template('account_statement.html', client=client)

@app.route('/notifications')
def view_notifications():
    client = get_current_client()
    if not client:
        return redirect(url_for('client_login'))

    return render_template('notifications.html', client=client)

@app.route('/admin/review_loans')
def review_loans():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    pending = [c for c in bank.database if c.loan_request and not c.loan_approved]
    active = [c for c in bank.database if c.loan_approved and c.loan_balance > 0]
    today = datetime.date.today()

    return render_template('review_loans.html', pending_loans=pending, active_loans=active, current_date=today)

@app.route('/admin/repayment_history_all')
def view_all_repayments():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    all_repayments = []

    for client in bank.database:
        for amount, date in client.repayment_history:
            all_repayments.append({
                'account_number': client.account_number,
                'name': client.name,
                'amount': amount,
                'date': date
            })

    return render_template('repayment_history_all.html', repayments=all_repayments)

if __name__ == '__main__':
    app.run(debug=True)
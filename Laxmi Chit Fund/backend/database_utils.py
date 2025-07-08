# db_utils.py
import mysql.connector
from backend.client import Client

def save_client_to_db(client):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Onedayiwill",
            port = 3306,
            database="laxmi_chit_fund"
        )
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO clients (
            account_number, name, gender, aadhar, phone, address,
            username, pin, balance, loan_request, loan_approved,
            loan_balance, loan_emi, loan_due_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            client.account_number,
            client.name,
            client.gender,
            client.id,
            client.ph_no,
            client.address,
            client.username,
            client.pin,
            client.open_bal,
            client.loan_request,
            client.loan_approved,
            client.loan_balance,
            client.loan_emi,
            client.loan_due_date
        ))

        conn.commit()
        print("✅ Client saved to database.")
    except mysql.connector.Error as err:
        print("❌ Error saving client to DB:", err)
    finally:
        cursor.close()
        conn.close()

def load_clients_from_db():
    clients = []

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Onedayiwill",
            port = 3306,
            database="laxmi_chit_fund"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clients")
        rows = cursor.fetchall()

        for row in rows:
            c = Client()
            c.account_number = row['account_number']
            c.name = row['name']
            c.gender = row['gender']
            c.id = row['aadhar']
            c.ph_no = row['phone']
            c.address = row['address']
            c.username = row['username']
            c.pin = row['pin']
            c.open_bal = row['balance']
            c.loan_request = row['loan_request']
            c.loan_approved = row['loan_approved']
            c.loan_balance = row['loan_balance']
            c.loan_emi = row['loan_emi']
            c.loan_due_date = row['loan_due_date']
            c.repayment_history = []
            c.transactions = []
            c.notifications = []
            clients.append(c)

        print(f"✅ Loaded {len(clients)} client(s) from the database.")

    except mysql.connector.Error as err:
        print("❌ Error loading clients:", err)
    finally:
        cursor.close()
        conn.close()

    return clients

def load_clients_from_db():
    from backend.db_transaction import get_repayments_by_account, get_transactions_by_account
    clients = []

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Onedayiwill",
            port = 3306,
            database="laxmi_chit_fund"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clients")
        rows = cursor.fetchall()

        for row in rows:
            c = Client()
            c.account_number = row['account_number']
            c.name = row['name']
            c.gender = row['gender']
            c.id = row['aadhar']
            c.ph_no = row['phone']
            c.address = row['address']
            c.username = row['username']
            c.pin = row['pin']
            c.open_bal = row['balance']
            c.loan_request = row['loan_request']
            c.loan_approved = row['loan_approved']
            c.loan_balance = row['loan_balance']
            c.loan_emi = row['loan_emi']
            c.loan_due_date = row['loan_due_date']

            # Load repayment history and transactions from DB
            c.repayment_history = get_repayments_by_account(c.account_number)
            c.transactions = get_transactions_by_account(c.account_number)
            c.notifications = []
            clients.append(c)

        print(f"✅ Loaded {len(clients)} client(s) with histories from the DB.")
    except mysql.connector.Error as err:
        print("❌ Error loading clients:", err)
    finally:
        cursor.close()
        conn.close()

    return clients

def update_client_in_db(client):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Onedayiwill",
            port = 3306,
            database="laxmi_chit_fund"
        )
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE clients SET
            balance=%s,
            pin=%s,
            loan_request=%s,
            loan_approved=%s,
            loan_balance=%s,
            loan_emi=%s,
            loan_due_date=%s
        WHERE account_number=%s
        """, (
            client.open_bal,
            client.pin,
            client.loan_request,
            client.loan_approved,
            client.loan_balance,
            client.loan_emi,
            client.loan_due_date,
            client.account_number
        ))

        conn.commit()
    except mysql.connector.Error as err:
        print("❌ Failed to update client:", err)
    finally:
        cursor.close()
        conn.close()
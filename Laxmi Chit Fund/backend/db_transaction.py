# transaction.py
import mysql.connector

def save_transaction(account_number, txn_type, amount, date):
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
        INSERT INTO transactions (account_number, type, amount, date)
        VALUES (%s, %s, %s, %s)
        """, (account_number, txn_type, amount, date))
        conn.commit()
    except mysql.connector.Error as err:
        print("❌ Error saving transaction:", err)
    finally:
        cursor.close()
        conn.close()

def save_repayment(account_number, amount, date):
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
        INSERT INTO repayments (account_number, amount, date)
        VALUES (%s, %s, %s)
        """, (account_number, amount, date))
        conn.commit()
    except mysql.connector.Error as err:
        print("❌ Error saving repayment:", err)
    finally:
        cursor.close()
        conn.close()

def get_repayments_by_account(account_number):
    records = []
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
        SELECT amount, date FROM repayments WHERE account_number = %s
        """, (account_number,))
        records = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return records

def get_transactions_by_account(account_number):
    records = []
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
        SELECT type, amount, date FROM transactions WHERE account_number = %s
        """, (account_number,))
        records = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return records
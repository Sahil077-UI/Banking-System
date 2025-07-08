import mysql.connector

def setup_database():
    try:
        conn = mysql.connector.connect(
            user = 'root',
            password = 'Onedayiwill',
            host = 'localhost',
            port = 3306,
        )

        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS laxmi_chit_fund")
        cursor.execute("USE laxmi_chit_fund")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            account_number BIGINT PRIMARY KEY,
            name VARCHAR(100),
            gender CHAR(1),
            aadhar BIGINT UNIQUE,
            phone BIGINT,
            address TEXT,
            username VARCHAR(50) UNIQUE,
            pin VARCHAR(4),
            balance FLOAT,
            loan_request FLOAT,
            loan_approved BOOLEAN,
            loan_balance FLOAT,
            loan_emi FLOAT,
            loan_due_date DATE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_number BIGINT,
            type VARCHAR(20),
            amount FLOAT,
            date DATE,
            FOREIGN KEY (account_number) REFERENCES clients(account_number)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS repayments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_number BIGINT,
            amount FLOAT,
            date DATE,
            FOREIGN KEY (account_number) REFERENCES clients(account_number)
        )
        """)

        conn.commit()
        print("✅ Database and tables created successfully.")
    
    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    setup_database()
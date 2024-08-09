import sqlite3
import hashlib
import random
from datetime import datetime

def setup_database():
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()

    # Drop tables if they exist to reset the schema (for development purposes only)
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS user_log")

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        account_number TEXT UNIQUE NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        transaction_type TEXT NOT NULL,
                        amount INTEGER NOT NULL,
                        balance_after INTEGER NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        action TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                      )''')

    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_account_number():
    return f"{random.randint(1000000000, 9999999999)}"

def create_account(username, password):
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()

    account_number = generate_account_number()
    initial_balance = 10000  # Initial balance for every new account

    try:
        cursor.execute("INSERT INTO users (username, password, account_number) VALUES (?, ?, ?)", 
                       (username, hash_password(password), account_number))
        conn.commit()

        # Add initial balance transaction
        cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount, balance_after) VALUES (?, ?, ?, ?)",
                       (cursor.lastrowid, 'deposit', initial_balance, initial_balance))
        conn.commit()

        print("Account creation successful.")
        print(f"Your account number is: {account_number}")
        print(f"You have received an initial balance of {initial_balance} naira from Abbey's Bank!")
    except sqlite3.IntegrityError:
        print("Username already exists.")

    conn.close()

def login(username, password):
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and user[1] == hash_password(password):
        log_user_action(user[0], 'logged in')
        print("Login successful.")
        conn.close()
        return user[0], username
    else:
        print("Invalid credentials.")
        conn.close()
        return None, None

def log_user_action(user_id, action):
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_log (user_id, action) VALUES (?, ?)", (user_id, action))
    conn.commit()
    conn.close()

    with open('user_log.txt', 'a') as file:
        file.write(f"{datetime.now()} - User ID {user_id} {action}\n")

def check_balance(user_id):
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(CASE WHEN transaction_type = 'deposit' THEN amount WHEN transaction_type = 'transfer' THEN -amount END), 0) FROM transactions WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()[0]

    print(f"Current balance: {balance}")
    conn.close()

def deposit_amount(user_id, amount):
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(CASE WHEN transaction_type = 'deposit' THEN amount WHEN transaction_type = 'transfer' THEN -amount END), 0) FROM transactions WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()[0]

    balance += amount
    cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount, balance_after) VALUES (?, ?, ?, ?)",
                   (user_id, 'deposit', amount, balance))
    conn.commit()
    conn.close()

    print(f"Balance after depositing {amount}: {balance}")

def transfer_amount(user_id, amount, recipient_account):
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()

    # Check if recipient account exists
    cursor.execute("SELECT id FROM users WHERE account_number = ?", (recipient_account,))
    recipient = cursor.fetchone()

    if recipient:
        recipient_id = recipient[0]

        cursor.execute("SELECT COALESCE(SUM(CASE WHEN transaction_type = 'deposit' THEN amount WHEN transaction_type = 'transfer' THEN -amount END), 0) FROM transactions WHERE user_id = ?", (user_id,))
        balance = cursor.fetchone()[0]

        if amount > balance:
            print("Error: Transfer amount exceeds account balance.")
        elif amount <= 0:
            print("Error: Transfer amount must be greater than zero.")
        else:
            # Debit sender
            balance -= amount
            cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount, balance_after) VALUES (?, ?, ?, ?)",
                           (user_id, 'transfer', -amount, balance))

            # Credit recipient
            cursor.execute("SELECT COALESCE(SUM(CASE WHEN transaction_type = 'deposit' THEN amount WHEN transaction_type = 'transfer' THEN -amount END), 0) FROM transactions WHERE user_id = ?", (recipient_id,))
            recipient_balance = cursor.fetchone()[0] + amount
            cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount, balance_after) VALUES (?, ?, ?, ?)",
                           (recipient_id, 'deposit', amount, recipient_balance))

            conn.commit()
            print(f"Transferred {amount} naira to account {recipient_account}. Your new balance is {balance} naira.")
    else:
        print("Error: Recipient account not found.")

    conn.close()

def logout(user_id):
    log_user_action(user_id, 'logged out')
    print("Logged out successfully.")

def main():
    setup_database()

    while True:
        print("\n1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            create_account(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_id, username = login(username, password)
            if user_id:
                while True:
                    print("\n1. Check Balance")
                    print("2. Deposit Amount")
                    print("3. Transfer Amount")
                    print("4. Logout")
                    action = input("Choose an action: ")

                    if action == '1':
                        check_balance(user_id)
                    elif action == '2':
                        amount = int(input("Enter amount to deposit: "))
                        deposit_amount(user_id, amount)
                    elif action == '3':
                        amount = int(input("Enter amount to transfer: "))
                        recipient_account = input("Enter recipient account number: ")
                        transfer_amount(user_id, amount, recipient_account)
                    elif action == '4':
                        logout(user_id)
                        break
                    else:
                        print("Invalid option. Please try again.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

import sqlite3
from datetime import datetime
import random

def setup_database():
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()

    # delete during presentationnnn
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS user_log")

    
    cursor.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        account_number TEXT UNIQUE NOT NULL,
                        balance REAL NOT NULL DEFAULT 10000,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )''')

    cursor.execute('''CREATE TABLE transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        transaction_type TEXT,
                        amount REAL,
                        balance_after REAL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                      )''')

    cursor.execute('''CREATE TABLE user_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        action TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                      )''')

    conn.commit()
    conn.close()

def create_account(username, password):
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()
    account_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    
    try:
        cursor.execute("INSERT INTO users (username, password, account_number) VALUES (?, ?, ?)", 
                       (username, password, account_number))
        conn.commit()
        print(f"Account creation successful.\nYour account number is: {account_number}")
        print("You have received an initial balance of 10000 naira from Abbey's Bank!")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    conn.close()

def login(username, password):
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        log_user_action(user_id, 'logged in')
        print("Login successful")
        conn.close()
        return user_id
    else:
        print("Invalid credentials")
        conn.close()
        return None

def log_user_action(user_id, action):
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_log (user_id, action) VALUES (?, ?)", (user_id, action))
    conn.commit()
    conn.close()

def check_balance(user_id):
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    balance = cursor.fetchone()[0]
    print(f"Current balance: {balance} naira")
    
    conn.close()

def deposit_amount(user_id, amount):
    if amount <= 0:
        print("Amount must be greater than zero")
        return

    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    current_balance = cursor.fetchone()[0]

    new_balance = current_balance + amount
    cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
    cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount, balance_after) VALUES (?, ?, ?, ?)",
                   (user_id, 'deposit', amount, new_balance))
    
    conn.commit()
    conn.close()

    print(f"Deposited {amount} naira. New balance: {new_balance} naira")

def transfer_amount(sender_id, recipient_account_number, amount):
    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()

  
    cursor.execute("SELECT balance FROM users WHERE id = ?", (sender_id,))
    sender_balance = cursor.fetchone()[0]

    if amount > sender_balance:
        print("Transfer amount exceeds account balance.")
        conn.close()
        return

    # Get recipient ID
    cursor.execute("SELECT id, balance FROM users WHERE account_number = ?", (recipient_account_number,))
    recipient = cursor.fetchone()

    if not recipient:
        print("Recipient account number not found.")
        conn.close()
        return

    recipient_id, recipient_balance = recipient

    # Update sender balance
    new_sender_balance = sender_balance - amount
    cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_sender_balance, sender_id))
    cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount, balance_after) VALUES (?, ?, ?, ?)",
                   (sender_id, 'transfer', -amount, new_sender_balance))

    # Update recipient balance
    new_recipient_balance = recipient_balance + amount
    cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_recipient_balance, recipient_id))
    cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount, balance_after) VALUES (?, ?, ?, ?)",
                   (recipient_id, 'transfer', amount, new_recipient_balance))
    
    conn.commit()
    conn.close()

    print(f"Transferred {amount} naira to account {recipient_account_number}. Your new balance is {new_sender_balance} naira.")

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
            user_id = login(username, password)
            
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
                        amount = float(input("Enter amount to deposit: "))
                        deposit_amount(user_id, amount)
                    
                    elif action == '3':
                        amount = float(input("Enter amount to transfer: "))
                        recipient_account_number = input("Enter recipient account number: ")
                        transfer_amount(user_id, recipient_account_number, amount)
                    
                    elif action == '4':
                        log_user_action(user_id, 'logged out')
                        print("Logged out.")
                        break
                    
                    else:
                        print("Invalid action, Please try again")
        
        elif choice == '3':
            break
        
        else:
            print("Invalid option, Please try again")

# if __name__ == "__main__":
main()

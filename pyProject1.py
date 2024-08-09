# ......something to accept account balance
dict
# import sqlite3
# def bankAccount():
#     conn = sqlite3.connect("users.db")
#     cur = conn.cursor()
#     cur.execute("""CREATE TABLE IF NOT EXISTS Users( 
#         ID INTEGER PRIMARY KEY AUTOINCREMENT,
#         Username TEXT UNIQUE NOT NULL, 
#         password TEXT NOT NULL , 
#         TimeCreated TEXT NOT NULL )""")
    
#     cur.execute('''
#     CREATE TABLE IF NOT EXISTS Transactions (
#     ID INTEGER PRIMARY KEY AUTOINCREMENT,
#     UserID INTEGER NOT NULL,
#     TransactionType TEXT NOT NULL,
#     Amount INTEGER NOT NULL,
#     BalanceAfter INTEGER NOT NULL,
#     Timestamp TEXT NOT NULL,
#     FOREIGN KEY (UserID) REFERENCES Users(ID)
# )
# ''')
#     cur.execute('''
#     CREATE TABLE IF NOT EXISTS user_log (
#     ID INTEGER PRIMARY KEY AUTOINCREMENT,
#     UserID INTEGER NOT NULL,
#     Action TEXT NOT NULL,
#     Timestamp TEXT NOT NULL,
#     FOREIGN KEY (UserID) REFERENCES Users(ID)
# )
# ''')
    

    
#     conn.commit()
#     conn.close()
#     print("created")



# # bankAccount()
# def insert():
#     conn = sqlite3.connect("users.db")
#     cur = conn.cursor()
#     id1 = 1
#     uname = "oyin"
#     password1 = "pass"
#     time = "ten"
#     cur.execute(
#                 "INSERT INTO Users (Username, password, TimeCreated) VALUES (?, ?, ?)",
#                 (uname, password1, time)
#             )
#     conn.commit()
#     conn.close()
#     print("inserted")



# insert()

# def usernameExists(username):
#     conn = sqlite3.connect("users.db")
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM Users WHERE Username = ?", (username,))
#     result = cur.fetchone()

#     if result is not None:
#         return True
#     else:
#         return False
    
        
#===================
# signup
#===================
# UserUsername = input("Enter your username: ")
# password = input("Enter your password: ")
# while True:
#     if usernameExists(UserUsername):
#         print("username exists, choose another")
#         continue
#     else:
#         print("available")
#         break

#(....... insert the name and password into the table)
#===================================================

# response = input("do you have an account (Y/N): ")
# if response == "N":
#     print("kindly create one: ")

    
# else:
    


#==============
#login
#==============
# UserUsername = input("Enter your username: ")
# password = input("Enter your password: ")












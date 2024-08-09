def delStudentInfo():
    import sqlite3
    conn = sqlite3.connect("mydatabase.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE User( 
        studentID INTEGER,
        Fname TEXT , 
        Lname TEXT , 
        Course TEXT , 
        Regnum VARCHAR , 
        Age INTEGER )""")
    studentID = 109
    first_name = "OYIN"
    last_name = "SOLARIN"
    coursee = "ICE"
    regnumm = 2000
    agee = 29

    # studentIDD = 890
    # first_namee = "OYINda"
    # last_namee = "SOLa"
    # courseee = "comp"
    # regnummm = 2001
    # ageee = 26

    # cur.execute("INSERT INTO User (studentID, Fname, Lname, Course, Regnum, Age) VALUES ( ?, ?, ?, ?, ?, ?)",
    #             (studentID, first_name, last_name, coursee, regnumm, agee))
    # cur.execute("INSERT INTO User (studentID, Fname, Lname, Course, Regnum, Age) VALUES ( ?, ?, ?, ?, ?, ?)",
    #             (studentIDD, first_namee, last_namee, courseee, regnummm, ageee))
    # cur.execute("DELETE FROM user WHERE StudentID = '890'")
    # conn.commit()
    # conn.close()
    # print("deleted")







# delStudentInfo()
def updateTrack():
    import sqlite3
    conn = sqlite3.connect("mydatabase.db")
    cur = conn.cursor()
    cur.execute("UPDATE user SET Course='python' WHERE studentID =109")
    conn.commit()
    conn.close()
    print("updated")



updateTrack()

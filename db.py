import sqlite3
conn=sqlite3.connect("employees.sqlite")

cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS department(
    deptid INTEGER PRIMARY KEY AUTOINCREMENT,
    DeptName TEXT NOT NULL
)
""")
cursor.execute(""" CREATE TABLE IF NOT EXISTS employee(
    EmpId integer PRIMARY KEY AUTOINCREMENT,
    EmpName text NOT NULL , 
    Designation text NOT NULL, 
    Manager integer , 
    deptid integer,FOREIGN KEY (deptid) REFERENCES department (deptid)
)""")


conn.commit()
conn.close()
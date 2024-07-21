from flask import Flask,request,jsonify,render_template

import sqlite3
app=Flask(__name__)

def db_connection():
    conn=None
    try:
        conn=sqlite3.connect('employees.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/departments', methods=['GET', 'POST'])
def departments():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM department ")
        departments = [
            dict(deptid=row[0], DeptName=row[1])
            for row in cursor.fetchall()
        ]
        return jsonify(departments)

    if request.method == 'POST':
        try:
            new_DeptName = request.form['DeptName']
        except KeyError:
            conn.close()
            return jsonify({"error": "Missing data"}),400

        sql = "INSERT INTO department (DeptName) VALUES (?)"
        cursor.execute(sql, (new_DeptName,))
        conn.commit()
        conn.close()
        return f"Department with the deptid: {cursor.lastrowid} created successfully", 201

@app.route('/department/<int:deptid>', methods=['GET', 'PUT', 'DELETE'])
def department_detail(deptid):
    conn = db_connection()

    if conn is None:
        return jsonify({"Could not connect to the database"}), 500
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM department WHERE deptid=?", (deptid,))
        row = cursor.fetchone()
        for r in row:
            department=r
        if department is not None:
            return jsonify(department), 200
        else:
            return "Department not found", 404

    if request.method == 'PUT':
        sql = """UPDATE department SET DeptName=? WHERE deptid=?"""
        DeptName = request.form['DeptName']
        update_deplist={
            "deptid":deptid,
            "DeptName":DeptName
        }
        cursor.execute(sql, (DeptName, deptid))
        conn.commit()
        return jsonify(update_deplist)




    if request.method == 'DELETE':
        sql = """DELETE FROM department WHERE deptid=?"""
        cursor.execute(sql, (deptid,))
        conn.commit()
        if cursor.rowcount:
            conn.close()
            return f"Department with deptid: {deptid} has been deleted.", 200
        else:
            conn.close()
            return f"Department with deptid: {deptid} not found", 404


@app.route('/employees',methods=['GET','POST'])
def employees():
    conn=db_connection()
    cursor=conn.cursor()
    if request.method=='GET':
        cursor=conn.execute("SELECT * FROM employee")
        employee=[
            dict(EmpId=row[0],EmpName=row[1],Designation=row[2],Manager=row[3],deptid=row[4])
            for row in cursor.fetchall()
        ]
        if employee is not None:
            return jsonify(employee)

    if request.method=='POST':

        new_EmpName=request.form['EmpName']
        new_Designation=request.form['Designation']
        new_Manager=int(request.form['Manager'])
        new_deptid=int(request.form['deptid'])
        sql="""INSERT INTO employee (EmpName,Designation,Manager,deptid)
        VALUES (?,?,?,?)"""
        cursor.execute(sql,(new_EmpName,new_Designation,new_Manager,new_deptid))
        conn.commit()
        return f"Employee with the EmpId:{cursor.lastrowid} created successfully",201


@app.route('/employee/<int:EmpId>',methods=['GET','PUT','DELETE'])
def employees_detail(EmpId):
    conn=db_connection()
    cursor=conn.cursor()
    employee=None
    if request.method=='GET':
        cursor.execute("SELECT * FROM employee WHERE EmpId=?",(EmpId,))
        rows=cursor.fetchone()
        for r in rows:
            employee=r
        if employee is not None:
            return jsonify(employee),200
        else:
            return "Employee not found",404
    if request.method=='PUT':
        sql="""
        UPDATE employee SET EmpName=?,
        Designation=?,
        Manager=?,
        deptid=? WHERE EmpId=?"""

        EmpName=request.form['EmpName']
        Designation=request.form['Designation']
        Manager=request.form['Manager']
        deptid=request.form['deptid']
        update_emplist={
            "EmpId":EmpId,
            "EmpName":EmpName,
            "Designation":Designation,
            "Manager":Manager,
            'deptid':deptid
        }
        conn.execute(sql,(EmpName,Designation,Manager,deptid,EmpId))
        conn.commit()
        return jsonify(update_emplist)

    if request.method=='DELETE':
        sql="""DELETE FROM employee WHERE EmpId=?"""
        conn.execute(sql,(EmpId,))
        conn.commit()
        return "The employee with EmpId: {} has been deleted.".format(EmpId),200

@app.route('/')
def home():
    links = {
        'Employee': 'http://127.0.0.1:5000/employees',
        'Employees_detail':'http://127.0.0.1:5000/employee/1',
        'Department': 'http://127.0.0.1:5000/departments',
        'Department_detail': 'http://127.0.0.1:5000/department/1'
    }
    return render_template('index.html', links=links)




if __name__=="__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify, render_template
import sqlite3
import re

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('company.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    user_query = request.json.get('query')
    
    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400
    
    # Process supported queries
    if re.match(r"show me all employees in the (.+) department", user_query, re.I):
        department = re.search(r"show me all employees in the (.+) department", user_query, re.I).group(1)
        return jsonify(show_employees_in_department(department))
    
    elif re.match(r"who is the manager of the (.+) department", user_query, re.I):
        department = re.search(r"who is the manager of the (.+) department", user_query, re.I).group(1)
        return jsonify(get_manager_of_department(department))
    
    elif re.match(r"list all employees hired after (.+)", user_query, re.I):
        hire_date = re.search(r"list all employees hired after (.+)", user_query, re.I).group(1)
        return jsonify(list_employees_hired_after(hire_date))
    
    elif re.match(r"what is the total salary expense for the (.+) department", user_query, re.I):
        department = re.search(r"what is the total salary expense for the (.+) department", user_query, re.I).group(1)
        return jsonify(total_salary_expense(department))
    
    else:
        return jsonify({"error": "Sorry, I could not understand your query."}), 400

# Define the functions with the queries

def show_employees_in_department(department):
    conn = get_db_connection()
    query = "SELECT * FROM Employees WHERE Department = ?"
    employees = conn.execute(query, (department,)).fetchall()
    conn.close()

    if employees:
        return {"employees": [dict(employee) for employee in employees]}
    else:
        return {"error": f"No employees found in the {department} department."}


def get_manager_of_department(department):
    conn = get_db_connection()
    query = """
        SELECT d.Manager 
        FROM Departments d 
        WHERE d.Name = ?
    """
    manager = conn.execute(query, (department,)).fetchone()
    conn.close()

    if manager:
        return {"manager": manager['Manager']}
    else:
        return {"error": f"No manager found for the {department} department."}

def list_employees_hired_after(date):
    conn = get_db_connection()
    query = """
        SELECT * 
        FROM Employees 
        WHERE Hire_Date > ?
    """
    employees = conn.execute(query, (date,)).fetchall()
    conn.close()

    if employees:
        return {"employees": [dict(employee) for employee in employees]}
    else:
        return {"error": f"No employees hired after {date}."}

def total_salary_expense(department):
    conn = get_db_connection()
    query = """
        SELECT SUM(Salary) AS TotalSalary 
        FROM Employees 
        WHERE Department = ?
    """
    result = conn.execute(query, (department,)).fetchone()
    conn.close()

    if result and result['TotalSalary']:
        return {"total_salary_expense": result['TotalSalary']}
    else:
        return {"error": f"No salary data found for the {department} department."}

if __name__ == "__main__":
    app.run(debug=True)

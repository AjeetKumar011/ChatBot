from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('company.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route("/")
def home():
    # Fetch data from Employees table
    conn = get_db_connection()
    employees_query = "SELECT * FROM Employees"
    employees = conn.execute(employees_query).fetchall()

    # Fetch data from Departments table
    departments_query = "SELECT * FROM Departments"
    departments = conn.execute(departments_query).fetchall()
    conn.close()

    # Pass the data to the HTML template
    return render_template("Table.html", employees=employees, departments=departments)

if __name__ == "__main__":
    app.run(debug=True)

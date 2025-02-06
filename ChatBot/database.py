import sqlite3

conn = sqlite3.connect('company.db')
c = conn.cursor()

# Create the Employees table
c.execute('''CREATE TABLE IF NOT EXISTS Employees (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Department TEXT,
                Salary INTEGER,
                Hire_Date TEXT)''')

# Create the Departments table
c.execute('''CREATE TABLE IF NOT EXISTS Departments (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Manager TEXT)''')

# Insert sample data into Employees table
c.execute("INSERT INTO Employees (Name, Department, Salary, Hire_Date) VALUES ('Alice', 'Sales', 50000, '2021-01-15')")
c.execute("INSERT INTO Employees (Name, Department, Salary, Hire_Date) VALUES ('Bob', 'Engineering', 70000, '2020-06-10')")
c.execute("INSERT INTO Employees (Name, Department, Salary, Hire_Date) VALUES ('Charlie', 'Marketing', 60000, '2022-03-20')")

# Insert sample data into Departments table
c.execute("INSERT INTO Departments (Name, Manager) VALUES ('Sales', 'Alice')")
c.execute("INSERT INTO Departments (Name, Manager) VALUES ('Engineering', 'Bob')")
c.execute("INSERT INTO Departments (Name, Manager) VALUES ('Marketing', 'Charlie')")

# Commit and close the connection
conn.commit()
conn.close()

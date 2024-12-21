import sqlite3

# Connect to SQLite
connection = sqlite3.connect("student.db")

# Create a cursor object
cursor = connection.cursor()

# Create the STUDENT table (use IF NOT EXISTS to avoid errors)
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""
cursor.execute(table_info)

# Insert some records
cursor.execute("INSERT INTO STUDENT VALUES ('Krish', 'Data Science', 'A', 90)")
cursor.execute("INSERT INTO STUDENT VALUES ('Sudhanshu', 'Data Science', 'B', 100)")
cursor.execute("INSERT INTO STUDENT VALUES ('Darius', 'Data Science', 'A', 86)")
cursor.execute("INSERT INTO STUDENT VALUES ('Vikash', 'DEVOPS', 'A', 50)")
cursor.execute("INSERT INTO STUDENT VALUES ('Dipesh', 'DEVOPS', 'A', 35)")

# Commit the changes to the database
connection.commit()

# Display all the records
print("The inserted records are:")
data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)

# Close the connection
connection.close()

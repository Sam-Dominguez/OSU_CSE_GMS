import os
import sqlite3 as sq

def run_query(cursor, query_string):
    try:
        result = cursor.execute(query_string)
    except:
        print("Query error")
        result = None
    return result


# Connect to the database
db_file = r'OSUCSEGraderManagementSystem.db'

if not os.path.isfile(db_file):
    print('Database file does not exist.')
else:
    try:
        conn = sq.connect(db_file)
        print("Database connection established.")
    except Error:
        print(Error)

# Create a cursor to use to access the data
try:
    cur = conn.cursor()
    print('Cursor created.')
except Error:
    print(Error)

# Get all table names
result = run_query(cur,'SELECT name from sqlite_master where type= "table"')
print(cur.fetchall())
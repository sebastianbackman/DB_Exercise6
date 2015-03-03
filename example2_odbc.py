# A simple program which connects to an ODBC database
# and then executes a simple query.
# It also illustrates the raw format of the returned result.
# Stephen J. Hegner 15 June 2011.
# Modified for Python 3 compatibility 21 February 2014.

### This script has been tested with both Python2 and Python3
### under PostgreSQL and MySQL running on Debian 7 Linux.
### IMPORTANT: For PostgreSQL:
###      the ANSI driver psqlodbca.so must be used for Python2;
###      the Unicode driver psqlodbcw.so must be used for Python3.
### For other Linux distributions which use Unicode in the OS (e.g., Ubuntu)
### it may be necessary to use psqlodbcw.so for Python2 as well.
### For MySQL, the driver libmyodbc.so works for both Python2 and Python3.

import pyodbc	
import sys

# This example program and others re-use the same Python functions many times,
# so they are loaded from local files.
import my_odbc_connect
import my_odbc_cursor

query = "SELECT LName, FName, MInit, Sex, Salary FROM Employee"
#sys.argv[1]
#sys.argv[2]
#sys.argv[3]
db_name= "database1"
user_name = "c5dv119_vt15_oi10sbn"
pwd = "test"
#query1 = ""

# This call produces "fancy" formatted output.
def process_query():
    cursor1.execute(query)
    print("Employees and their salaries:")
    n=0
    while 1:
        row = cursor1.fetchone()
        if not row:
            break
        n = n+1
        print_result(row)
    if n==0:
        print("No tuples matching the given query were found.")

def print_result(r):
    titledict = {"F":"Ms.", "M":"Mr."}
    try:
        title = titledict[r[3]]
    except:
        title = "?"
    print("     %s %s %s. %s $%.0f" % (title, r[1], r[2], r[0], r[4]))

# This call shows that each retrieved row is a Python tuple.
def process_query2():
    cursor1.execute(query)
    print("Raw output for the query, one row at a time:")
    n=0
    while 1:
        row = cursor1.fetchone()
        if not row:
            break
        n = n+1
        print_result_raw(row)
    if n==0:
        print("No tuples matching the given query were found.")

# This call shows that a list of tuples may be retrieved at once.
def process_query3():
    cursor1.execute(query)
    print("Raw output for the query, all at once:")
    result = cursor1.fetchall()
    print_result_raw(result)

def print_result_raw(r):
    print(r)

print("")

connection1 = my_odbc_connect.establish_connection(db_name,user_name,pwd)
print("")
cursor1 = my_odbc_cursor.establish_cursor(connection1)
print("")
process_query()
print("")



#!/usr/bin/python
# To use python3, append "3" to the above line like this: #!/usr/bin/python3
# A basic program which connects to an ODBC database.
# Instead of prompting, this program takes its arguments from the command line.
# The ODBC database name must be described in the ODBC configuration file.
# ~/.odbc.ini under Unix/Linux.
# The arguments are <odbc_db_name> <user_id>
# If the third argument is -p, then there is a prompt for the password.
# Otherwise, the third argument is the password.
# Stephen J. Hegner 19 September 2011.
# Modified for Python 3 compatibility 21 February 2014.

### This script has been tested with both Python2 and Python3
### under PostgreSQL and MySQL running on Debian 7 Linux.
### IMPORTANT: For PostgreSQL:
###      the ANSI driver psqlodbca.so must be used for Python2;
###      the Unicode driver psqlodbcw.so must be used for Python3.
### For other Linux distributions which use Unicode in the OS (e.g., Ubuntu)
### it may be necessary to use psqlodbcw.so for Python2 as well.
### For MySQL, the driver libmyodbc.so works for both Python2 and Python3.
from __future__ import print_function

import pyodbc
import sys
import getpass
import my_odbc_connect
import my_odbc_cursor


def echo_args():
    for arg in range(0,len(sys.argv)):
        print("arg[%s]=%s" % (arg, sys.argv[arg]))

def commit_updates(c):
    print("Committing the updates.")
    c.commit()

def handle_query(con,curs):
    odbc_ssn = sys.argv[4]
    odbc_pno = sys.argv[5]
    if sys.argv[6] == 'NULL':
        odbc_hrs = None
    else:
        odbc_hrs = round(float(sys.argv[6]),1)  # cast to float and round

    # Queries
    qCheck = "SELECT * FROM Works_on WHERE ESSN=? AND PNo=?"
    query0 = "DELETE FROM Works_on WHERE ESSN=? AND PNo=?"
    query1 = "INSERT INTO Works_on VALUES (?,?,?)"
    query2 = "UPDATE Works_on SET Hours=? WHERE ESSN=? AND PNo=?"

    # Handle hours parameter
    if (odbc_hrs < 0.0 and (sys.argv[6]!='NULL')) or (odbc_hrs > 40.0 and (sys.argv[6]!='NULL')):
        print("ERROR: Hours must be NULL or between 0 and 40.", file=sys.stderr)
        sys.exit()

    elif (sys.argv[6] == '0'):
        #Check if tuple exists
        curs.execute(qCheck,odbc_ssn,odbc_pno)
        result = curs.fetchall()

        if not result:
            print("DELETE FAILED: There is no entry for employee %s on project number %s."%(odbc_ssn,odbc_pno), file=sys.stderr)
            sys.exit()
        else:
            # Delete employee from project
            try:
                curs.execute(query0,odbc_ssn,odbc_pno)
                print("Deleted entire entry for employee %s for project number %s in Works_on"%(odbc_ssn,odbc_pno))
            except pyodbc.IntegrityError, why:
                print("The update would violate an integrity constraint.")
                print("The reason is:", why)
    else:
        #Check if employee works on project, if so update else insert new tuple
        curs.execute(qCheck,odbc_ssn,odbc_pno)
        result = curs.fetchall()
        if not result:
            # Insert tuple
            try:
                curs.execute(query1,odbc_ssn,odbc_pno,odbc_hrs)
                print("Number of hours which employee %s works on project %s successfully changed to %s" % (odbc_ssn,odbc_pno,odbc_hrs), file=sys.stderr)
            except pyodbc.IntegrityError, why:
                print("The update would violate an integrity constraint.")
                print("The reason is:", why)
        else:
            # Update tuple
            try:
                curs.execute(query2,odbc_hrs,odbc_ssn,odbc_pno)
                print("Number of hours which employee %s works on project %s successfully changed to %s" % (odbc_ssn,odbc_pno,odbc_hrs), file=sys.stderr)
            except pyodbc.IntegrityError, why:
                print("The update would violate an integrity constraint.")
                print("The reason is:", why)




# Check number of arguments
if len(sys.argv) != 7:
    print("Not correct number of arguments. Usage: ./chghrs <DBName> <UserID> <password> <SSN> <PNo> <Hours>.")
    sys.exit()

# Assign arguments
db_name = sys.argv[1]
user_name = sys.argv[2]
pwd = sys.argv[3]
# Establish connection and execute query
connection = my_odbc_connect.establish_connection(db_name,user_name,pwd)
cursor = my_odbc_cursor.establish_cursor(connection)
handle_query(connection,cursor)
commit_updates(connection)
my_odbc_cursor.close_cursor(cursor)
my_odbc_connect.close_connection(connection)

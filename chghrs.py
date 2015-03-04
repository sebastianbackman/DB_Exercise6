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

import pyodbc
import sys
import getpass
import my_odbc_connect as odbc_con
import my_odbc_cursor as odbc_curs


def echo_args():
    for arg in range(0,len(sys.argv)):
        print("arg[%s]=%s" % (arg, sys.argv[arg]))

def handle_query(con):
    odbc_ssn = sys.argv[4]
    odbc_pno = sys.argv[5]
    odbc_hrs = round(float(sys.argv[6]),1)  # cast to float and round

    curs = odbc_curs.establish_cursor(con)

    # Handle hours parameter
    if odbc_hrs < 0.0 or odbc_hrs > 40.0:
        print("Hours must be NULL or between 0 and 40.")
        return 0
    elif (sys.argv[6] == '0'):
        print("hej")
        # Delete employee from project
        query = "DELETE FROM Works_on WHERE (SSN='%s') AND (PNo='%s')" % (odbc_ssn,odbc_pno)
        print(query)
    else:
        #CHECK IF EMPLOYEE WORKS ON PNO
        qCheck = "SELECT * FROM Works_on WHERE (ESSN='%s') AND (PNo='%s')" % (odbc_ssn,odbc_pno)
        curs.execute(qCheck)
        print("Raw output for the query, all at once:")
        result = curs.fetchall()
        print(result)
        # IF EMPLOYEE WORKS ON PNO
        query = "UPDATE Works_on SET Hours = %s WHERE (ESSN='%s') AND (PNo='%s')" % (odbc.hrs,odbc.hrs,odbc.pno)

    odbc_curs.close_cursor(curs)

# Check number of arguments
if len(sys.argv) != 7:
    print("Not correct number of arguments. Usage: ./chghrs <DBName> <UserID> <password> <SSN> <PNo> <Hours>.")
    sys.exit()

# Show the arguments for this test program.
echo_args()
# Now establish and close the connection using them.
odbc_db_name = sys.argv[1]
odbc_user_name = sys.argv[2]
odbc_pwd = sys.argv[3]

connection = odbc_con.establish_connection(odbc_db_name,odbc_user_name,odbc_pwd)
handle_query(connection)
close_connection(connection)

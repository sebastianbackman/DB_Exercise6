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

# sys.argv is a list of the command-line arguments.
# sys.argv[0] is the calling command itself.

def echo_args():
    for arg in range(0,len(sys.argv)):
        print("arg[%s]=%s" %  (arg, sys.argv[arg]))

def establish_connection():
    odbc_db_name = sys.argv[1]
    odbc_user_name = sys.argv[2]
    if sys.argv[3] == "-p":
        odbc_pwd = getpass.getpass("Enter the database password: ")
    else:
        odbc_pwd = sys.argv[3]
    try:
        c = pyodbc.connect("DSN="+odbc_db_name+";Uid="+odbc_user_name+";PWD="+odbc_pwd);
    except:
        print("ODBC connection failed.")
    else:
        print("ODBC connection: %s" % c)
        return c

def close_connection(c):
    print("Closing the connection.")
    c.close()

# Show the arguments for this test program.
echo_args()
# Now establish and close the connection using them.
connection1 = establish_connection()
close_connection(connection1)
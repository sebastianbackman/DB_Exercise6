# Python commands to open and close ODBC connections.
# Stephen J. Hegner 21 February 2014.
# Repaired to handle autocommit correctly 22.02.2015

import sys
import pyodbc
import getpass

# Function to establish a connection:        

def establish_connection(odbc_db_name,odbc_user_name,odbc_pwd):
    if odbc_pwd == "-p":
        odbc_pwd = getpass.getpass("Enter the database password: ")
    try:
        c = pyodbc.connect("DSN="+odbc_db_name+";Uid="+odbc_user_name+";PWD="+odbc_pwd);
    except:
        print("ODBC connection failed.")
    else:
        print("ODBC connection: %s" % c)
        return c
    
# Close the connection.    
def close_connection(c):
    c.close()
    print("Closing the connection.")

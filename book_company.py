# An ODBC program to create the ElMasri/Navathe Company database.
#   Stephen J. Hegner, Department of Computing Science, Umea University, Sweden
#   hegner@cs.umu.se, 04.08.2011

import sys
import pyodbc
import getpass
# Need to include the current directory in the search path:
sys.path.append('./') 
# It is probably necessary to alter or comment out the above line in
# an MS Windows installation.
# To put the current directory at the beginning of the search path,
# use this instead:
# sys.path.insert(0, './')
from company_tables import *
from company_tuples import *

def establish_connection():
    odbc_db_name = raw_input("Enter the ODBC database name: ")
    odbc_user_name = raw_input("Enter the database user ID: ")
    odbc_pwd = getpass.getpass("Enter the database password (ignored with ident authentication): ")
    try:
        c = pyodbc.connect("DSN="+odbc_db_name+";Uid="+odbc_user_name+";PWD="+odbc_pwd)
    except:
        print "ODBC connection failed."
    else:
        print "ODBC connection: %s" % c
        return c

def establish_cursor():
    c = cnxn.cursor()
    print "Cursor", c, "established."
    return c

def close_cursor(c):
    c.close()
    print "Cursor", c, "closed."

def commit_trans(c):
    cursor.execute("commit;")
    print "Transaction", c, "committed."

def close_connection(c):
    c.close()
    print "Connection", c, "closed."

def create_tables(t):
    i=0
    print len(t)
    while i < len(t):
        result = cursor.execute(t[i])
        print result
        print "Table "+table_names[i]+" created"
        i = i+1

def insert_tuples_1(r,t):
     i=0
     while i < len(t):
         cursor.execute("insert into "+r+" values "+t[i])
         print "insert into "+r+" values "+t[i]
         i = i+1

def insert_tuples():
    insert_tuples_1("Employee",employee_tuples)
    insert_tuples_1("Department",department_tuples)
    insert_tuples_1("Dept_Locations",dept_locations_tuples)
    insert_tuples_1("Project",project_tuples)
    insert_tuples_1("Works_On",works_on_tuples)
    insert_tuples_1("Dependent",dependent_tuples)

def add_constraints():
    result = cursor.execute(sql_add_constraints)
    print result
    print "Final constraints added."

print ""
cnxn = establish_connection()
print ""
cursor = establish_cursor()
print ""
create_tables(table_tup)
print ""
insert_tuples()
print ""
add_constraints()
print ""
commit_trans(cursor)
print ""
close_cursor(cursor)
print ""
close_connection(cnxn)




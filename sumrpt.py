#!/usr/bin/python
# A that program connects to an ODBC database and calculates
# a summary.
# It also illustrates the raw format of the returned result.
# Sebastian Backman, John Bergman, 5 March 2015

### This script has been tested with both Python
### under PostgreSQL running on Debian 7 Linux.

import pyodbc	
import sys

# Functions loaded from local files.
import my_odbc_connect
import my_odbc_cursor

query = "SELECT SSN, LName, FName, MInit, Salary, Hours, Pno FROM Employee JOIN Works_on ON (SSN=ESSN) ORDER BY SSN"

db_name= sys.argv[1]
user_name = sys.argv[2]
pwd = sys.argv[3]

def process_query():
    cursor1.execute(query)
    print("| %-12s | %-12s | %-12s | %-12s | %-12s | %-12s | %-12s |" % ("SSN", "LName", "FName", "MInit", "Known_Hrs", "Unknown_Hrs", "Overtime"))
    print("|--------------|--------------|--------------|--------------|--------------|--------------|--------------|")

    n=0
    Tot_Hrs=0
    row1 = cursor1.fetchone()
    SSN = row1[0]
    OldSSN = SSN
    Unknown_Hrs = 0 
    Num_Unknown_Hrs = 0   
    while 1:
        n = n+1
        if SSN == OldSSN:
            if row1[5] != None:
                Tot_Hrs = Tot_Hrs+row1[5]
            else:
                Unknown_Hrs = 1
                Num_Unknown_Hrs = Num_Unknown_Hrs+1
        else:
            print_result(Oldrow1, Tot_Hrs, Unknown_Hrs, Num_Unknown_Hrs)

            Num_Unknown_Hrs=0
            Unknown_Hrs = 0
            
            if row1[5] == None:
                Num_Unknown_Hrs = Num_Unknown_Hrs+1
                Unknown_Hrs = 1
                Tot_Hrs = 0
            else:
                Tot_Hrs = row1[5]                            
        
        OldSSN = SSN
        Oldrow1 = row1
        row1 = cursor1.fetchone()
        
        if not row1:
            print_result(Oldrow1, Tot_Hrs, Unknown_Hrs, Num_Unknown_Hrs)
            break
        SSN=row1[0]

    if n==0:
        print("No tuples matching the given query were found.") 
      
def print_result(r, Tot_Hrs, Unknown_Hrs, Num_Unknown_Hrs):
    if Unknown_Hrs == 1:
        U="Yes"
    else:
        U="No"

    if Tot_Hrs > 40:
        Overtime = "Yes"
    elif Tot_Hrs + 40 * Num_Unknown_Hrs <= 40:
        Overtime = "No"
    else:
        Overtime = "?"
    print("| %-12s | %-12s | %-12s | %-12s | %-12s | %-12s | %-12s |" % (r[0], r[1], r[2], r[3], Tot_Hrs, U, Overtime))    


def print_result_raw(r):
    print(r)

print("")
connection1 = my_odbc_connect.establish_connection(db_name,user_name,pwd)
print("")
cursor1 = my_odbc_cursor.establish_cursor(connection1)
print("")
process_query()
print("")
my_odbc_cursor.close_connection(connection1)


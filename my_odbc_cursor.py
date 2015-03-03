# Python commands to open and close a single cursor named c.
# Stephen J. Hegner 21 February 2014.

import sys
import pyodbc

# For Python2 the input function is called raw_input.
if  sys.version_info<(3,0,0):
        input = raw_input

def establish_cursor(cnxn):
    c = cnxn.cursor()
    print("Cursor", c, "established.")
    return c

def close_cursor(c):
    c.close()
    print("Cursor", c, "closed.")


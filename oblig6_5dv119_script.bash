#!/bin/bash

# Test script for the olbligatory ODBC exercise, 5DV119, V13.
# Run this script with $1=database_name, $2=user_id, $3=password
# on the _original_ company database of the textbook.
# Example: ./oblig6_5dv119_script.bash company c5dv119_vt13_jsuser foo
# For PostgreSQL with ident authenticaion, the password is ignored.
# If no password is given, it is set to the empty string.
# Stephen J. Hegner 24.10.2011
# Revised 25.02.2013

dbname=$1
uname=$2
pwd=${3:-"\"\""}

declare -i case_number=1

function write_summary
 {
   printf "\n\nSummary report:\n\n"
   ./sumrpt $dbname $uname $pwd
 }

function change_hours
 {
   printf "\n\nTest case $case_number: change hours for SSN=$1 and PNo=$2 to $3:\n\n"
   ./chghrs $dbname $uname $pwd $1 $2 $3
   case_number=$case_number+1
   write_summary
 }

write_summary
change_hours 666666666 10 40
change_hours 66666666T 10 40
change_hours 123456789 12 30
change_hours 123456789  1 41
change_hours 123456789  1 -10
change_hours 999887777 30 30.5
change_hours 123456789 10 30
change_hours 123456789 20 10
change_hours 123456789  3 10
change_hours 453453453  3 NULL
change_hours 453453453  1 10
change_hours 453453453 10 20
change_hours 453453453  3 10
change_hours 453453453  1 NULL
change_hours 453453453  1 0
change_hours 453453453 30 0
change_hours 999887777 30 0
change_hours 888665555 20 0
change_hours 987654321 20 NULL
change_hours 666884444 20 NULL
# An ODBC program to create the ElMasri/Navathe Company database.
# Tuple definitions.
#   Stephen J. Hegner, Department of Computing Science, Umea University, Sweden
#   hegner@cs.umu.se, 04.08.2011
# Fixed capitalization error 04.03.2014

table_names = ("Employee", "Department", "Dept_Locations", 
               "Project", "Works_On", "Dependent")

table_tup = ( "CREATE TABLE Employee \
      (FName    Varchar(15)     not null, \
       MInit    Char(1), \
       LName    Varchar(15)     not null, \
       SSN      Char(9)         not null, \
       BDate    Date, \
       Address  Varchar(30), \
       Sex      Char(1), \
       Salary   Decimal(10,2), \
       Super_SSN Char(9), \
       DNo      Int             not null, \
       Constraint pkey_emp primary key (SSN), \
       Constraint fkey_emp1 foreign key (Super_SSN) \
       references Employee (SSN));",

   "CREATE TABLE Department  \
      (DName    Varchar(15)     not null, \
       DNumber  Int             not null, \
       MgrSSN   Char(9)         not null, \
       MgrStartDate Date, \
       Constraint pkey_dept primary key (DNumber), \
       Constraint ckey_dept unique (DName), \
       Constraint fkey_dept foreign key (MgrSSN)  \
       references Employee (SSN));",

   "CREATE TABLE Dept_Locations   \
      (Dnumber     Int     not null, \
       Dlocation   varchar(15) not null, \
       Constraint pkey_dep_loc primary key (DNumber, DLocation), \
       Constraint fkey_dep_loc foreign key (Dnumber) \
       references Department (DNumber));",

   "CREATE TABLE Project  \
      (PName   Varchar(15) not null, \
       PNumber Int     not null, \
       PLocation   Varchar(15), \
       DNum        Int     not null, \
       Constraint pkey_proj primary key (PNumber), \
       Constraint ckey_proj unique (PName), \
       Constraint fkey_proj_1 foreign key (DNum) \
       references Department (DNumber));",

   "CREATE TABLE Works_On  \
      (ESSN    Char(9)     not null, \
       PNo     Int     not null, \
       Hours   Decimal(3,1), \
       Constraint pkey_works_on primary key (ESSN, PNo), \
       Constraint fkey_works_on_1 foreign key (ESSN) \
       references Employee (SSN), \
       Constraint fkey_works_on_2 foreign key (PNo) \
       references Project (PNumber));",

   "CREATE TABLE Dependent  \
      (ESSN    Char(9)     not null, \
       Dependent_Name Varchar(15)  not null, \
       Sex     Char(1), \
       BDate   Date, \
       Relationship Varchar(8), \
       Constraint pkey_depe primary key (ESSN, Dependent_Name), \
       Constraint fkey_depe foreign key (ESSN) \
       references Employee (SSN));"
   )

# Because Access does not support deferrred constraint checking, 
#   circular foreign key constraints must be deferred until the
#   database has been created.
sql_add_constraints = "ALTER TABLE Employee \
      Add Constraint fkey_emp2 foreign key (DNo) \
      references Department (DNumber);"

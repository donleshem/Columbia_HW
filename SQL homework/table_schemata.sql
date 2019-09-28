-- departments table 
create table departments(
dept_no VARCHAR, 
dept_name VARCHAR,
primary key (dept_no)
);

-- dept_manager table
create table dept_manager(
dept_no VARCHAR, 
emp_no int,
from_date date,
to_date date,
foreign key(dept_no) references departments (dept_no),
foreign key(emp_no) references employees (emp_no), 
primary key (emp_no,dept_no)
);

--dept_emp table
create table dept_emp(
emp_no int, 
dept_no VARCHAR,
from_date date,
to_date date,
foreign key(dept_no) references departments (dept_no),
foreign key(emp_no) references employees (emp_no), 
primary key (emp_no,dept_no)
);

--salaries table
create table salaries(
emp_no int, 
salary int,
from_date date,
to_date date,
foreign key(emp_no) references employees (emp_no), 
primary key (emp_no)
);

--titles table
create table titles(
emp_no int, 
title VARCHAR,
from_date date,
to_date date,
foreign key(emp_no) references employees (emp_no)
);

--employees table
create table employees(
emp_no int, 
birth_date date,
first_name VARCHAR,
last_name VARCHAR,
gender VARCHAR,
hire_date date,
primary key (emp_no)
);

--viewing the tables
select * from departments
select * from dept_emp
select * from dept_manager
select * from employees
select * from salaries
select * from titles
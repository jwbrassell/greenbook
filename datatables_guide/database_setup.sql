-- Create the database
CREATE DATABASE IF NOT EXISTS employees;
USE employees;

-- Create the employees table
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(100),
    office VARCHAR(100),
    age INT,
    start_date DATE,
    salary DECIMAL(10, 2)
);

-- Insert sample data
INSERT INTO employees (name, position, office, age, start_date, salary) VALUES
    ('John Doe', 'Software Engineer', 'New York', 30, '2020-01-15', 85000.00),
    ('Jane Smith', 'Product Manager', 'San Francisco', 35, '2019-03-20', 110000.00),
    ('Mike Johnson', 'UI Designer', 'Los Angeles', 28, '2021-06-10', 75000.00),
    ('Sarah Williams', 'Data Analyst', 'Chicago', 32, '2020-09-01', 80000.00),
    ('David Brown', 'DevOps Engineer', 'Seattle', 34, '2018-11-15', 95000.00),
    ('Emily Davis', 'QA Engineer', 'Boston', 29, '2021-02-28', 70000.00),
    ('Michael Wilson', 'Full Stack Developer', 'Austin', 31, '2019-07-12', 90000.00),
    ('Lisa Anderson', 'Project Manager', 'Denver', 38, '2017-04-05', 105000.00),
    ('Robert Taylor', 'Systems Architect', 'Portland', 40, '2016-08-22', 120000.00),
    ('Jennifer Martin', 'Frontend Developer', 'Miami', 27, '2022-01-10', 72000.00),
    ('William Thompson', 'Backend Developer', 'Atlanta', 33, '2020-05-18', 88000.00),
    ('Elizabeth Clark', 'Scrum Master', 'Houston', 36, '2019-11-30', 95000.00),
    ('James Rodriguez', 'Database Administrator', 'Phoenix', 39, '2018-03-25', 98000.00),
    ('Patricia Lee', 'Security Engineer', 'Dallas', 34, '2020-07-08', 92000.00),
    ('Thomas White', 'Mobile Developer', 'San Diego', 31, '2021-09-15', 85000.00);

-- Create an index for improved search performance
CREATE INDEX idx_employee_search ON employees(name, position, office);

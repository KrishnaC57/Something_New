## Spark and SQL Interview Scenerio Questions

### Table of Contents

|No| Scenerios                                                                |
|--|--------------------------------------------------------------------------|
|1 |[Scenerio-1](#scenerio-1)                                                 |
|2 |[Scenerio-2](#scenerio-2)                                                 |
|3 |[Scenerio-3](#scenerio-3)                                                 |
|4 |[Scenerio-4](#scenerio-4)                                                 |
|5 |[Scenerio-5](#scenerio-5)                                                 |
|6 |[Scenerio-6](#scenerio-6)                                                 |
|7 |[Scenerio-7](#scenerio-7)                                                 |
|8 |[Scenerio-8](#scenerio-8)                                                 |
|9 |[Scenerio-9](#scenerio-9)                                                 |
|10|[Scenerio-10](#scenerio-10)                                               |
|11|[Scenerio-11](#scenerio-11)                                               |
|12|[Scenerio-12](#scenerio-12)                                               |
|13|[Scenerio-13](#scenerio-13)                                               |
|14|[Scenerio-14](#scenerio-14)                                               |
|15|[Scenerio-15](#scenerio-15)                                               |
|16|[Scenerio-16](#scenerio-16)                                               |
|17|[Scenerio-17](#scenerio-17)                                               |
|18|[Scenerio-18](#scenerio-18)                                               |
|19|[Scenerio-19](#scenerio-19)                                               |
|20|[Scenerio-20](#scenerio-20)                                               |
|21|[Scenerio-21](#scenerio-21)                                               |
|22|[Scenerio-22](#scenerio-22)                                               |
|23|[Scenerio-23](#scenerio-23)                                               |
|24|[Scenerio-24](#scenerio-24)                                               |
|25|[Scenerio-25](#scenerio-25)                                               |
|26|[Scenerio-26](#scenerio-26)                                               |
|27|[Scenerio-27](#scenerio-27)                                               |
|28|[Scenerio-28](#scenerio-28)                                               |
|29|[Scenerio-29](#scenerio-29)                                               |
|30|[Scenerio-30](#scenerio-30)                                               |
|31|[Scenerio-31](#scenerio-31)                                               |
|32|[Scenerio-32](#scenerio-32)                                               |
|33|[Scenerio-33](#scenerio-33)                                               |
|34|[Scenerio-34](#scenerio-34)                                               |
|35|[Scenerio-35](#scenerio-35)                                               |
|36|[Scenerio-36](#scenerio-36)                                               |
|37|[Scenerio-37](#scenerio-37)                                               |
|38|[Scenerio-38](#scenerio-38)                                               |
|39|[Scenerio-39](#scenerio-39)                                               |
|40|[Scenerio-40](#scenerio-40)                                               |
|41|[Scenerio-41](#scenerio-41)                                               |
|42|[Scenerio-42](#scenerio-42)                                               |
|43|[Scenerio-43](#scenerio-43)                                               |


### Scenerio-1 
#### A person who likes bananas and apples only
#### Input :-
```
+---------+--------+
| persons | fruits |
+---------+--------+
| P1      | Apple  |
| P1      | Banana |
| P1      | Mango  |
| P3      | Banana |
| P3      | Apple  |
| P2      | Apple  |
| P2      | Mango  |
+---------+--------+
```
#### Expected Output :- 
```
+---------+
| persons |
+---------+
| P3      |
+---------+
```
#### Solution :- 
PySpark - [S-1.py](<SFiles/S-1.py>) <br>
SQL - 
```
SELECT persons
FROM person_data
GROUP BY persons
HAVING 
    SUM(fruits = 'Banana') > 0 AND
    SUM(fruits = 'Apple') > 0 AND
    SUM(fruits NOT IN ('Banana', 'Apple')) = 0;

--------------------------------------
SELECT DISTINCT persons
FROM person_data AS t1
WHERE fruits IN ('Banana', 'Apple')
  AND NOT EXISTS (
    SELECT 1
    FROM person_data AS t2
    WHERE t2.persons = t1.persons
      AND t2.fruits NOT IN ('Banana', 'Apple')
  );
```

**[⬆ Back to Top](#table-of-contents)**

### Scenerio-2 
#### (Difference between fruits sold per each day)
#### Input :- 
```
+------------+---------+----------+
| sale_date  | fruit   | num_sold |
+------------+---------+----------+
| 18-11-2022 | apple   |       10 |
| 18-11-2022 | oranges |        8 |
| 19-11-2022 | apple   |        5 |
| 19-11-2022 | oranges |        5 |
| 20-11-2022 | apple   |        7 |
| 20-11-2022 | oranges |       10 |
+------------+---------+----------+
```
#### Expected Output :- 
```
+------------+------------+
| sale_date  | fruit_diff |
+------------+------------+
| 18-11-2022 |          2 |
| 19-11-2022 |          0 |
| 20-11-2022 |         -3 |
+------------+------------+
```
#### Solution :- 
PySpark - [S-2.py](<SFiles/S-2.py>) <br>
SQL - 
```
create table saletab(sale_date varchar(10), fruit varchar(8), num_sold int);
insert into saletab values('18-11-2022','apple',10),
('18-11-2022','oranges',8),
('19-11-2022','apple',5),
('19-11-2022','oranges',5),
('20-11-2022','apple',7),
('20-11-2022','oranges',10);

select * from saletab;

with diff_cte as(
select sale_date, (num_sold - (lead(num_sold) over(partition by sale_date order by sale_date) )) as fruit_diff
from saletab
)

select * from diff_cte
where fruit_diff is not null;
```

**[⬆ Back to Top](#table-of-contents)**

### Scenerio-3 
#### (Remove special values from table)
#### Input :- 
```
+------+
| id   |
+------+
| 111  |
| 222  |
| *    |
| 333  |
| 444  |
| ?5?  |
+------+
```
#### Expected Output :- 
```
+------+
| id   |
+------+
| 111  |
| 222  |
| 333  |
| 444  |
+------+
```
#### Solution :- 
PySpark - [S-3.py](<SFiles/S-3.py>) <br>
SQL - 
```
create table tab(id varchar(4));
insert into tab values('111'),('222'),('*'),('333'),('444'),('???');

select * from tab;
select * from tab where id regexp('^[0-9]+$');

--Other examples
select * from tab where id regexp('[0-9]');
select * from tab where id regexp('[?*]');
```

**[⬆ Back to Top](#table-of-contents)**

### Scenerio-4 
#### (Find Avg salary of employees for each department and order the employees with a department by age)
#### Input :- 
```
+---------+------+------------+--------+
| Name    | Age  | Department | salary |
+---------+------+------------+--------+
| ram     |   20 | Finance    |  50000 |
| Sudeep  |   25 | Sales      |  30000 |
| Suresh  |   22 | Finance    |  50000 |
| Pradeep |   28 | Finance    |  20000 |
| Iqbal   |   22 | Sales      |  20000 |
+---------+------+------------+--------+
```
#### Expected Output :- 
```
+------------+---------+------+--------+------------+
| Department | Name    | age  | Salary | avg_sal    |
+------------+---------+------+--------+------------+
| Finance    | Pradeep |   28 |  20000 | 40000.0000 |
| Finance    | Suresh  |   22 |  50000 | 40000.0000 |
| Finance    | ram     |   20 |  50000 | 40000.0000 |
| Sales      | Sudeep  |   25 |  30000 | 25000.0000 |
| Sales      | Iqbal   |   22 |  20000 | 25000.0000 |
+------------+---------+------+--------+------------+
```
#### Solution :- 
PySpark - [S-4.py](<SFiles/S-4.py>) <br>
SQL - 
```
CREATE TABLE raw_data (Name varchar(8),Age Int, Department varchar(10), salary int);

INSERT INTO raw_data VALUES ('ram', 20, 'Finance',50000),
                            ('Sudeep', 25, 'Sales',30000),
                            ('Suresh', 22, 'Finance',50000),
                            ('Pradeep', 28, 'Finance',20000),
                            ('Iqbal', 22, 'Sales',20000);

SELECT * FROM raw_data;

Select Department, Name, age,Salary, avg(salary) over(partition by Department) avg_sal
from raw_data
Order by Department, age desc;
```

**[⬆ Back to Top](#table-of-contents)**

### Scenerio-5 
* You have a table with 2 columns
* 1st Row should have India in country column
* 2nd row should have highest population irrespective of country
* 3rd row should have lowest population
#### Input :- 
```
+---------+------------+
| country | population |
+---------+------------+
| Brazil  | 10000      |
| India   | 15000      |
| US      | 20000      |
| UK      | 12000      |
| Europe  | 12000      |
+---------+------------+
```
#### Expected Output :- 
```
+---------+------------+
| country | population |
+---------+------------+
| India   | 15000      |
| US      | 20000      |
| Brazil  | 10000      |
+---------+------------+
```
#### Solution :- 
PySpark - [S-5.py](<SFiles/S-5.py>) <br>
SQL - 
```
CREATE TABLE country_population (country varchar(8),population varchar(10));

INSERT INTO country_population VALUES ('Brazil', 10000),('India', 15000),
('US', 20000),('UK', 12000),('Europe', 12000);

SELECT * FROM country_population;

(
    SELECT * FROM country_population WHERE country = 'India'
)
UNION ALL
(
    SELECT * FROM country_population 
    WHERE country != 'India'
    ORDER BY population DESC
    LIMIT 1
)
UNION ALL
(
    SELECT * FROM country_population 
    WHERE country != 'India'
    ORDER BY population ASC
    LIMIT 1
);
```

**[⬆ Back to Top](#table-of-contents)**

### Scenerio-6 
#### (Find the user_id which are having more outgoing messages for Feb month compared to Jan month)
#### Input :-
```
+---------+---------------+----------+------------+
| user_id | mobile_number | msg_type | mob_date   |
+---------+---------------+----------+------------+
|   12345 | 9988445566    | outgoing | 2022-01-23 |
|   67890 | 8899445566    | incoming | 2022-02-01 |
|   78915 | 7799884455    | outgoing | 2022-01-23 |
|   12345 | 6698112244    | outgoing | 2022-02-02 |
|   12345 | 5598445566    | incoming | 2022-01-24 |
|   12345 | 1199885544    | outgoing | 2022-02-05 |
+---------+---------------+----------+------------+
```
#### Expected Output :- 
```
+---------+
| user_id |
+---------+
|   12345 |
+---------+
```
#### Solution :- 
PySpark - [S-6.py](<SFiles/S-6.py>) <br>
SQL -
```
CREATE TABLE mobile_data (
    user_id INT,
    mobile_number TEXT,
    msg_type TEXT,
    mob_date DATE
);

INSERT INTO mobile_data VALUES
(12345, '9988445566', 'outgoing', '2022-01-23'),
(67890, '8899445566', 'incoming', '2022-02-01'),
(78915, '7799884455', 'outgoing', '2022-01-23'),
(12345, '6698112244', 'outgoing', '2022-02-02'),
(12345, '5598445566', 'incoming', '2022-01-24'),
(12345, '1199885544', 'outgoing', '2022-02-05');

select * from mobile_data;


SELECT feb.user_id
FROM (
    SELECT user_id, COUNT(*) AS feb_count
    FROM mobile_data
    WHERE msg_type = 'outgoing' AND MONTH(mob_date) = 2
    GROUP BY user_id
) AS feb
JOIN (
    SELECT user_id, COUNT(*) AS jan_count
    FROM mobile_data
    WHERE msg_type = 'outgoing' AND MONTH(mob_date) = 1
    GROUP BY user_id
) AS jan
ON feb.user_id = jan.user_id
WHERE feb.feb_count > jan.jan_count;
```

**[⬆ Back to Top](#table-of-contents)**

### Scenerio-7
### (Find Total Tickets, Closed Tickets, Avg Resolution Hours)
#### Input :- 
```
+----------+----------------+-------------+-----------------+
| TicketID | AssignedTo     | Status      | ResolutionHours |
+----------+----------------+-------------+-----------------+
| TKT-1001 | Alex Johnson   | Resolved    |            2.50 |
| TKT-1002 | Priya Sharma   | In Progress |            4.00 |
| TKT-1003 | Alex Johnson   | Closed      |            1.50 |
| TKT-1004 | Michael Chen   | Open        |            0.00 |
| TKT-1005 | Priya Sharma   | Resolved    |            6.00 |
| TKT-1006 | Michael Chen   | Pending     |            3.50 |
| TKT-1007 | Alex Johnson   | Closed      |            2.00 |
| TKT-1008 | Sarah Williams | In Progress |            5.00 |
| TKT-1009 | Priya Sharma   | Resolved    |            7.50 |
| TKT-1010 | Sarah Williams | Open        |            0.00 |
| TKT-1011 | Michael Chen   | Resolved    |            4.50 |
| TKT-1012 | Alex Johnson   | In Progress |            3.00 |
+----------+----------------+-------------+-----------------+
```
#### Expected Output :- 
```
+--------------+--------------+---------------+--------------------+
| AssignedTo   | TotalTickets | ClosedTickets | AvgResolutionHours |
+--------------+--------------+---------------+--------------------+
| Alex Johnson |            4 |             2 |           1.750000 |
| Priya Sharma |            3 |             0 |           0.000000 |
| Michael Chen |            3 |             0 |           0.000000 |
+--------------+--------------+---------------+--------------------+
```
#### Solution :- 
PySpark - [S-7.py](<SFiles/S-7.py>) <br>
SQL - 
```
CREATE TABLE Tickets
(
    TicketID VARCHAR(20) PRIMARY KEY,
    AssignedTo VARCHAR(100),
    Status VARCHAR(20),
    ResolutionHours DECIMAL(5,2)
);
 
INSERT INTO Tickets (TicketID, AssignedTo, Status, ResolutionHours)
VALUES
    ('TKT-1001', 'Alex Johnson', 'Resolved', 2.5),
    ('TKT-1002', 'Priya Sharma', 'In Progress', 4.0),
    ('TKT-1003', 'Alex Johnson', 'Closed', 1.5),
    ('TKT-1004', 'Michael Chen', 'Open', 0.0),
    ('TKT-1005', 'Priya Sharma', 'Resolved', 6.0),
    ('TKT-1006', 'Michael Chen', 'Pending', 3.5),
    ('TKT-1007', 'Alex Johnson', 'Closed', 2.0),
    ('TKT-1008', 'Sarah Williams', 'In Progress', 5.0),
    ('TKT-1009', 'Priya Sharma', 'Resolved', 7.5),
    ('TKT-1010', 'Sarah Williams', 'Open', 0.0),
    ('TKT-1011', 'Michael Chen', 'Resolved', 4.5),
    ('TKT-1012', 'Alex Johnson', 'In Progress', 3.0);
 
select * from Tickets;

Select AssignedTo, TotalTickets, ClosedTickets, COALESCE(AvgResolutionHours, 0) as AvgResolutionHours
From (select AssignedTo, count(*) as TotalTickets, 
      sum(case when Status = "Closed" then 1 else 0 end) as ClosedTickets, 
      avg(case when Status = "Closed" then ResolutionHours end) as AvgResolutionHours
    From Tickets
group by AssignedTo
having TotalTickets >2 ) as proctab;
```

**[⬆ Back to Top](#table-of-contents)**

### Scenerio-8
### (Write a SQL query to group the rows by id and concatenate all data values belonging to the same id into a single comma-separated string)
#### Input :- 
```
+------+------+
| id   | data |
+------+------+
|    1 |    1 |
|    1 |    2 |
|    1 |    3 |
|    2 |    4 |
|    2 |    5 |
|    3 |    6 |
|    3 |    4 |
+------+------+
```
#### Expected Output :- 
```
+------+-------+
| id   | data  |
+------+-------+
|    1 | 1,2,3 |
|    2 | 4,5   |
|    3 | 6,4   |
+------+-------+
```
#### Solution :- 
PySpark - [S-8.py](<SFiles/S-8.py>) <br>
SQL - 
```
Create table cat (id int, data integer);
Insert into cat values(1,1),(1,2),(1,3),(2,4),(2,5),(3,6),(3,4);
Select * from cat;

Select id, group_concat(data separator ',') as data from cat group by id;
```

**[⬆ Back to Top](#table-of-contents)**

### Scenerio-9 
#### (Find Followers Percentage)
#### Input :- 
```
+---------+-------------+
| user_id | follower_id |
+---------+-------------+
|       1 |           2 |
|       1 |           3 |
|       2 |           4 |
|       5 |           1 |
|       5 |           3 |
|      11 |           7 |
|      12 |           8 |
|      13 |           5 |
|      13 |          10 |
|      14 |          12 |
|      14 |           3 |
|      15 |          14 |
|      15 |          13 |
+---------+-------------+
```
#### Expected Output :- 
```
+---------+-------------------+
| user_id | famous_percentage |
+---------+-------------------+
|       1 |           15.3846 |
|       2 |            7.6923 |
|       5 |           15.3846 |
|      11 |            7.6923 |
|      12 |            7.6923 |
|      13 |           15.3846 |
|      14 |           15.3846 |
|      15 |           15.3846 |
+---------+-------------------+
```
#### Solution :- 
PySpark - [S-9.py](<SFiles/S-9.py>) <br>
SQL - 
```
create table famous (user_id INT, follower_id INT);
Insert Into famous values(1, 2), (1, 3), (2, 4), (5, 1), (5, 3), (11, 7), 
(12, 8), (13, 5), (13, 10), (14, 12), (14, 3), (15, 14), (15, 13);

Select * from famous;

with distinct_users as(
select user_id as users from famous
UNION
select follower_id as users from famous
),

follower_count as (
select user_id, count(follower_id ) as followers 
from famous 
group by user_id
)

select f.user_id, 
(f.followers * 100)/(select count(*) from distinct_users) as famous_percentage 
from follower_count as f;
```

**[⬆ Back to Top](#table-of-contents)**

### Scenerio-10
* Given a table containing a Person and a comma-separated list of fruits in their Basket
* Write a SQL query or PySpark program to transform the data so that:
    * Each unique fruit becomes a separate column.
    * If the person's basket contains that fruit, display Yes.
    * Otherwise, display No.
    * Keep one row per person.
#### Input :- 
```
+--------+---------------------+
| Person | Basket              |
+--------+---------------------+
| A      | Apple, Mango,Orange |
| B      | Apple               |
| C      | Guava,Cherry        |
| D      | Mango,Cherry,Orange |
+--------+---------------------+
```
#### Expected Output :- 
```
+--------+-------+-------+--------+-------+--------+
| Person | Apple | Mango | Orange | Guava | Cherry |
+--------+-------+-------+--------+-------+--------+
| A      | Yes   | Yes   | Yes    | No    | No     |
| B      | Yes   | No    | No     | No    | No     |
| C      | No    | No    | No     | Yes   | Yes    |
| D      | No    | Yes   | Yes    | No    | Yes    |
+--------+-------+-------+--------+-------+--------+
```
#### Solution :- 
PySpark - [S-10.py](<SFiles/S-10.py>) <br>
SQL -
```
CREATE TABLE Baskets (Person TEXT, Basket TEXT);

INSERT INTO Baskets VALUES ('A', 'Apple, Mango,Orange'),('B', 'Apple'),
('C', 'Guava,Cherry'),('D', 'Mango,Cherry,Orange');

SELECT * FROM Baskets;

Select Person, case when Basket like '%Apple%' then 'Yes' else 'No' end as Apple,
  case when Basket like '%Mango%' then 'Yes' else 'No' end as Mango,
  case when Basket like '%Orange%' then 'Yes' else 'No' end as Orange,
  case when Basket like '%Guava%' then 'Yes' else 'No' end as Guava,
  case when Basket like '%Cherry%' then 'Yes' else 'No' end as Cherry
From Baskets;
```

**[⬆ Back to Top](#table-of-contents)**

### Scenerio-11 
* Find CustomerType based on TotalOrders
* CustomerType Rules:
	* 1 order → New Customer
	* 2 to 5 orders → Regular Customer
	* More than 5 orders → VIP Customer
* output columns: CustomerID, CustName, TotalOrders, CustomerType
#### Input :- 
```
Customers table:
+------------+----------+
| CustomerID | CustName |
+------------+----------+
|          1 | John     |
|          2 | Mary     |
|          3 | David    |
|          4 | Sarah    |
|          5 | Robert   |
+------------+----------+
```
```
Orders Table:
+---------+------------+
| OrderID | CustomerID |
+---------+------------+
|     101 |          1 |
|     102 |          1 |
|     103 |          2 |
|     104 |          3 |
|     105 |          3 |
|     106 |          3 |
|     107 |          5 |
+---------+------------+
```
#### Expected Output :- 
```
+------------+----------+-------------+------------------+
| CustomerID | CustName | TotalOrders | CustomerType     |
+------------+----------+-------------+------------------+
|          1 | John     |           2 | Regular Customer |
|          2 | Mary     |           1 | New Customer     |
|          3 | David    |           3 | Regular Customer |
|          5 | Robert   |           1 | New Customer     |
+------------+----------+-------------+------------------+
```
#### Solution :- 
PySpark - [S-11.py](<SFiles/S-11.py>) <br>
SQL -
```
-- Create Customers table
CREATE TABLE Customers
(
  CustomerID INT PRIMARY KEY,
  CustName VARCHAR(100) NOT NULL
);
 
INSERT INTO Customers (CustomerID, CustName)
VALUES
(1, 'John'), (2, 'Mary'), (3, 'David'), (4, 'Sarah'), (5, 'Robert');


-- Create Orders table
CREATE TABLE Orders
(
  OrderID INT PRIMARY KEY,
  CustomerID INT NOT NULL,
 
  CONSTRAINT FK_Orders_Customers
  FOREIGN KEY (CustomerID)
  REFERENCES Customers(CustomerID)
);

INSERT INTO Orders (OrderID, CustomerID)
VALUES (101, 1), (102, 1), (103, 2), (104, 3), (105, 3), (106, 3), (107, 5);

Select * from Customers;
Select * from Orders;

----Query
Select *, (case when TotalOrders = 1 then "New Customer" 
                when TotalOrders between 2 and 5 then "Regular Customer"
                when TotalOrders >5 then "VIP Customer" end) as CustomerType
From (select c.CustomerID, CustName, count(*) as TotalOrders
			From Customers c inner join Orders o
			on c.CustomerID =o.CustomerID
			group by CustomerID, CustName
			) TotalOrdersTab;
```

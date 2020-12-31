# MPP-Shop-Assignment

#### Multi-Paradigm Programming Shop Assignment, GMIT 2020

Author: Slawomir Sowa <br>
Gitgub: https://github.com/Slawak1/<br>
email: G00376519@gmit.ie<br>
***
### Subject:
Add additional functionality to the shop program developed in the lecturer video series. 

### Functionality:
- The shop CSV should hold the initial cash value for the shop.
- Read in customer orders from a CSV file.
 * That file should include all the products they wish to buy and in what quantity
 * It should also include their name and their budget.
- The shop must be able to process the orders of the customer.
    - It is important that the state of the shop be consistent.
        * You should create customer test files (CSVs) which cannot be completed by the shop e.g. customer wants 400
            loaves of bread but the shop only has 20, or the customer wants 2 cans of coke but can only afford 1.
        * If these files don’t exist marks penalties will be applied.
    - Know whether or not the shop can fill an order
        * Thrown an appropriate error.
- Operate in a live mode, where the user can enter a product by name, specify a quantity, and pay for it. The user should
    be able to buy many products in this way.

### Project overview:


The folder contains three subfolders:
* C - folder with the application written in C (Procedural Programming),
* Python - a folder with an application written in Python (Procedural Programming),
* Python_oop - folder with an application written in Python OOP (Object Oriented Programming).

CSV files:
- stock.csv - contains information about shop stock and cash
- order.csv - customer name, budget and customer shopping list
- test_low_budget.csv - test CSV for "low budget" case
- test_not_enough_stock.csv - test CSV for "not enough stock" case
- test_not_in_stock.csv - test CSV for "not in stock" case

Files txt and pdf
- readme.txt - istruction how to run project 
- report.pdf - short description and comparison of the programming paradigms used in the project

### Instruction:

* Procedural project in C:
    Navigate to folder G00376519 -Slawomir Sowa - Assignment/c/
    compile program: gcc shop.c
    run: a.exe

* Procedural project in Python:
    Navigate to folder G00376519 -Slawomir Sowa - Assignment/python/ 
    run: python shop.py

* OOP project in python:
    Navigate to folder G00376519 -Slawomir Sowa - Assignment/python_oop/
    run: python start_shop

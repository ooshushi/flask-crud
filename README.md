Loan Management System

Prerequisites
Python 3.x
Flask
Flask-MySQLdb
MySQL

Features
Login/Logout: Users can log in to the system using a username and password. The system uses a simple in-memory user authentication mechanism.

View Loan Contracts: Users can view a list of existing loan contracts.

Add Loan Contract: Users can add a new loan contract by providing the required information.

Update Loan Contract: Users can update an existing loan contract by providing the updated information.

Delete Loan Contract: Users can delete a loan contract.

API Endpoints
GET /loancontract: Retrieve a list of all loan contracts.

POST /loancontract: Add a new loan contract.

PUT /loancontract/int:id: Update an existing loan contract.

DELETE /loancontract/int:id: Delete a loan contract.

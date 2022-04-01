# FoundationProject FebBatch 2022 BigData

A Python CLI (Command Line Interface) application for Business Management and Inventory. This application allows the user to Create, View, Delete, and Analyze Customers, Orders, and Products information stored in a MongoDB database. You can View Customer Details, Product Details, and Orders. You can Create a new Product, Place an Order, Update Product and Customer Details, as well as Deleting Products and Orders. This application has the functionality to Load Customers, Orders and Products data from a JSON file.

### To Use
> Start MongoDB Server

Make sure the MongoDB Server is running before starting the application

In one terminal window:
`brew services start mongodb-community@<version>`

> Start Program

In another terminal window:
`python3 cli.py`

### Notes
- Make sure your JSON files are in the same directory as cli.py
- Make sure pymongo is installed
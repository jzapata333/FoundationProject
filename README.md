# FoundationProject FebBatch 2022 BigData

A Python CLI (Command Line Interface) application for Business Management and Inventory. This application has the functionality to Load Customers, Orders and Products data from a JSON file.

### Technologies Used
 - Python - version 3.x
   - File I/O
   - Collections
 - MongoDB - version 4.4 or higher
 - PyMongo
 - gitSCM (+ Github)

### Features 
 - This application allows the user to Create, View, Delete, and Analyze Customers, Orders, and Products information stored in a MongoDB database.
 - The user can View Customer Details, Product Details, and Orders. 
 - It also provides the functionality to Create a new Product, Place an Order, Update Product and Customer Details, as well as Deleting Products and Orders.

### Getting Started
In your terminal window: `git clone` https://github.com/jzapata333/FoundationProject.git

### To Use
> Start MongoDB Server

Make sure the MongoDB Server is running before starting the application

In one terminal window:
- For Windows: `C:\Program Files\MongoDB\Server\5.0\bin\mongod.exe" --dbpath="f:\<your_mongodb_path>\data\db`
- For Unix: `brew services start mongodb-community@<version>` 

> Start Program

In another terminal window:
`python3 cli.py`

### Notes
- Make sure your JSON files are in the same directory as cli.py
- Make sure pymongo is installed

### License 
> This project uses the following license: [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html)

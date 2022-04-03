from this import d
from pymongo import MongoClient
import json
from bson.objectid import ObjectId
from pprint import pprint
import re
from tkinter import E
from functions import createProduct, deleteOrder, deleteProduct, disconnect, loadData, placeOrder, updateCust_Details, updateProd_Details, viewCust_Details, viewCustomers, viewOrder_Details, viewProd_Details, viewProducts, viewOrders


def option():
    while(True):
        try:
            print(
                "\nWelcome to Rain Forest Systems\nPlease select your option: ")
            print("1. Load Data")
            print("2. View Customers")
            print("3. View Customer Details")
            print("4. View Products")
            print("5. View Product Details")
            print("6. View Orders")
            print("7. View Orders for a Customer")
            print("8. Place an Order")
            print("9. Create New Product")
            print("10. Update Product Details")
            print("11. Update Customer Details")
            print("12. Delete a Product")
            print("13. Delete an Order\n")

            num = int(input("Option # (0 to exit): "))
            if(num > 13 or num < 0):
                print("Please enter an option between 1 and 13.")

            elif(num == 0):
                disconnect()
                break

            elif(num == 1):
                loadData()

            elif(num == 2):
                viewCustomers()

            elif(num == 3):
                viewCust_Details()

            elif(num == 4):
                viewProducts()

            elif(num == 5):
                viewProd_Details()

            elif(num == 6):
                viewOrders()

            elif(num == 7):
                viewOrder_Details()

            elif(num == 8):
                placeOrder()

            elif(num == 9):
                createProduct()

            elif(num == 10):
                updateProd_Details()

            elif(num == 11):
                updateCust_Details()

            elif(num == 12):
                deleteProduct()

            elif(num == 13):
                deleteOrder()

        except:
            print("Please enter a valid option.")
            continue


option()

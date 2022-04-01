from pymongo import MongoClient
import json
from bson.objectid import ObjectId
from pprint import pprint
import re


client = MongoClient('mongodb://127.0.0.1:27017')
db = client.rainforeststore
c_collection = db.customers
o_collection = db.orders
p_collection = db.products


def disconnect():
    print("Thank you for using Rain Forest Systems.\nNow Exiting...")
    client.close()


def loadData():
    print("1. Load Data")
    with open("products.json") as products:
        file_data = json.load(products)
        p_collection.insert_many(file_data)
        print("Products data loaded.")

    with open("customers.json") as customers:
        file_data = json.load(customers)
        c_collection.insert_many(file_data)
        print("Customers data loaded.")

    with open("orders.json") as orders:
        file_data = json.load(orders)
        o_collection.insert_many(file_data)
        print("Orders data loaded.")


def viewCustomers():
    print("2. View Customers\n")
    customers = c_collection.find()
    for c in customers:
        print(str(c['id']) + ".", c['name']
              ['firstname'] + " " + c['name']['lastname'])


def viewCust_Details():
    print("3. View Customer Details\n")
    while(True):
        try:
            id = int(
                input("Please enter Customer ID (0 to exit): "))
            check_ccol = c_collection.find_one({"id": id})
            if(id == 0):
                break
            elif(check_ccol == None):
                print(
                    f"Customer with ID {id} does not exist. Please try again.")
            else:
                customer = c_collection.find_one({"id": id})
                print("Name: ", customer["name"]["firstname"] +
                      " " + customer["name"]["lastname"])
                print("Username: ", customer["username"])
                print("Email: ", customer["email"])
                print("Address: ", customer["address"]["number"], customer["address"]["street"],
                      customer["address"]["city"], ", MA", customer["address"]["zipcode"], "\n")
        except:
            print("Invalid Customer ID. Please try again.")


def viewProducts():
    print("4. View Products\n")
    products = p_collection.find()
    for p in products:
        print("id:", str(p["id"]) + ",", p["title"] +
              ", " + "$" + str(p["price"]))


def viewProd_Details():
    print("5. View Product Details\n")
    while(True):
        try:
            id = int(input("Please enter Product ID (0 to exit): "))
            check_pcol = p_collection.find_one({"id": id})
            if(id == 0):
                break
            elif(check_pcol == None):
                print(
                    f"Order with ID {id} does not exist. Please try again.")
            else:
                product = p_collection.find_one({"id": id})
                print("Product ID: ", product["id"])
                print("Title: ", product["title"])
                print("Price: ", "$" + str(product["price"]))
                print("Category: ", product["category"])
                print("Image: ", product["image"], "\n")
        except:
            print(
                "Product ID not available. Be sure to enter a numeric value for Product ID.")


def viewOrders():
    print("6. View Orders\n")
    pipeline = ([
        {
            "$lookup": {
                "from": "customers",
                "localField": "userId",
                "foreignField": "id",
                "as": "order_details"
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "products.productId",
                "foreignField": "id",
                "as": "product_details"
            }
        },
    ])
    for doc in (o_collection.aggregate(pipeline)):
        # pprint(doc)
        print("Order ID: ", doc["id"])
        print("Date: ", doc["date"])
        print("Customer ID: ", doc["userId"])
        print("Name: ", doc["order_details"][0]["name"]["firstname"] +
              " " + doc["order_details"][0]["name"]["lastname"])
        for p in doc["product_details"]:
            print("Product Title: ", p["title"])
            print("Price: ", "$" +
                  str(p["price"]))
        for q in doc["products"]:
            print("Product Quantity: ", q["quantity"])
        # pprint(doc)
        print("\n")


def viewOrder_Details():
    print("7. View Orders for a Customer\n")
    while(True):
        try:
            userId = int(input("Please enter Customer ID (0 to exit): "))
            check_ccol = c_collection.find_one({"id": userId})
            if(userId == 0):
                break
            elif(check_ccol == None):
                print("Invalid Customer ID or Customer ID does not exist.")
            else:
                # The $lookup stage
                pipeline = ([
                    {
                        "$lookup": {
                            "from": "customers",
                            "localField": "userId",
                            "foreignField": "id",
                            "as": "order_details"
                        }
                    }, {"$match": {"userId": userId}}
                ])
                for doc in (o_collection.aggregate(pipeline)):
                    pass

                orders = o_collection.find({"userId": userId})
                for o in orders:
                    print("Order ID: ", o["id"])
                    print("Customer ID: ", o["userId"])
                    print("Name: ", doc["order_details"][0]["name"]["firstname"] +
                          " " + doc["order_details"][0]["name"]["lastname"])
                    print("date: ", o["date"], "\n")
        except:
            print(
                "Customer ID not available. Be sure to enter a numeric value for Customer ID.")


def placeOrder():
    print("8. Place an Order")
    order = {}
    while(True):
        try:
            userId = int(input("Enter Customer ID (0 to exit): "))
            check_ccol = c_collection.find_one({"id": userId})
            # print(check_ccol)
            if(userId == 0):
                break
            elif(check_ccol == None):
                print(
                    "Invalid Customer ID or Customer ID does not exist.")
            else:
                id = int(input("Enter new Order ID (0 to exit): "))
                check_ocol = o_collection.find_one({"id": id})
                # print(check_ocol)
                if(id == 0):
                    break
                elif(check_ocol != None):
                    print(
                        f"Order with ID {id} already exists. Please try a different Order ID.")
                else:
                    date = str(
                        input("Enter Order date (YYYY-MM-DD): "))
                    time = str(
                        input("Enter Order time (00:00:00): "))
                    date_regex = '\d{4}[-\.\s]\d{2}[-\.\s]\d{2}'
                    date_result = re.match(date_regex, date)
                    time_regex = '\d{2}[:\.\s]\d{2}[:\.\s]\d{2}'
                    time_result = re.match(time_regex, time)
            if(not date_result and not time_result):
                print(
                    "Invalid Order date and/or Order time. Please try again.")
            else:
                date_time = date + "T" + time + ".000Z"
                print("datetime: ", date_time)
                order["products"] = []

            while(True):
                def add_product():
                    productId = int(input("Enter Product ID: "))
                    check_pcol = p_collection.find_one(
                        {"id": productId})
                    if(check_pcol == None):
                        print(
                            f"Product with ID {productId} does not exist. Please try again.")
                    else:
                        quantity = int(
                            input("Enter Product Quantity: "))
                        if(quantity <= 0):
                            print(
                                "Quantity cannot be zero or a negative number.")
                        else:
                            current_product = {
                                "productId": productId,
                                "quantity": quantity
                            }
                            order["id"] = id
                            order["userId"] = userId
                            order["date"] = date_time
                            order["products"].append(
                                current_product)
                            print(order)
                            try:
                                next_step = int(input(
                                    "Would you like to add more Products to this order (0 to exit, 1 to add product)? "))
                                if(next_step == 0):
                                    print("\nCustomer's Order:")
                                    print(order)
                                    o_collection.insert_one(order)
                                    print(
                                        f"\nOrder with ID {id} has been successfully placed.")
                                elif(next_step == 1):
                                    add_product()
                            except:
                                print(
                                    "Invalid option. Please try again.")
                add_product()
                break
        except:
            print("Invalid data. Please try again.")


def createProduct():
    print("9. Create New Product")
    dictionary = {}
    while(True):
        try:
            id = int(input("Enter new Product ID (0 to exit): "))
            check_pcol = p_collection.find_one({"id": id})
            # print(check_pcol)
            if(id == 0):
                break
            elif(check_pcol != None):
                print(
                    f"Product with ID {id} already exists. Please try a different Product ID.")
            else:
                title = str(input("Enter Product Title: "))
                price = float(input("Enter Product Price: "))
                description = str(
                    input("Enter Product Description: "))
                category = str(input("Enter Product Category: "))
                image = str(input("Enter Product Image URL: "))
                dictionary["id"] = id
                dictionary["title"] = title
                dictionary["price"] = price
                dictionary["description"] = description
                dictionary["category"] = category
                dictionary["image"] = image
                print("\nYou entered: ")
                print(dictionary)
                product = p_collection.insert_one(dictionary)
                print("\nProduct has been successfully created.")
        except:
            print("Invalid data. Please try again.")


def updateProd_Details():
    print("10. Update Product Details\n")
    print("1. Title")
    print("2. Price")
    print("3. Description")
    print("4. Category")
    print("5. Image")
    while(True):
        num = int(input("What would you like to update? (0 to exit): "))
        if(num == 0):
            break
        elif(num == 1):
            print("1. Title")
            id = int(input("Enter Product ID: "))
            check_pcol = p_collection.find_one({"id": id})
            if(check_pcol == None):
                print(
                    f"Product with ID {id} does not exist. Please try a different Product ID.")
            else:
                title = str(input("Enter Product Title: "))
                product = p_collection.update_one(
                    {"id": id}, {"$set": {"title": title}})
                print(
                    f"Title for Product with ID {id} has been updated.")
        elif(num == 2):
            print("2. Price")
            id = int(input("Enter Product ID: "))
            check_pcol = p_collection.find_one({"id": id})
            if(check_pcol == None):
                print(
                    f"Product with ID {id} does not exist. Please try a different Product ID.")
            else:
                price = float(input("Enter Product Price: "))
                product = p_collection.update_one(
                    {"id": id}, {"$set": {"price": price}})
                print(
                    f"Price for Product with ID {id} has been updated.")
        elif(num == 3):
            print("3. Description")
            id = int(input("Enter Product ID: "))
            check_pcol = p_collection.find_one({"id": id})
            if(check_pcol == None):
                print(
                    f"Product with ID {id} does not exist. Please try a different Product ID.")
            else:
                description = str(input("Enter Product Description: "))
                product = p_collection.update_one(
                    {"id": id}, {"$set": {"description": description}})
                print(
                    f"Description for Product with ID {id} has been updated.")
        elif(num == 4):
            print("4. Category")
            id = int(input("Enter Product ID: "))
            check_pcol = p_collection.find_one({"id": id})
            if(check_pcol == None):
                print(
                    f"Product with ID {id} does not exist. Please try a different Product ID.")
            else:
                category = str(input("Enter Product Category: "))
                product = p_collection.update_one(
                    {"id": id}, {"$set": {"category": category}})
                print(
                    f"Category for Product with ID {id} has been updated.")
        elif(num == 5):
            print("5. Image")
            id = int(input("Enter Product ID: "))
            check_pcol = p_collection.find_one({"id": id})
            if(check_pcol == None):
                print(
                    f"Product with ID {id} does not exist. Please try a different Product ID.")
            else:
                image = str(input("Enter Product Image URL: "))
                product = p_collection.update_one(
                    {"id": id}, {"$set": {"image": image}})
                print(
                    f"Image URL for Product with ID {id} has been updated.")


def updateCust_Details():
    print("11. Update Customer Details\n")
    print("1. Address")
    print("2. Email")
    print("3. Password")
    print("4. Phone Number")
    print("5. Username")
    while(True):
        num = int(input("What would you like to update? (0 to exit): "))
        if(num == 0):
            break
        elif(num == 1):
            print("1. Address")
            id = int(input("Enter Customer ID: "))
            check_ccol = c_collection.find_one({"id": id})
            if(check_ccol == None):
                print(
                    f"Customer with ID {id} does not exist. Please try a different Customer ID.")
            else:
                number = int(input("Enter Street Number: "))
                street = str(input("Enter Street Address: "))
                city = str(input("Enter City: "))
                zipcode = str(
                    input("Enter  Zipcode in the following format [00000-0000]: "))
                zip_regex = '\d{5}[-\.\s]\d{4}'
                zip_result = re.match(zip_regex, zipcode)
                if(zip_result):
                    customer = c_collection.update_one({"id": id}, {"$set": {
                        "address.number": number, "address.street": street, "address.city": city, "address.zipcode": zipcode}})
                    print(
                        f"Address for Customer with ID {id} has been successfully updated.")
                else:
                    print("Zipcode format is invalid. Please try again.")

        elif(num == 2):
            print("2. Email")
            id = int(input("Enter Customer ID: "))
            check_ccol = c_collection.find_one({"id": id})
            if(check_ccol == None):
                print(
                    f"Customer with ID {id} does not exist. Please try a different Customer ID.")
            else:
                email = str(input("Enter new Customer Email: "))
                customer = c_collection.update_one(
                    {"id": id}, {"$set": {"email": email}})
                print(
                    f"Customer with ID {id} has been successfully updated.")

        elif(num == 3):
            print("3. Password")
            id = int(input("Enter Customer ID: "))
            check_ccol = c_collection.find_one({"id": id})
            if(check_ccol == None):
                print(
                    f"Customer with ID {id} does not exist. Please try a different Customer ID.")
            else:
                passwd = str(input("Enter new Customer Password: "))
                passwd2 = str(input("Re-enter Customer Password: "))
                if(passwd == passwd2):
                    customer = c_collection.update_one(
                        {"id": id}, {"$set": {"password": passwd}})
                    print(
                        f"Password for Customer with ID {id} has been successfully updated.")
                else:
                    print("Passwords do not match. Please try again.")

        elif(num == 4):
            while(True):
                print("4. Phone Number")
                id = int(input("Enter Customer ID: "))
                check_ccol = c_collection.find_one({"id": id})
                if(check_ccol == None):
                    print(
                        f"Customer with ID {id} does not exist. Please try a different Customer ID.")
                else:
                    phone_num = str(input(
                        "Enter new Customer Phone Number in the following format [0-000-000-0000]: "))
                    regex = "\d{1}[-\.\s]\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}"
                    result = re.match(regex, phone_num)
                    if(result):
                        customer = c_collection.update_one(
                            {"id": id}, {"$set": {"phone": phone_num}})
                        print(
                            f"Phone Number for Customer with ID {id} has been successfully updated.")
                        break
                    else:
                        print(
                            "Invalid Phone Number format. Please try again.")

        elif(num == 5):
            print("5. Username")
            id = int(input("Enter Customer ID: "))
            check_ccol = c_collection.find_one({"id": id})
            if(check_ccol == None):
                print(
                    f"Customer with ID {id} does not exist. Please try a different Customer ID.")
            else:
                username = str(input("Enter new Customer Username: "))
                customer = c_collection.update_one(
                    {"id": id}, {"$set": {"username": username}})
                print(
                    f"Username for Customer with ID {id} has been successfully updated.")


def deleteProduct():
    print("12. Delete a Product\n")
    while(True):
        try:
            id = int(input("Enter Product ID (0 to exit): "))
            # print(p_collection.find_one({"id": id}))
            check_pcol = p_collection.find_one({"id": id})
            if(id == 0):
                break
            elif(check_pcol == None):
                print(
                    f"Product with ID {id} does not exist. Please try again.")
            else:
                product = p_collection.delete_one({"id": id})
                print(
                    f"Product with ID {id} has been successfully deleted.")
        except:
            print(
                "Invalid data. Be sure to enter a numeric value for Product ID.")


def deleteOrder():
    print("13. Delete an Order")
    while(True):
        try:
            id = int(input("Enter Order ID (0 to exit): "))
            check_ocol = o_collection.find_one({"id": id})
            if(id == 0):
                break
            elif(check_ocol == None):
                print(
                    f"Order with ID {id} does not exist. Please try again.")
            else:
                order = o_collection.delete_one({"id": id})
                print(
                    f"Order with ID {id} has been successfully deleted.")
        except:
            print(
                "Invalid data. Be sure to enter a numeric value for Order ID.")

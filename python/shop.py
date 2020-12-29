from dataclasses import dataclass, field
from typing import List
import csv
import os

@dataclass
class Product:
    '''Class for keeping information about shop product - product name and product price'''

    name: str
    price: float = 0.0

@dataclass 
class ProductStock:
    '''Class for keeping information about shop Stock - product and product quantity'''
    product: Product
    quantity: int

@dataclass 
class Shop:
    '''Class for keeping information about Shop - Shop cash and Product Stock'''
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    '''Class for keeping information about Customer -Customer name, Budget and shopping list '''
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)

def create_and_stock_shop():
    '''
        Function to read shop data from CSV file, and create Shop 

        CSV Template:
            Shop_cash (float),,
            product_1(str), price_1(float), stock_1(int)
            product_2(str), price_2(float), stock_2(int)
            ...

        Returns:
            s : instance of Shop Class 

    '''
    # Instantiate  an object of Shop Class
    s = Shop() 

    # Open CSV file 
    with open('../stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        # Read first row from csv file and assign to variable cash
        first_row = next(csv_reader)
        s.cash = float(first_row[0])

        # for each row loop will create instances of Product Class and Product Stock Class
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
            #print(ps)
    return s

def clearScreen():  
    '''
        Function to clear console screen
    '''
    os.system('cls')  # For Windows
    os.system('clear')  # For Linux/OS X

def print_product(p):
    '''
        Function to print product to the console
        
        Parameters:
            p : Product : instance of Product Class
    '''

    print(f'PRODUCT NAME: {p.name} - PRODUCT PRICE: {p.price:,.2f}')


def print_shop(s):
    '''
        Function to print shop to the console

        Parameters:
            s : Shop : instance of Shop Class
    '''

    print('Shop has {:,.2f} in cash'.format(s.cash))
    print("--------------------------")

    # loop over shop stock to print each item to the console
    for item in s.stock:
        # call print_product 
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above')
        print("--------------------------")


def read_customer(file_path):
    '''
        Function to read customer data from CSV file and create customer

        CSV template:
            Customer_name (str), Customer_budget (float)
            Product_1 (str), quantity_1 (int)
            Product_2 (str), quantity_2 (int)
            ...

        Parameters:
            file_path : str : Path to the CSV file 

        Returns:
            c : Customer : instance of Customer Class
    '''
    # Open CSV file 
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # first row is customer name and budget
        first_row = next(csv_reader)

        # intantiate Customer Class with parameters name and budget
        c = Customer(first_row[0], float(first_row[1]))

        # Create shoping list
        # for each row in csv file create Product, add Product to Product Stock and Product Stock append to customer shopping list
        for row in csv_reader:
            name = row[0]
            quantity = int(row[1])
            p = Product(name)
            ps = ProductStock(p, quantity)
            c.shopping_list.append(ps)
        return c 

def print_customer(c,s):
    '''
        Function to print Customer Name, Customer Budget and shopping list to the console.
        Gets price for customer product from shop stock.  
        Also adds a summary of total price and updated customer budget

        Parameters:
            c : Customer : instance of Customer class
            s : Shop     : instance of Shop class
    '''

    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget:,.2f}')
    print("--------------------------")

    # initiate variable total price
    total_price = 0

    # iterate over a customer shopping list
    for item in c.shopping_list:

        # for each customer item call getItem function which checks if the product.name from the customer shopping list 
        # exists in the store and if true, returns product from shop product stock
        shop_product = getItem(s,item.product.name).product
      
        if shop_product is None:
            print("Pass")
        else:
            # print shop product
            print_product(shop_product)
            
            print(f'{c.name} ORDERS {item.quantity} OF ABOVE PRODUCT')

            # calculate cost for each item 
            cost = item.quantity * shop_product.price
            print(f'The cost to {c.name} will be €{cost:,.2f}')
            print("--------------------------")

            # calculate total price for all items
            total_price += cost

    print(f"{c.name}'s Provisional total cost: {total_price:,.2f}")
    print(f"{c.name}'s Provisional updated budget: {c.budget - total_price:,.2f}")
    print("--------------------------")


def getItem(shop, name):
    '''
        I introduced this method in order to be able to quickly find a product from the client's list in the store, searching by the product name. 
        Thanks to this, I will have access to the price and number available in the store for the product that the customer is looking for.

        Parameters:
            shop : Shop : instance of Shop class
            name : str  : product name 

        Returns:
            i :  ProductStock : if True instance of ProductStock class, None otherwise
            
    '''

    # iterate over the shop.stock, 
    for i in shop.stock:
        # for each ProductStock compare product.name with searched string 
        if i.product.name == name:
            # if found return ProductStock
            return i
    # if not found return None
    return None


def finish_order(shop, customer):
    '''
        This function is to complete the purchase operation. Checking the availability of products, 
        constantly monitoring the customer's budget and, if the transaction was successful, updating the store, 
        by changing the shop cash and product quantity for purchased products. 

        Parameteres: 
            shop     : Shop     : instance of Shop class
            customer : Customer : Instance of Customer class
    '''

    # iterate over the customer shopping list 
    for item in customer.shopping_list:

        # check if customer's product exists in shop stock 
        shop_item = getItem(shop, item.product.name)
        
        # if product not found in shop stock 
        if shop_item == None:
            print(f"I am very sorry, but unfortunately we do not sell {item.product.name}")
        else:
            # calculates order value 
            order_value = item.quantity * shop_item.product.price

            # checks if there is enough product in the store
            if item.quantity <= shop_item.quantity: 
                
                # checks if the client has a sufficient budget to complete the transaction
                if customer.budget > order_value:

                    # Updates shop and customer budget
                    shop_item.quantity -= item.quantity
                    shop.cash += order_value
                    customer.budget -= order_value

                    print(f"You bought {item.quantity} of {item.product.name}")


                else:
                    print(f"I'm very sorry but you don't have enough money, you are short of {order_value - customer.budget:,.2f} euro to buy {item.quantity} {item.product.name}")
            else:
                print(f"I'm sorry but unfortunately we don't have enough in stock to cover your order for {item.quantity} {item.product.name}")
        

    print("*******************\n")
    

def liveCustomer(shop):
    '''
        This function is used to create a client for Live Mode Shop, where client parameters 
        are entered from the console by user. User enters the name, budget and then a shopping list is created using while loop, 
        by giving the product name and quantity. The list is created until user breaks the loop by answering "n" 
        to the question "Would You like to buy another product?"

        Parameters:
            shop : Shop : instance of Shop class

        Returns:
            live_customer : Customer : instance of Customer class
    '''

    print("\nHere is my stock list")
    print("--------------------------")

    # Loop to print out to the console list of products and prices available in the shop 
    for i in shop.stock:
        print_product(i.product)
        print("--------------------------")

    # gets data from user
    cust_name = input("\nPLEASE ENTER YOUR NAME: ") 
    cust_budget = float(input("\nPLEASE ENTER YOUR BUDGET: ")) 

    # Create an instance of Customer class 
    live_customer = Customer(cust_name,cust_budget)

    print("\nWhat Would you likte to buy?\n")
    
    # creating a new variable and assigning the value 
    choice = -1
    
    # loop to create a shopping list, 
    # loop will breaks when choice = "n"
    while choice != "n":
        customer_item = input("ENTER PRODUCT NAME: ")
        
        customer_quantity = int(input("\nENTER PRODUCT QUANTITY: "))
        
        p = Product(customer_item)
        ps = ProductStock(p,customer_quantity)
        live_customer.shopping_list.append(ps)

        choice = input("\nWOULD YOU LIKE TO BUY ANOTHER PRODUCT? y/n: ")
    
    return live_customer




def testMenu(shop):
    '''
        Test Mode is used to test the store in situations when some of the purchase conditions cannot be met. 
        The menu test consists of 4 options: 
            1. the customer does not have a sufficient budget to make a purchase, 
            2. the customer wants to buy a product that is not in the store, 
            3. the store does not have enough of a given product to fulfill the order. 
            0. returns to the main menu.
        A different CSV file is loaded for each of the three above situations.  

        Parameters: 
            shop : Shop : instance of Shop class
    '''

    print("##################################")
    print("#                                #")
    print("#       WELCOME TO MY SHOP       #")
    print("#          (TEST MODE)           #")
    print("##################################")
    print("1. Test Low Budget")
    print("2. Test Not in Stock")
    print("3. Test Not enough Stock")
    print("0. Exit")

    # creates variable choice
    choice = -1

    # while loop breaks when 0 is pressed
    while choice !=0:
        choice = int(input("Please choose an option: "))
        
        if choice == 1:
            print("\n**** Load Test Low Budget from CSV file ****\n")
            # create customer from CSV file 
            customer = read_customer("../test_low_budget.csv") 
            print_customer(customer,shop)
            finish_order(shop,customer)
        
        elif choice == 2:
            print("**** Load Test Not in Stock from CSV file ****\n")
            
            # create customer from CSV file 
            customer = read_customer("../test_not_in_stock.csv")
            print_customer(customer,shop)
            finish_order(shop,customer)

        elif choice == 3:
            print("**** Load Test Not enough Stock ****\n")
            
            # create customer from CSV file 
            customer = read_customer("../test_not_enough_stock.csv")
            print_customer(customer,shop)
            finish_order(shop,customer)
       
        elif choice == 0:

            show_options()


    


def show_options():
    '''
        Brings up the menu on the console screen.
        There are 6 options in the menu:
        1. Displays information about the store, the amount of money held, a list of products, their prices and quantity,
        2. Loads and processes the order from a CSV file where all purchase conditions are met.
        3. goes to Test Mode, displays the sub-menu, where we can load csv files where the purchase conditions have not been met.
        4. option in which we go to the live version of the store. in this option, we create a customer by providing his name and budget, 
            then create a shopping list and process the order.
        9. Clears the console screen and returns to the main menu,
        0. closes the shop
    '''

    clearScreen()
    print("##################################")
    print("#                                #")
    print("#       WELCOME TO MY SHOP       #")
    print("#                                #")
    print("##################################")

    print("1. Print Shop Stock")
    print("2. Get order from Shopping List")
    print("3. Test Shop")
    print("4. Live Mode")
    print("9. Return to Menu")
    print("0. Exit")


def display_menu(shop):
    '''
        Adds functionality to the main menu. We are asked to choose one of the 6 options. 
        The loop breaks when option 0 is selected. The store closes

        Parameters:
            shop : Shop : instance of Shop class
    '''

    # displays main menu
    show_options()
    choice = -1

    # while loop breaks when 0 is pressed 
    while choice != 0:
        choice = int(input("Please choose an option (press 9 to show menu option, 0 to exit): "))
        print("\n")

        if choice == 1:
            
            # calls method to print shop
            print_shop(shop)
            print("\n")
        
        elif choice == 2:
            print("**** Get order from ORDER.CSV shopping list ****\n")
            # creates customer from csv file 
            customer = read_customer("../order.csv")

            print("\n---===<< YOUR ORDER CONFIRMAION >>===---\n")

            # prints customer 
            print_customer(customer,shop)

            # finishes customer order 
            finish_order(shop,customer)


        elif choice == 3:

            # clear console screen and enters a test menu
            clearScreen()
            testMenu(shop)

        elif choice == 4:
            print("Hello!!, Welcome To my Live Shop.")
            print("Please Take a look around")

            # creates live customer 
            live_customer = liveCustomer(shop)

            print("\n---===<< YOUR ORDER CONFIRMAION >>===---\n")

            # prints live mode customer  
            print_customer(live_customer,shop)

            # finishes live customer order
            finish_order(shop,live_customer )

        elif choice == 9:

            # displays main menu
            show_options()

    print("\nThank You for shopping with Us.")


# Program starts here:
# creates shop and adds stock from csv file
s = create_and_stock_shop()

# displays main menu. 
display_menu(s)




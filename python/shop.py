from dataclasses import dataclass, field
from typing import List
import csv
import os

@dataclass
class Product:
    name: str
    price: float = 0.0

@dataclass 
class ProductStock:
    product: Product
    quantity: int

@dataclass 
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)

def create_and_stock_shop():
    s = Shop()
    with open('../stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
            #print(ps)
    return s

def clearScreen():  

    os.system('cls')  # For Windows
    os.system('clear')  # For Linux/OS X
    

        

def print_product(p):
    print(f'PRODUCT NAME: {p.name} - PRODUCT PRICE: {p.price:,.2f}')


def print_shop(s):
    print('Shop has {:,.2f} in cash'.format(s.cash))
    print("--------------------------")
    for item in s.stock:
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above')
        print("--------------------------")




###############################
def read_customer(file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        c = Customer(first_row[0], float(first_row[1]))
        for row in csv_reader:
            name = row[0]
            quantity = int(row[1])
            p = Product(name)
            ps = ProductStock(p, quantity)
            c.shopping_list.append(ps)
        return c 

def print_customer(c,s):
    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget:,.2f}')
    print("--------------------------")
    total_price = 0
    for item in c.shopping_list:
        
        shop_product = getProduct(s,item.product.name)
      
        if shop_product is None:
            print("Pass")
        else:
            print_product(shop_product)
            
            print(f'{c.name} ORDERS {item.quantity} OF ABOVE PRODUCT')
            cost = item.quantity * shop_product.price
            print(f'The cost to {c.name} will be €{cost:,.2f}')
            print("--------------------------")
            total_price += cost

    print(f"{c.name}'s Provisional total cost: {total_price:,.2f}")
    print(f"{c.name}'s Provisional updated budget: {c.budget - total_price:,.2f}")
    print("--------------------------")

def getProduct(shop, name):

    for i in shop.stock:
        if i.product.name == name:
            p = i.product
            return p
        
    return None

def getQuantity(shop, name):

    for i in shop.stock:
        if i.product.name == name:
            
            return i
        
    return None


def finish_order(shop, customer):

    for item in customer.shopping_list:

        shop_product = getProduct(shop, item.product.name)
        shop_stock = getQuantity(shop, item.product.name)
        
        
        if shop_product == None:
            print(f"I am very sorry, but unfortunately we do not sell {item.product.name}")
        else:
            order_value = item.quantity * shop_product.price
            if item.quantity <= shop_stock.quantity:

                if customer.budget > order_value:

                    shop_stock.quantity -= item.quantity
                    shop.cash += order_value
                    customer.budget -= order_value

                    print(f"You bought {item.quantity} of {item.product.name}")


                else:
                    print(f"I'm very sorry but you don't have enough money, you are short of {order_value - customer.budget:,.2f} euro to buy {item.quantity} {item.product.name}")
            else:
                print(f"I'm sorry but unfortunately we don't have enough in stock to cover your order for {item.quantity} {item.product.name}")
        

    print("*******************")
    print("")

def liveCustomer(shop):
    print("")
    cust_name = input("PLEASE ENTER YOUR NAME: ") 
    print("")
    cust_budget = float(input("PLEASE ENTER YOUR BUDGET: ")) 
    print("") 

    live_customer = Customer(cust_name,cust_budget)

    print("Here is my stock list")
    print("--------------------------")

    for i in shop.stock:
        print_product(i.product)
        print("--------------------------")

    print("What Would you likte to buy?")
    print("")
    print("")


    choice = -1
    
    while choice != "n":
        customer_item = input("ENTER PRODUCT NAME: ")
        print("")
        customer_quantity = int(input("ENTER PRODUCT QUANTITY: "))
        print("")

        p = Product(customer_item)
        ps = ProductStock(p,customer_quantity)
        live_customer.shopping_list.append(ps)

        choice = input("WOULD YOU LIKE TO BUY ANOTHER PRODUCT? y/n: ")
    
    return live_customer




def testMenu(shop):

    print("##################################")
    print("#                                #")
    print("#       WELCOME TO MY SHOP       #")
    print("#          (TEST MODE)           #")
    print("##################################")
    print("1. Test Low Budget")
    print("2. Test Not in Stock")
    print("3. Test Not enough Stock")
    print("0. Exit")

    choice = -1


    while choice !=0:
        choice = int(input("Please choose an option: "))
        print("")
        if choice == 1:
            print("**** Load Test Low Budget from CSV file ****")
            print("")
            customer = read_customer("../test_low_budget.csv")
            finish_order(shop,customer)
        
        elif choice == 2:
            print("**** Load Test Not in Stock from CSV file ****")
            print("")
            customer = read_customer("../test_not_in_stock.csv")
            finish_order(shop,customer)

        elif choice == 3:
            print("**** Load Test Not enough Stock ****")
            print("")
            customer = read_customer("../test_not_enough_stock.csv")
            finish_order(shop,customer)
       
        elif choice == 0:

            show_options()


    


def show_options():

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

    show_options()
    choice = -1
    while choice != 0:
        choice = int(input("Please choose an option (press 9 to show menu option, 0 to exit): "))
        print("\n")

        if choice == 1:
            
            print_shop(shop)
            print("\n")
        
        elif choice == 2:
            print("**** Get order from ORDER.CSV shopping list ****\n")
            customer = read_customer("../order.csv")
            print("")
            print("---===<< YOUR ORDER CONFIRMAION >>===---\n")
            print("")

            print_customer(customer,shop)

            finish_order(shop,customer)
            #print(customer.shopping_list)

        elif choice == 3:

            clearScreen()
            testMenu(shop)

        elif choice == 4:
            print("Hello!!, Welcome To my Live Shop.")
            print("Please Take a look around")

            live_customer = liveCustomer(shop)
            print("")
            print("---===<< YOUR ORDER CONFIRMAION >>===---")
            print("")
            print_customer(live_customer,shop)
            finish_order(shop,live_customer )

        elif choice == 9:
            show_options()







#---------- MAIN -----------# 

s = create_and_stock_shop()
display_menu(s)

# c = read_customer("../customer.csv")
# print_customer(c)




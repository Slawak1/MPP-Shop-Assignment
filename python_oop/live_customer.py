from product_stock import ProductStock
from product import Product
from customer import Customer

class LiveCustomer(Customer):
    def __init__(self):
        
        self.create_customer()

    def create_customer(self):

        print("")
        cust_name = input("PLEASE ENTER YOUR NAME: ") 
        print("")
        cust_budget = float(input("PLEASE ENTER YOUR BUDGET: ")) 
        print("") 

        return cust_name, cust_budget

    def create_shopping_list(self):
        shopping_list = []
        choice = -1
        
        while choice != "n":
            customer_item = input("ENTER PRODUCT NAME: ")
            print("")
            customer_quantity = int(input("ENTER PRODUCT QUANTITY: "))
            print("")

            p = Product(customer_item)
            ps = ProductStock(p,customer_quantity)
            shopping_list.append(ps)

            choice = input("WOULD YOU LIKE TO BUY ANOTHER PRODUCT? y/n: ")
        
        return shopping_list

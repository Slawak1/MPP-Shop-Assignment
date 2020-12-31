from customer import Customer
from product import Product
from product_stock import ProductStock

class LiveCustomer(Customer):
    def __init__(self):
        super().__init__(path=None)


    def create_live_customer(self):
        '''
            Creates a client using user input from the console, the user is prompted for name and budget
        '''

        # gets from user 
        self.name = input("\nPLEASE ENTER YOUR NAME: ") 
        self.budget = float(input("\nPLEASE ENTER YOUR BUDGET: ")) 

    def create_shopping_list(self):
        '''
            Creates a shopping list for live mode. The user is asked to enter the name of the product 
            and the quantity he wants to buy. Thanks to the use of the loop, it is possible to add many products. 
            The loop ends when the question "WOULD YOU LIKE TO BUY ANOTHER PRODUCT?" the user presses the "n" key
        '''

        choice = -1

        # While loop breaks when choice == "n"
        while choice != "n":

            customer_item = input("ENTER PRODUCT NAME: ")
            customer_quantity = int(input("\nENTER PRODUCT QUANTITY: "))
            
            # create instance of a Product class 
            p = Product(customer_item)

            # create instance of a ProductStock class
            ps = ProductStock(p,customer_quantity)
            self.shopping_list.append(ps)

            choice = input("\nWOULD YOU LIKE TO BUY ANOTHER PRODUCT? y/n: ")

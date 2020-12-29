import csv
from product import Product
from product_stock import ProductStock



class Customer:
    '''
        Class to create and store information about customer
    '''

    def __init__(self, path = None):
        '''
            Parameters:
                path : str : Path to the CSV file, Default = None 
        '''

        # shopping list variable 
        self.shopping_list = []
        
        # if path to the CSV file is provided by the function caller 
        # then customer is created from that CSV 
        # When path is not provided live customer can be created 
        if path:
            self.read_csv(path)

    def read_csv(self, path):    
        '''
            Loads the CSV file and creates the client
            
            Parameters:
                path : str : Path to the CSV file
        '''
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])
            for row in csv_reader:
                name = row[0]
                quantity = float(row[1])
                p = Product(name)
                ps = ProductStock(p, quantity)
                self.shopping_list.append(ps) 

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
        # Whiel loop breaks when choice == "n"
        while choice != "n":

            customer_item = input("ENTER PRODUCT NAME: ")
            customer_quantity = int(input("\nENTER PRODUCT QUANTITY: "))
            
            p = Product(customer_item)
            ps = ProductStock(p,customer_quantity)
            self.shopping_list.append(ps)

            choice = input("\nWOULD YOU LIKE TO BUY ANOTHER PRODUCT? y/n: ")
                    
    def calculate_costs(self, price_list):
        '''
            Compares the customer's shopping list with the store's stock list, 
            if the product names match the price on the customer's list, 
            the store price is assigned

            Parameters:
                price_list : list : price list from store 

        '''
        for shop_item in price_list:
            for list_item in self.shopping_list:
                if (list_item.name() == shop_item.name()):
                    list_item.product.price = shop_item.unit_price()
    
    def order_cost(self):
        ''' 
        '''
        cost = 0

        for list_item in self.shopping_list:         
            cost += list_item.cost()
        
        return cost
    
    def __repr__(self):
        
        str = f"CUSTOMER NAME:{self.name}"
        str += "\n"
        str += f"CUSTOMER BUDGET:{self.budget:,.2f} \n"
        #str += "\n"
        str += "--------------------------"

        for item in self.shopping_list:
            
            cost = item.cost()
            str += f"\n{item}"
            str += "\n"
            if (cost == 0):
                str += f"{self.name} doesn't know how much that costs :(\n"
                str += "--------------------------"
            else:
                str += f"The cost to Gerars will be €{cost:,.2f} \n"
                str += "--------------------------"

        str += f"\n{self.name}'s Provisional total cost: {self.order_cost():,.2f} "        
        str += f"\n{self.name}'s Provisional updated budget: {self.budget - self.order_cost():,.2f} "  
        str += "\n--------------------------"      
        
        return str 
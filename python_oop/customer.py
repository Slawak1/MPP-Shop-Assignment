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
        # open csv file 
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            # read first row from csv as a list
            first_row = next(csv_reader)

            # assing name and budget for customer
            self.name = first_row[0]
            self.budget = float(first_row[1])

            # create shopping list by reading data from csv and assign values to self.shopping_list
            for row in csv_reader:
                name = row[0]
                quantity = float(row[1])

                # create instance of a Product class 
                p = Product(name)

                # create instance of a ProductStock class
                ps = ProductStock(p, quantity)
                self.shopping_list.append(ps) 

    
                    
    def calculate_costs(self, price_list):
        '''
            Compares the customer's shopping list with the store's stock list, 
            if the product names match the price on the customer's list, 
            the store price is assigned

            Parameters:
                price_list : list : price list from store 

        '''
        # iterate over shop price list 
        for shop_item in price_list:
            # iterate over customer shopping list 
            for list_item in self.shopping_list:
                # if names match get product price from price list and assign to product from shopping list. 
                if (list_item.name() == shop_item.name()):
                    list_item.product.price = shop_item.unit_price()
    
    def order_cost(self):
        ''' 
            Calculates the total cost of the order from the customer list

            Returns:
                cost : float : total cost of the order
        '''
        # initialize variable 
        cost = 0

        # iterate over the shopping list, calculate cost for each item and add value to cost vairable 
        for list_item in self.shopping_list:         
            cost += list_item.cost()
        
        return cost
    
    def __repr__(self):
        '''
            Special Method for string representation for customer object. 
            This is how the customer object will look when we call print() function.

            Returns:
                str
        '''
        str = f"CUSTOMER NAME:{self.name}"
        str += "\n"
        str += f"CUSTOMER BUDGET:{self.budget:,.2f} \n"
        str += "--------------------------"

        # iterate over shopping list, print cost for each item from list 
        # print provisional cost and updated budget. 
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
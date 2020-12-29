import csv
from product import Product
from product_stock import ProductStock

class Shop:
    '''
        Class to store information about Shop
    '''
    def __init__(self, path):
        '''
        Paramaters:
            path : str : path to the CSV file
        '''

        # create self.stock list to holds ProductStock 
        self.stock = []

        # open csv file 
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            # read first row from csv as a list
            first_row = next(csv_reader)

            # assing cash value from csv file to self.cash variable       
            self.cash = float(first_row[0])

            # create shop stock by reading data from csv and assign values to self.stock list
            for row in csv_reader:

                # create instance of a Product class 
                p = Product(row[0], float(row[1]))

                # create instance of a ProductStock class
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)
        

    def getItem(self,name):
        '''
            Method to find the product in shop stock and return ShopStock object if the product is found. 
            In case the product is not in the store, the value None is returned.

            Parameters:
                name : str : searched product name

            Returns:
                n : ProductStock : instace pf ProductStock class
        '''
        
        # iterate over shop stock
        for n in self.stock:
            # if product name match to searched string then ProductStock is returned
            # else returned None
            if n.name() == name:
                return n
        return None


    def finish_order(self, shopping_list, budget):
        '''
            This method is to complete the purchase operation. Checking the availability of products, 
            constantly monitoring the customer's budget and, if the transaction was successful, updating the store, 
            by changing the shop cash and product quantity for purchased products. 

            Parameteres: 
                shopping_list     : list     : customer's shopping list 
                budget            : float    : Customer's budget
        '''
        
        # iterate over customer shopping list 
        for item in shopping_list:
            
            # check if customer's product exists in shop stock 
            shop_item = self.getItem(item.name())
           
            # if product not in shop stock           
            if shop_item == None:
                print(f"I am very sorry, but unfortunately we do not sell {item.name()}")
            else:
                # calculates order value 
                order_value = item.quantity * shop_item.unit_price()

                # checks if there is enough product in the store
                if item.quantity <= shop_item.quantity:

                    # checks if the client has a sufficient budget to complete the transaction
                    if budget > order_value:

                        # Updates shop and customer budget
                        shop_item.quantity -= item.quantity
                        self.cash += order_value
                        budget -= order_value

                        print(f"You bought {item.quantity} of {item.name()}")


                    else:
                        print(f"I'm very sorry but you don't have enough money, you are short of {order_value - budget:,.2f} euro to buy {item.quantity} {item.name()}")
                else:
                    print(f"I'm sorry but unfortunately we don't have enough in stock to cover your order for {item.quantity} {item.name()}")
            

        print("*******************")
        print("")

    
    def __repr__(self):
        '''
            Special Method for string representation for Shop object. 
            This is how the Shop object will look when we call print() function.

            Returns:
                str
        '''
        str = ""
        str += f'Shop has {self.cash:,.2f} in cash'
        str += "\n"
        str += "--------------------------"
        str += "\n"
        for item in self.stock:
            str += f"{item}\n"
        return str

from shop import Shop
from customer import Customer
import os


class RunShop:
    '''
        Class to create Main Menu
    '''
    def __init__(self):

        # create instance of Shop class
        shop = Shop("../stock.csv")

        # call method MainMenu with Shop object as a parameter
        self.MainMenu(shop)
        

    def clearScreen(self):  
        '''
            Method to clear console screen
        '''

        os.system('cls')  # For Windows
        os.system('clear')  # For Linux/OS X

    
    def testMenu(self,shop):
        '''
            Test Mode is used to test the store in situations when some of the purchase conditions cannot be met. 
            The menu test consists of 4 options: 
                1. the customer does not have a sufficient budget to make a purchase, 
                2. the customer wants to buy a product that is not in the store, 
                3. the store does not have enough of a given product to fulfill the order. 
                0. returns to the main menu.
            A different CSV file is loaded for each of the three situations.  

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

        # # while loop breaks when 0 is pressed
        while choice !=0:
            choice = int(input("Please choose an option: "))
            
            if choice == 1:
                print("\n**** Load Test Low Budget from CSV file ****\n")
                
                # create customer from CSV file
                customer = Customer("../test_low_budget.csv")

                customer.calculate_costs(shop.stock)
                print(customer)

                # call method finish_order
                shop.finish_order(customer.shopping_list, customer.budget)
            
            elif choice == 2:
                print("**** Load Test Not in Stock from CSV file ****\n")
                # create customer from CSV file 
                customer = Customer("../test_not_in_stock.csv")
                customer.calculate_costs(shop.stock)
                print(customer)
                # call method finish_order
                shop.finish_order(customer.shopping_list, customer.budget)

            elif choice == 3:
                print("**** Load Test Not enough Stock ****\n")
                # create customer from CSV file 
                customer = Customer("../test_not_enough_stock.csv")
                customer.calculate_costs(shop.stock)
                print(customer)
                # call method finish_order
                shop.finish_order(customer.shopping_list, customer.budget)
        
            elif choice == 0:

                self.show_options()
    
    def show_options(self):
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

        self.clearScreen()
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

    def MainMenu(self, shop):
        '''
            Adds functionality to the main menu. We are asked to choose one of the 6 options. 
            The loop breaks when option 0 is selected. The store closes

            Parameters:
                shop : Shop : instance of Shop class
        '''
        # displays main menu
        self.show_options()

        choice = -1
        
        # while loop breaks when 0 is pressed
        while choice != 0:
            choice = int(input("Please choose an option (press 9 to show menu option, 0 to exit): "))
            print("\n")

            if choice == 1:
                # calls method to print shop
                print(shop)
                print("\n")
            
            elif choice == 2:
                print("**** Get order from ORDER.CSV shopping list ****\n")
                
                # creates customer from csv file 
                customer = Customer("../order.csv")
                print("")
                print("---===<< YOUR ORDER CONFIRMAION >>===---\n")
                print("")
                customer.calculate_costs(shop.stock)
                print(customer)
                # call method finish_order
                shop.finish_order(customer.shopping_list, customer.budget)


            elif choice == 3:
                # clear console screen and display test Menu
                self.clearScreen()
                self.testMenu(shop)

            elif choice == 4:
                print("Hello!!, Welcome To my Live Shop.")
                print("Please Take a look around\n")

                print("Here is my stock list")
                print("--------------------------")

                # display shop stock list
                for item in shop.stock:
                    print(f"{item}")
                    print(f"--------------------------")

                # create an instance of a Customer class
                live_customer = Customer()
                
                # call create_live_customer method where name and budget are entered
                live_customer.create_live_customer()

                print("\nWhat Would you likte to buy?\n")

                # call create_shopping_list method where shopping list is created 
                live_customer.create_shopping_list()

                live_customer.calculate_costs(shop.stock)
                print("")
                print("---===<< YOUR ORDER CONFIRMAION >>===---")
                print("")
                print(live_customer)

                # call method finish_order
                shop.finish_order(live_customer.shopping_list, live_customer.budget)

            elif choice == 9:

                # display Main Menu
                self.show_options()

        print("\nThank You for shopping with Us.")


# Program starts here
run = RunShop()
run



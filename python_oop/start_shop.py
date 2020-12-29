
from shop import Shop
from customer import Customer
#from live_customer import LiveCustomer
import os


class RunShop:
    def __init__(self):

        shop = Shop("../stock.csv")
        self.MainMenu(shop)
        

    def clearScreen(self):  

        os.system('cls')  # For Windows
        os.system('clear')  # For Linux/OS X

    
    def testMenu(self,shop):

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
                customer = Customer("../test_low_budget.csv")
                customer.calculate_costs(shop.stock)
                print(customer)
                shop.finish_order(customer.shopping_list, customer.budget)
            
            elif choice == 2:
                print("**** Load Test Not in Stock from CSV file ****")
                print("")
                customer = Customer("../test_not_in_stock.csv")
                customer.calculate_costs(shop.stock)
                print(customer)
                shop.finish_order(customer.shopping_list, customer.budget)

            elif choice == 3:
                print("**** Load Test Not enough Stock ****")
                print("")
                customer = Customer("../test_not_enough_stock.csv")
                customer.calculate_costs(shop.stock)
                print(customer)
                shop.finish_order(customer.shopping_list, customer.budget)
        
            elif choice == 0:

                self.show_options()
    
    def show_options(self):

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

        self.show_options()

        choice = -1
        while choice != 0:
            choice = int(input("Please choose an option (press 9 to show menu option, 0 to exit): "))
            print("\n")

            if choice == 1:
                
                print(shop)
                print("\n")
            
            elif choice == 2:
                print("**** Get order from ORDER.CSV shopping list ****\n")
                customer = Customer("../order.csv")
                print("")
                print("---===<< YOUR ORDER CONFIRMAION >>===---\n")
                print("")
                customer.calculate_costs(shop.stock)
                print(customer)
                shop.finish_order(customer.shopping_list, customer.budget)


            elif choice == 3:

                self.clearScreen()
                self.testMenu(shop)

            elif choice == 4:
                print("Hello!!, Welcome To my Live Shop.")
                print("Please Take a look around\n")

                print("Here is my stock list")
                print("--------------------------")

                for item in shop.stock:
                    print(f"{item}")
                    print(f"--------------------------")

                live_customer = Customer()
                

                live_customer.create_live_customer()

                print("\nWhat Would you likte to buy?\n")

                live_customer.create_shopping_list()
                live_customer.calculate_costs(shop.stock)
                print("")
                print("---===<< YOUR ORDER CONFIRMAION >>===---")
                print("")
                print(live_customer)

                shop.finish_order(live_customer.shopping_list, live_customer.budget)

            elif choice == 9:
                self.show_options()

        print("\nThank You for shopping with Us.")



run = RunShop()
run



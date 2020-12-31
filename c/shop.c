/*
Student: Slawomir Sowa
Date: 10/12/2020
Student ID: G00376519
MultiParadigmProgramming Assignmetn
Title: Shop
Language: C 

*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>


struct Product {
	// datatype struct contain product name and price
	char* name;
	double price;
};

struct ProductStock {
	// datatype struct contain stock for shop - nested struct Product and quantity
	struct Product product;
	int quantity;
};

struct Shop {
	// datatype struct contain shop stock and cash
	double cash;
	struct ProductStock stock[20];
	int index; // current index of stock list 
};

struct Customer {
	// datatype struct contains Customer details name, budget and shopping list
	char* name;
	double budget;
	struct ProductStock shoppingList[10];
	int index; // current index of shop list
};



void printProduct(struct Product p)
/* 
	Function to print information about product
	Parameters:
		p : struct Product : Holds information about product name and price
*/
{
	printf("PRODUCT NAME: %s - PRODUCT PRICE: %.2f\n", p.name, p.price);

}

void printCustomer(struct Customer c)
/*
	Function to print customer details and shopping list 
	Parameters:
		c : struct Customer : Holds information about customer name, budget and shopping list 
*/
	
{	
	double total_price = 0.0;

	// print customer name and budget
	printf("CUSTOMER NAME: %s \nCUSTOMER BUDGET: %.2f\n", c.name, c.budget);
	printf("--------------------------\n");

	// iterates over customer shopping list 
	for(int i = 0; i < c.index; i++) // 
	{	
		// method call printProduct
		printProduct(c.shoppingList[i].product); // prints product from shopping list 
		printf("%s ORDERS %d OF ABOVE PRODUCT\n", c.name, c.shoppingList[i].quantity); // prints information about customer name and quantity
		double cost = c.shoppingList[i].quantity * c.shoppingList[i].product.price; // calculate cost
		printf("The cost to %s will be e%.2f\n", c.name, cost); // print costs
		printf("--------------------------\n");
		total_price += cost; // increment total price variable
	}

	printf("%s's Provisional total cost: %.2f\n", c.name, total_price);
	printf("%s's Provisional updated budget: %.2f\n", c.name, (c.budget - total_price));
	printf("--------------------------\n");
}

struct Shop createAndStockShop()
/*
	Function to create Shop, read stock from CSV file 

	Returns:
		shop : struct Shop
*/
{
    FILE * fp; 
    char * line = NULL;
    size_t len = 0;
    size_t read;

    fp = fopen("..\\stock.csv", "r");  // opens csv file 

	// if fp is null exit program
    if (fp == NULL)
        exit(EXIT_FAILURE);
	
	read = getline(&line, &len, fp);

	// convert string to float
	float cash = atof(line);
	
	// create struct Shop and assign cash variable
	struct Shop shop = { cash };
	
    while ((read = getline(&line, &len, fp)) != -1) {
        
		// method strtok breaks string str into a tokens using delimiter "," as string
		char *n = strtok(line, ",");
		char *p = strtok(NULL, ",");
		char *q = strtok(NULL, ",");

		// convert variables from string to integer and double
		int quantity = atoi(q);
		double price = atof(p);

		// method malloc allocates the requested memory and returns a pointer to it
		// in below case is memory alocated for size of 50 characters 
		char *name = malloc(sizeof(char) * 50);

		// method to copythe string pointed by source n to the destination name
		strcpy(name, n);

		// create product and stockItem
		struct Product product = { name, price };
		struct ProductStock stockItem = { product, quantity };

		// increase shop stock index
		shop.stock[shop.index++] = stockItem;
    }
	return shop;
}
struct Product getProduct(struct Shop s, char* pname)
/*
	Function to check the shop for a product and return it
	Parameters:
		s : struct Shop : datatype struct contain shop stock and cash
		pname: char : searched item in shop stock
	
	Return:
		p : struct Product : datatype struct contain product name and price

*/
{
    struct Product p;

	// loop over a shop index and compare related to index product name to searched phrase
    for (int i = 0; i < s.index; i++){
		// if strcmp returns 0 product was found and product p is returned
    	if(strcmp(s.stock[i].product.name,pname)==0){
    		p = s.stock[i].product;
    	}
    }
	return p;
};


void clearScreen()
/*
	
	Function to clear screen that will work for linux, windows and Mac OS. 
	https://stackoverflow.com/questions/2347770/how-do-you-clear-the-console-screen-in-c
*/
{
  system("cls||clear");
}

void printShop(struct Shop s)
/*
	Function to print in console shop cash, stock product and stock quantity

	Parameters:
		s : struct Shop : datatype struct contain shop stock and cash
*/
{
	// print shop cash
	printf("Shop has %.2f in cash\n", s.cash);
	printf("--------------------------\n");
	// for loop that print out shop product and product quantity
	for (int i = 0; i < s.index; i++)
	{
		printProduct(s.stock[i].product);
		printf("The shop has %d of the above\n", s.stock[i].quantity);
		printf("--------------------------\n");
	}
}

struct Customer CustOrder(struct Shop s, char* order_csv_file)
/*
	Function to read customer order from csv file. 
	The csv file contains the customer's name, budget and a list of products that the customer wants to buy in the store.
	The task of this function is to read the data line by line and pass it to datatype struct Customer 

	Parameters:
		s : struct Shop : datatype struct contain shop stock and cash
		order_csv_file : char : name of the CSV file

	Returns:
		customer : struct Customer : datatype struct contains Customer details name, budget and shopping list
*/

{	
	FILE * fp;
	char * line = NULL;
	size_t len = 0;
	size_t read;

	// opens csv file 
	fp = fopen(order_csv_file,"r");

	getline(&line, &len, fp);

	// method strtok breaks string str into a tokens using delimiter "," as string
	char *cName = strtok(line,",");
	char *cBudget = strtok(NULL,",");

	// method malloc allocates the requested memory and returns a pointer to it
	// in the following case, memory is alocated for 50 characters
	char *custName = malloc(sizeof(char)*50);

	// method to copythe string pointed by source n to the destination name
	strcpy(custName,cName);

	// convert variables from string to double
	double custBudget = atof(cBudget);

	// create struct Customer and assign customer name and customer budget
	struct Customer customer = {custName, custBudget};

	while ((read = getline(&line, &len, fp)) != -1)
	{
		
		char *p = strtok(line, ",");
		char *qt = strtok(NULL,",");
		
		int prodQuant = atoi(qt);
		char *prodName = malloc(sizeof(char)*50);
		strcpy(prodName,p);

		struct Product product = {prodName, getProduct(s,prodName).price};
		struct ProductStock listItem = {product, prodQuant};

		customer.shoppingList[customer.index++] = listItem;	
	}
	return customer;
};


char* getProductName(struct Shop* s, char *pname)
/*
	Function to check the shop for a product and return it
	Parameters:
		s : struct Shop : datatype struct contain shop stock and cash
		pname: char : searched item in shop stock
	
	Return:
		p : char : product name
*/


{

	for(int j = 0; j < s->index; j++){
		if(strcmp(s->stock[j].product.name,pname)==0){
			return s->stock[j].product.name;   
         }         
   }

	return "NULL";
}

int getQuantity(struct Shop* s, char* pname)
/*
	Function to get stock quantity for product name
	Parameters:
		s : struct Shop : datatype struct contain shop stock and cash
		pname : char : product name 
	
	Returns:
		q : int : quantity, if product not in sock returns 0
*/
{
   // loop over shop index, get product name for each index and compare it to searched product
   // if product found in shop stock return its quantity
   // else return 0 
   for (int i = 0; i < s->index; i++){
      if(strcmp(s->stock[i].product.name,pname)==0){
        int q = s->stock[i].quantity;
		return q;		
      }
   }
	return 0;

};


void finishOrder(struct Shop* s, struct Customer* c)
/*  
	The task of this function is to check whether a given order can be completed and to update the shop parameters.

	In for loop:
		1. We compare whether a given item from the client's list is in the store's assortment.
		2. We check whether we have a sufficient quantity of a given product
		3. we check whether the client has a sufficient amount of cash in the budget.

	If the above conditions are met, we execute the order:
		- we reduce shop quantity,
		- we add order value to shop cash 
		- we reduce the client's budget.

	Parameters:
		s : struct Shop : datatype struct contain shop stock and cash
		c : struct Customer :Holds information about customer name, budget and shopping list 
*/
{	
	int some_var = 0;

	// for loop over a customer shopping list
	for (int i = 0; i<c->index; i++)
	{

		char *customer_item = malloc(sizeof(char) * 50); // Declare variable to hold product name
		strcpy(customer_item, c->shoppingList[i].product.name); 

		int customer_quantity = c->shoppingList[i].quantity; // Declare variable to hold customer quantity

		double product_price = c->shoppingList[i].product.price; // Declare variable to hold product price
		double order_value = customer_quantity * product_price; // variable to store order value (quantity * item_price)

		// call function getProductName  to check if customer product is in shop stock, returned value assign to shop_product   
		char* shop_product = getProductName(s,customer_item); 

		// call function getQuantity and returned value assign to shop_quantity
		int shop_quantity = getQuantity(s,shop_product); 

		// check if customer product not in shop
		if (shop_product == "NULL"){
			printf("I am very sorry, but unfortunately we do not sell %s \n",customer_item);
		} else {
			if (shop_quantity - customer_quantity >= 0)
				{		
				 	// if the order value is lower than the client's budget, the order can be processed
					if (order_value < c->budget)
					{
						// Loop over shop prroducts and update product quantity
						for (int j = 0; j<s->index; j++)
						{
							if (s->stock[j].product.name == shop_product)
							{
								// Reduce product quantity in shop stock
								s->stock[j].quantity = shop_quantity - customer_quantity;
							}
						}
						
						// Update shop cash
						s->cash = s->cash + order_value;
						// Update customer budget
						c->budget = c->budget - order_value;
						printf("You bought %d of %s \n",customer_quantity,customer_item);
					}
					else
					{
						printf("I'm very sorry but you don't have enough money, you are short of %.2f euro to buy %d %s\n", (order_value - c->budget), customer_quantity, customer_item );
					}
				}
				else
				{
					printf("I'm sorry but unfortunately we don't have enough in stock to cover your order for %d %s\n",customer_quantity, customer_item  );	
				}
		}
	}
	printf("*******************\n");
}	

	
struct Customer liveCustomer(struct Shop s)
/*
	Function to implement live shop. 
	It allow to buy product directly from console by entering customer name, budget, product name and quantity. 
	
	Then customer is created and returned to caller

	Parameters:
		s : struct Shop : Holds information about customer name, budget and shopping list 

	Returns:
		live_customer : struct Customer : // datatype struct contains Customer details name, budget and shopping list
*/
{
	// create live_customer variable
	struct Customer live_customer; 

	printf("Here is my stock list\n");
	printf("--------------------------\n");


	// loop over product stock to print product in console
	for (int i = 0; i < s.index; i++){
        struct Product p = s.stock[i].product;
		printProduct(p);
		printf("--------------------------\n");		
      }

	// read customer name from console 
	printf("\nPLEASE ENTER YOUR NAME: ");
	char *cust_name = malloc(sizeof(char) * 50);
	scanf("%s", cust_name);

	// assign variable to live_customer.name 
	live_customer.name = cust_name;
	fflush(stdin); // clear the output

	// read customer budget from console 
	printf("\nPLEASE ENTER YOUR BUDGET: ");
	double cust_budget;
	
	// https://stackoverflow.com/questions/210590/why-does-scanf-need-lf-for-doubles-when-printf-is-okay-with-just-f
	// I found on stack overflow how to read double from console 
	scanf("%lf", &cust_budget);

	// assign variable to live_customer.budget
	live_customer.budget = cust_budget;
	fflush(stdin);

	printf("\n");

	printf("What Would you likte to buy? \n");
	printf("\n");
	printf("\n");

	
	char choice;
	live_customer.index = 0; 

	// While loop will keep asking for product name and quantity until "n" is pressed
	while (strcmp(&choice, "n") != 0)
	{
		// gets product name from user
		printf("\nENTER PRODUCT NAME: ");
		char* customer_item = malloc(sizeof(char)*50);
		scanf("\n%[^\n]%*c", customer_item); // regular expression that reads product name without last "\n" character

		printf("\n");
		fflush(stdin);

		// gets product quantity from user 
		printf("ENTER PRODUCT QUANTITY: ");
		int customer_quantity;
		 
		scanf("%d", &customer_quantity);
		printf("\n");


		// creates Product,ProductStock and appends to customer shopping list. 
		struct Product live_product = {customer_item,getProduct(s,customer_item).price};
		struct ProductStock live_listItem = {live_product, customer_quantity};

		live_customer.shoppingList[live_customer.index] = live_listItem;	
		live_customer.index++;

		// if answer is "n" while loop breaks 
		printf("WOULD YOU LIKE TO BUY ANOTHER PRODUCT? y/n: ");
		printf("\n")
		fflush(stdin); 
		scanf("%s", &choice);
		

	}
	
	return live_customer;

} 

void show_options()
/* 
	Function to clear screen and display Main menu in console
	There are 6 options in the menu:
        1. Displays information about the store, the amount of money held, a list of products, their prices and quantity,
        2. Loads and processes the order from a CSV file where all purchase conditions are met.
        3. goes to Test Mode, displays the sub-menu, where we can load csv files where the purchase conditions have not been met.
        4. option in which we go to the live version of the store. in this option, we create a customer by providing his name and budget, 
            then create a shopping list and process the order.
        9. Clears the console screen and returns to the main menu,
        0. closes the shop

*/
{
	clearScreen();
	printf("##################################\n");
	printf("#                                #\n");
	printf("#       WELCOME TO MY SHOP       #\n");
	printf("#                                #\n");
	printf("##################################\n");
	printf("\n");
	printf("1. Print Shop Stock\n");
	printf("2. Get order from Shopping List\n");
	printf("3. Test Shop\n");
	printf("4. Live Mode\n");
	printf("9. Return to Menu\n");
	printf("0. Exit\n");
}


void testMenu(struct Shop shop)
/* 
	Function to display shop menu in test mode in console
	Test Mode is used to test the store in situations when some of the purchase conditions cannot be met. 
        The menu test consists of 4 options: 
            1. the customer does not have a sufficient budget to make a purchase, 
            2. the customer wants to buy a product that is not in the store, 
            3. the store does not have enough of a given product to fulfill the order. 
            0. returns to the main menu.
        A different CSV file is loaded for each of the three above situations.

	Parameter:
		s : struct Shop : Holds information about customer name, budget and shopping list
*/
{
	
	printf("##################################\n");
	printf("#                                #\n");
	printf("#       WELCOME TO MY SHOP       #\n");
	printf("#          (TEST MODE)           #\n");
	printf("##################################\n");
	printf("\n");
	printf("1. Test Low Budget\n");
	printf("2. Test Not in Stock\n");
	printf("3. Test Not enough Stock\n");
	printf("0. Exit\n");

	// creates variable choice
	int choice = -1;

	// while loop breaks when 0 is pressed
	while (choice != 0)
	{
		fflush(stdin);
		printf("\nPlease choose an option: ");
		scanf("%d",&choice);
		printf("\n");

		if(choice == 1)
		{
			printf("**** Load Test Low Budget from CSV file **** \n\n");
			// create customer from CSV file 
			struct Customer customer = CustOrder(shop, "..\\test_low_budget.csv");
			// finishes custoemr order 
			printCustomer(customer);
			finishOrder(&shop, &customer);
			printf("\n");



		} else if (choice == 2)
		{
			printf("**** Load Test Not in Stock from CSV file **** \n\n");
			// create customer from CSV file 
			struct Customer customer_stock = CustOrder(shop, "..\\test_not_in_stock.csv");
			// finishes custoemr order 
			printCustomer(customer_stock);
			finishOrder(&shop, &customer_stock);
			printf("\n");

		} else if (choice == 3)
		{
			printf("**** Load Test Not enough Stock **** \n\n");
			// create customer from CSV file
			struct Customer customer_stock = CustOrder(shop, "..\\test_not_enough_stock.csv");
			// finishes custoemr order 
			printCustomer(customer_stock);
			finishOrder(&shop, &customer_stock);
			printf("\n");


		} else if (choice == 0)
		{
			// returns to main menu
			show_options();
		}
	
	}
	
}


void displayMenu(struct Shop shop)
/* 
	Adds functionality to the main menu. We are asked to choose one of the 6 options. 
    he loop breaks when option 0 is selected. The store closes

	Parameter:
		s : struct Shop : Holds information about customer name, budget and shopping list
*/
{
	show_options(); // display main  menu

	int choice = -1;
	
	// while loop breaks when 0 is pressed

	while (choice != 0)
	{
		
		printf("\nPlease choose an option (press 9 to show menu option, 0 to exit): ");
		fflush(stdin);
		scanf("%d",&choice);
		printf("\n");

		if (choice == 1)
		{
			// calls method to print shop
			printShop(shop);
	
		}else if (choice == 2)
		{
			printf("**** Get order from ORDER.CSV shopping list ****\n\n");
			// creates customer from csv file
			struct Customer customer = CustOrder(shop, "..\\order.csv");
			printf("\n");
			printf("---===<< YOUR ORDER CONFIRMAION >>===---\n \n");
			// prints customer
			printCustomer(customer);
			// finishes customer order
			finishOrder(&shop, &customer);
			printf("\n");
		} 
		
		else if (choice == 3)
		{
			clearScreen(); // Call clear screen function
			testMenu(shop); // call Test Menu for testing  
			
		} else if (choice == 4)
		{
			
			printf("Hello!!, Welcome To my Live Shop.  \n");
			printf("\n");
			printf("Please Take a look around \n");
			printf("\n");
			// creates live customer
			struct Customer live_customer = liveCustomer(shop);
			
			printf("\n");
			printf("---===<< YOUR ORDER CONFIRMAION >>===---\n \n");
			// prints live mode customer
			printCustomer(live_customer);
			// finishes live customer order
			finishOrder(&shop, &live_customer);
			

		} else if (choice == 9)
		{
			show_options(); // call show options function
		}

	}
	printf("\nThank You for shopping with Us.");

	
	
}




// -------------------------------- //
int main(void) 
/*
	Program starts here: 
	struct Shop as a shop variable is created
	and main menu is displayed 
*/
{
	struct Shop shop = createAndStockShop();
	displayMenu(shop);
	

    return 0;
}


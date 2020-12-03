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



//####################################################################//



void printProduct(struct Product p)
/* 
	Method to print information about product
	Parameters:
		p : struct : Holds information about product name and price
*/
{
	printf("PRODUCT NAME: %s \nPRODUCT PRICE: %.2f\n", p.name, p.price);
	//printf("-------------\n");
}

void printCustomer(struct Customer c)
/*
	Method to print customer details and shopping list 
	Parameters:
		c : struct : Holds information about customer name, budget and shopping list 
*/
	
{	
	double total_price = 0.0;
	// print customer name and budget
	printf("CUSTOMER NAME: %s \nCUSTOMER BUDGET: %.2f\n", c.name, c.budget);
	printf("-------------\n");

	// iterates over customer shopping list 
	for(int i = 0; i < c.index; i++) // 
	{	
		// method call printProduct
		printProduct(c.shoppingList[i].product); // prints product from shopping list 
		printf("%s ORDERS %d OF ABOVE PRODUCT\n", c.name, c.shoppingList[i].quantity); // prints information about customer name and quantity
		double cost = c.shoppingList[i].quantity * c.shoppingList[i].product.price; // calculate cost
		printf("The cost to %s will be e%.2f\n", c.name, cost); // print costs
		printf("---------------\n");
		total_price += cost;
	}

	printf("%s's Provisional total cost: %.2f\n", c.name, total_price);
	printf("%s's Provisional updated budget: %.2f\n", c.name, (c.budget - total_price));
	printf("#######################\n");
}

struct Shop createAndStockShop()
/*
	Method to create Shop, read stock from CSV file 

	Returns:
		shop : struct 
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
	
	// create shop and initiate cash variable
	struct Shop shop = { cash };

	// loop 
    while ((read = getline(&line, &len, fp)) != -1) {
        
		// method strtok breaks string str into a tokens using delimiter "," as string
		char *n = strtok(line, ",");
		char *p = strtok(NULL, ",");
		char *q = strtok(NULL, ",");

		// convert variables from string 
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

struct Product getProduct(struct Shop s, char* pname){
   // check the shop for a product and return it
   struct Product p;
   for (int i = 0; i < s.index; i++){
      if(strcmp(s.stock[i].product.name,pname)==0){
        p = s.stock[i].product;
      }
   }
   return p;
};


void clearScreen()
/*
https://stackoverflow.com/questions/2347770/how-do-you-clear-the-console-screen-in-c
Method to Clear screen that will work for linux, windows and Mac OS. 
*/
{
  system("cls||clear");
}

void printShop(struct Shop s)
{
	printf("Shop has %.2f in cash\n", s.cash);
	printf("----------------\n");
	for (int i = 0; i < s.index; i++)
	{
		printProduct(s.stock[i].product);
		printf("The shop has %d of the above\n", s.stock[i].quantity);
		printf("------------------\n");
	}
}

struct Customer CustOrder(struct Shop s, char* order_csv_file)
{	
	FILE * fp;
	char * line = NULL;
	size_t len = 0;
	size_t read;

	fp = fopen(order_csv_file,"r");

	getline(&line, &len, fp);

	char *cName = strtok(line,",");
	char *cBudget = strtok(NULL,",");

	char *custName = malloc(sizeof(char)*50);
	strcpy(custName,cName);

	double custBudget = atof(cBudget);

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


void finishOrder(struct Shop* s, struct Customer* c)
{
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

		param : struct Shop 
		param : struct Customer
	*/
	
	int some_var = 0;

	// for loop over a customer shopping list
	for (int i = 0; i<c->index; i++)
	{

		char *customer_item = malloc(sizeof(char) * 50); // Declare variable to hold product name
		strcpy(customer_item, c->shoppingList[i].product.name); 

		int customer_quantity = c->shoppingList[i].quantity; // Declare variable to hold customer quantity

		double product_price = c->shoppingList[i].product.price; // Declare variable to hold product price
		double order_value = customer_quantity * product_price; // variable to store order value (quantity * item_price)
		
		// inner loop over a shop products 
		for (int j = 0; j<s->index; j++)
		{
			
			char *shop_item = malloc(sizeof(char) * 50);
			int shop_quantity = s->stock[j].quantity; // Declare variable to hold shop quantity for each product

			strcpy(shop_item, s->stock[j].product.name);	
				
			// compare two products by it's name and store result in variable 
			// int result_product = product_compare( customer_item, shop_item ); 
			 int result_product = strcmp( customer_item, shop_item ); 

			// if result_product is equal 1 it means that product from sopping list was found in shop stock
			
			if (result_product == 0)
			{
				some_var = 1;
				// if the difference between shop_quantity and customer_quantity is greater than zero, the order can be fulfilled
				if (shop_quantity - customer_quantity >= 0)
				{
					// if the order value is lower than the client's budget, the order can be processed
					if (order_value < c->budget)
					{
						// Update stock quantity
						s->stock[j].quantity = shop_quantity - customer_quantity;
						// Update shop cash
						s->cash = s->cash + order_value;
						// Update customer budget
						c->budget = c->budget - order_value;
						printf("You bought %d of %s \n",customer_quantity,customer_item);
					}
					else
					{
						printf("Sorry, but you are short of e%.2f to buy %d of %s", (order_value - c->budget), customer_quantity, customer_item );
					}
				}
				else
				{
					printf("Sorry, We have not enough stock of %s\n",customer_item );	
				}
			}
		}

		if (some_var == 0)
		{
			printf("Sorry, We dont have %s in our stock\n",customer_item );	
		} 
		
			
	}



	printf("*******************\n");
}	

	


// --------------- TEST MODE SECTION ----------------// 


void testMenu(struct Shop shop)
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

	int choice = -1;

	while (choice != 0)
	{
		fflush(stdin);
		printf("\nPlease choose an option: ");
		scanf("%d",&choice);
		printf("\n");

		if(choice == 1)
		{
			printf("**** Load Test Low Budget from CSV file **** \n\n");
			struct Customer customer = CustOrder(shop, "..\\test_low_budget.csv");
			finishOrder(&shop, &customer);
			printf("\n");



		} else if (choice == 2)
		{
			printf("**** Load Test Not in Stock from CSV file **** \n\n");
			struct Customer customer_stock = CustOrder(shop, "..\\test_not_in_stock.csv");
			finishOrder(&shop, &customer_stock);
			printf("\n");

		} else if (choice == 3)
		{
			printf("**** Load Test Not enough Stock **** \n\n");
			struct Customer customer_stock = CustOrder(shop, "..\\test_not_enough_stock.csv");
			finishOrder(&shop, &customer_stock);
			printf("\n");


		} else if (choice == 0)
		{
			show_options();
		}
	
	}
	
}

// ---------- GET ORDER FROM SHOPPING LIST -------------//

void show_options()

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

void displayMenu(struct Shop shop)
/* 
	Method to print menu, that user can choose between options,
	return : char : option choosed by user 
	
*/
{

	show_options();

	int choice = -1;
	
	while (choice != 0)
	{
		
		printf("\nPlease choose an option (press 9 to show menu option, 0 to exit): ");
		fflush(stdin);
		scanf("%d",&choice);
		printf("\n");

		if (choice == 1)
		{
			
			printShop(shop);
	
		}else if (choice == 2)
		{
			printf("**** Get order from ORDER.CSV shopping list ****\n\n");
			struct Customer customer = CustOrder(shop, "..\\order.csv");
			printCustomer(customer);
			finishOrder(&shop, &customer);
			printf("\n");
		} 
		
		else if (choice == 3)
		{
			clearScreen(); // Call clear screen function
			testMenu(shop); // call Test Manu for testing  
			
		} else if (choice == 3)
		{
			printf("Welcome in Live mode");
		} else if (choice == 9)
		{
			show_options(); // call show options function
		}

	}
	printf("\nBye.");

	
	
}




// -------------------------------- //
int main(void) 
{
	struct Shop shop = createAndStockShop();
	displayMenu(shop);
	

    return 0;
}


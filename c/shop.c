#include <stdio.h>
#include <string.h>
#include <stdlib.h>

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
		printf("The cost to %s will be €%.2f\n", c.name, cost); // print costs
	}
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

    fp = fopen("../stock.csv", "r");  // opens csv file 

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

void printShop(struct Shop s)
{
	printf("Shop has %.2f in cash\n", s.cash);
	for (int i = 0; i < s.index; i++)
	{
		printProduct(s.stock[i].product);
		printf("The shop has %d of the above\n", s.stock[i].quantity);
		printf("------------------\n");
	}
}

void displayMenu(struct Shop shop)
/* 
	Method to print menu, that user can choose between options,
	
*/
{
	printf("##################################\n");
	printf("#                                #\n");
	printf("#       WELCOME TO MY SHOP       #\n");
	printf("#                                #\n");
	printf("##################################\n");
	printf("\n");
	printf("1. Print Shop Stock\n");
	printf("2. Test Shop\n");
	printf("3. Live Mode\n");
	printf("0. Exit\n");

	// create variable choice and assign -1
	int choice = -1;

	
	while (choice != 0)
	{
		fflush(stdin);
		printf("\nPlease choose an option: ");
		scanf("%d",&choice);
		printf("\n");

		if (choice == 1)
		{
			printShop(shop);
		} else if (choice == 2)
		{
			printf("To be completed");
		} else if (choice == 3)
		{
			printf("Welcome in Live mode");
		}
	}
	printf("\nBye.");
}

int main(void) 
{
	struct Shop shop = createAndStockShop();
	displayMenu(shop);
	
	// printShop(shop);

    return 0;
}


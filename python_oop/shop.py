import csv
from product import Product
from product_stock import ProductStock

class Shop:
    
    def __init__(self, path):
        self.stock = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)
        
        

    def getItem(self,name):

        for n in self.stock:
            if n.name() == name:
                return n
        return None

    # def getQuantity(self, name):
    #     for q in self.stock:
    #         if q.product.name == name:
    #             return q
        
    #     return 0

    def finish_order(self, shopping_list, budget):

        for item in shopping_list:
            
            shop_item = self.getItem(item.name())
           
            if shop_item == None:
                print(f"I am very sorry, but unfortunately we do not sell {item.name()}")
            else:
                order_value = item.quantity * shop_item.unit_price()
                if item.quantity <= shop_item.quantity:

                    if budget > order_value:

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
        str = ""
        str += f'Shop has {self.cash:,.2f} in cash'
        str += "\n"
        str += "--------------------------"
        str += "\n"
        for item in self.stock:
            str += f"{item}\n"
        return str
class ProductStock:
    '''
        Class to store information about product stock
    '''
    
    def __init__(self, product, quantity):
        '''
        Paramaters:
            product  : Product  : instance of a Product class 
            quantity : int      : quantity of the product in store
        '''

        self.product = product
        self.quantity = quantity
    
    def name(self):
        '''
            Method to return product name
        '''
        return self.product.name
    
    def unit_price(self):
        '''
            Method to return product price
        '''
        return self.product.price
        
    def cost(self):
        '''
            Method to calculate product cost
        '''
        return self.unit_price() * self.quantity
        
    def __repr__(self):
        '''
            Special Method for string representation for ProductStock object. 
            This is how the ProductStock object will look when we call print() function.

            Returns:
                str
        '''
        return f"{self.product} QUANTITY: {self.quantity:.0f}"
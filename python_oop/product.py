class Product:
    '''
        Class to store information about product
    '''
    def __init__(self, name, price=0):
        '''
        Paramaters:
            name  : str   : product name 
            price : float : product price
        '''
        self.name = name
        self.price = price
    
    def __repr__(self):
        '''
            Special Method for string representation for Product object. 
            This is how the Product object will look when we call print() function.

            Returns:
                str
        '''
        return f'PRODUCT NAME: {self.name} - PRODUCT PRICE: €{self.price:,.2f}'
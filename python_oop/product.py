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
        return f'PRODUCT NAME: {self.name} - PRODUCT PRICE: €{self.price:,.2f}'
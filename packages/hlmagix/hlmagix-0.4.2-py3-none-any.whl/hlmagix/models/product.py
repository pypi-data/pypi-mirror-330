# product.py
# This module contains the Product model class

class Product:
    """
    Product model representing an item for sale.
    
    Attributes:
        product_id (int): Unique identifier for the product
        name (str): Name of the product
        price (float): Price of the product
        in_stock (bool): Whether the product is in stock
    """
    
    def __init__(self, product_id, name, price, in_stock=True):
        """
        Initialize a new Product instance.
        
        Args:
            product_id (int): Unique identifier for the product
            name (str): Name of the product
            price (float): Price of the product
            in_stock (bool, optional): Whether the product is in stock. Defaults to True.
        """
        self.product_id = product_id
        self.name = name
        self.price = price
        self.in_stock = in_stock
    
    def __str__(self):
        """
        Return a string representation of the Product.
        
        Returns:
            str: String representation of the Product
        """
        return f"Product(id={self.product_id}, name={self.name}, price=${self.price:.2f})"
    
    def mark_out_of_stock(self):
        """
        Mark the product as out of stock.
        """
        self.in_stock = False
    
    def mark_in_stock(self):
        """
        Mark the product as in stock.
        """
        self.in_stock = True
    
    def apply_discount(self, discount_percent):
        """
        Apply a discount to the product price.
        
        Args:
            discount_percent (float): Discount percentage (0-100)
            
        Returns:
            float: The discounted price
        """
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        
        discount_factor = 1 - (discount_percent / 100)
        return self.price * discount_factor
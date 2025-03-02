# user.py
# This module contains the User model class

class User:
    """
    User model representing a system user.
    
    Attributes:
        user_id (int): Unique identifier for the user
        username (str): Username for login
        email (str): User's email address
        is_active (bool): Whether the user account is active
    """
    
    def __init__(self, user_id, username, email, is_active=True):
        """
        Initialize a new User instance.
        
        Args:
            user_id (int): Unique identifier for the user
            username (str): Username for login
            email (str): User's email address
            is_active (bool, optional): Whether the user account is active. Defaults to True.
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.is_active = is_active
    
    def __str__(self):
        """
        Return a string representation of the User.
        
        Returns:
            str: String representation of the User
        """
        return f"User(id={self.user_id}, username={self.username}, email={self.email})"
    
    def deactivate(self):
        """
        Deactivate the user account.
        """
        self.is_active = False
    
    def activate(self):
        """
        Activate the user account.
        """
        self.is_active = True
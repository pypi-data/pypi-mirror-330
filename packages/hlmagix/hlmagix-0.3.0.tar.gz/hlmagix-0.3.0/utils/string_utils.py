# string_utils.py
# This module contains utility functions for string manipulation

def capitalize_words(text):
    """
    Capitalize the first letter of each word in a string.
    
    Args:
        text (str): The input string to process
        
    Returns:
        str: The processed string with each word capitalized
    """
    if not text:
        return ""
    return " ".join(word.capitalize() for word in text.split())


def reverse_string(text):
    """
    Reverse a string.
    
    Args:
        text (str): The input string to reverse
        
    Returns:
        str: The reversed string
    """
    return text[::-1]
from tkinter import *

def position_image(root, img):
    """ Center an image in the root window """
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    img_width = img.winfo_width()
    img_height = img.winfo_height()

    x = (window_width - img_width) / 2
    y = (window_height - img_height) / 8
    
    img.place(x=x, y=y)

def validate_password(password):
    """
    Validates that a password meets specific criteria:
    - At least 7 characters long
    - Contains at least one uppercase letter
    - Contains at least one special character
    """
    if len(password) < 7:
        return False, "Password must be at least 7 characters long"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(char in "!@#$%^&*()_+" for char in password):
        return False, "Password must contain at least one special character"
    return True, "Password is valid"

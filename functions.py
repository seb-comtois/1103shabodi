# functions.py

def position_image(root, img):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    img_width = img.width()
    img_height = img.height()

    x = (window_width - img_width) / 2
    y = (window_height - img_height) / 3
    
    img.place(x=x, y=y)

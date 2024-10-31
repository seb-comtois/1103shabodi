from tkinter import *
from PIL import Image, ImageTk

# configuration for the window
root = Tk()
root.title("Remote mentor tool")
root.configure(background="grey")
root.minsize(200, 200)
root.maxsize(1920, 1080)

#create text
text1 = Label(root, text="Shabodi mentorship software")
text1.pack()


#import image
image_shabodi = PhotoImage(file="shabodi_logo.gif")
img = Label(root, image = image_shabodi)
img.pack()



#needed to run the program
root.mainloop()
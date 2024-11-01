from tkinter import *
from PIL import Image, ImageTk
import functions

# configuration for the window
root = Tk()
root.title("Remote mentor tool")
root.configure(background="grey")
root.geometry("1000x800")

#create text
text1 = Label(root, text="Shabodi mentorship software")
text1.pack()


#import image
image_shabodi = PhotoImage(file="shabodi_logo.gif")
img1 = Label(root, image = image_shabodi)
img1.pack()

root.update_idletasks()
functions.position_image(root, img1)




#needed to run the program
root.mainloop()
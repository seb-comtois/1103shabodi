from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import functions
import login

# configuration for the window
root = Tk()
root.title("Remote mentor tool")
root.configure(background="grey")
root.geometry("1000x800")

#create font
title = font.Font(family="Helvetica", size=16, weight="bold")

#create text
text1 = Label(root, text="Shabodi mentorship software", bg="grey", font = title)
text1.place(x=390, y=50)

#import image
image_shabodi = PhotoImage(file="shabodi_logo.gif")
img1 = Label(root, image = image_shabodi)
img1.pack()

root.update_idletasks()
functions.position_image(root, img1)

#login button
log_in = Button(root, text="Log in", bg="grey", width=20, height=2, font=title, command=lambda: login.login_window(root, title))
log_in.place(x=392, y=300)









#needed to run the program
root.mainloop()
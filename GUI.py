from tkinter import *

root = Tk()


def printname(event):
    print('My name is alex')


button1 = Button(root, text='Print name')
button1.bind('<Button-1>', printname)
button1.grid(row=0)


root.mainloop()  # to keep window open

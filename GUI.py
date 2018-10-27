from tkinter import *

root = Tk()

topframe = Frame(root)
topframe.pack()

bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)

button1 = Button(topframe, text='Button 1', fg='red')
button2 = Button(topframe, text='Button 2', fg='blue')
button3 = Button(topframe, text='Button 3', fg='green')
button4 = Button(topframe, text='Button 4', fg='black')

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=BOTTOM)

root.mainloop()  # to keep window open

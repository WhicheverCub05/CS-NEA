from tkinter import *


class TheClass:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.printButton = Button(frame, text='print message', command=self.printMessage)
        self.printButton.pack(side=LEFT)

        self.quitButton = Button(frame, text='Quit', command=frame.quit)  # closes the mainloop()
        self.quitButton.pack(side=LEFT)

    def printMessage(self):
        print('wow this actually worked!')


root = Tk()
b = TheClass(root)
root.mainloop()  # to keep window open

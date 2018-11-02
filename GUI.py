from tkinter import *


class TheClass:

    def __init__(self, master):
        '''
        frame = Frame(master)  # height=300, width=500
        frame.pack()
        '''
        root.geometry("500x300")

        self.topframe = Frame(root, background="purple")
        self.topframe.pack(side=TOP)

        self.setupframe = Frame(self.topframe, background='green')
        self.setupframe.pack(side=TOP)

        self.midframe = Frame(root, background='blue')
        self.midframe.pack(side=TOP)

        self.bottomframe = Frame(root, width=200, height=300, background="orange")
        self.bottomframe.pack(side=BOTTOM, expand=0)

        self.setuplabel = Label(self.setupframe, text='Setup before running the program')
        self.setuplabel.pack(side=TOP)

        self.setuptext = Label(self.setupframe, text='Step 1                                                     Step 2'
                                                     '                                                     Step 3')
        self.setuptext.pack()

        self.steptext1 = Label(self.setupframe, text='make sure the inline \n is outputting')
        self.steptext1.pack(side=LEFT)

        self.steptext3 = Label(self.setupframe, text='Run the sequence')
        self.steptext3.pack(side=RIGHT)

        self.steptext2 = Label(self.setupframe, text='make sure the volume\n on the inline and output are\n '
                                                     'at the volume of intended use')
        self.steptext2.pack()

        self.startButton = Button(self.midframe, text='Start', width=10, height=2)
        self.startButton.pack(side=LEFT)

        self.printCheckbox = Checkbutton(self.midframe, text='Run custom frequencies?')
        self.printCheckbox.pack(side=RIGHT)

        self.graphtext = Label(self.bottomframe, text='Graph')  # closes the mainloop()
        self.graphtext.pack(side=LEFT)

        self.graphtext = Label(self.bottomframe, text='Graph2', height=100)  # closes the mainloop()
        self.graphtext.pack(side=RIGHT)

    def print_message(self):
        print('wow this actually worked!')


root = Tk()
b = TheClass(root)
root.mainloop()  # to keep window open

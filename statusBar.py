import tkinter
import textEditor
class StatusBar(tkinter.Frame):   
    def __init__(self, master, tem):
        tkinter.Frame.__init__(self, master)
        self.variable=tkinter.StringVar()        
        self.tem = tem
        self.label=tkinter.Label(self, bd=1, anchor=tkinter.W,
                           textvariable=self.variable,
                           font=('arial',16,'normal'))
        self.variable.set('row 1 col 1')
        self.label.pack(fill=tkinter.X)        
        self.pack()

    def notify_cursor(self):
        s = 'row ' + str(self.tem.cursor_location.row + 1) + ' col ' + str(self.tem.cursor_location.col + 1)
        self.variable.set(s)
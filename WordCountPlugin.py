import textEditorModel
import undoManager
import ClipboardStack
import tkinter as tk
from tkinter import scrolledtext

class Plugin():
    
    def get_name(self):
        return 'statistics'
    
    def get_description(self):
        return 'Various statistics'
    
    def execute(self, tem):
        lines = 0
        wc = 0
        cc = 0
        for line in tem.lines:
            lines += 1
            wc += len(line.split(' '))
            cc += len(line)

        window = tk.Tk()
        window.title("Text Area Example")

        # Create a text area
        label = tk.Label(window, text='lines: {}, words: {}, chars: {}'.format(
            lines, wc, cc
        )).pack()

        print(lines)

        # Start the main loop
        window.mainloop()
            
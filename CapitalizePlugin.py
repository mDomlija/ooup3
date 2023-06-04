import textEditorModel
import undoManager
import ClipboardStack
import tkinter as tk
from tkinter import scrolledtext

class Plugin():
    
    def get_name(self):
        return 'Capitalize'
    
    def get_description(self):
        return 'Various statistics'
    
    def execute(self, tem):
        lines = list ( map ( lambda x: x.title(), tem.lines ) )
        tem.lines = lines
        tem.notify_text_observers()
            
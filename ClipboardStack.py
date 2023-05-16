class ClipboardStack:
    
    def __init__(self):
        self.texts = []
        self.clipboard_observers = []

    def attach_clipboard_observer(self, o):
        self.clipboard_observers.append(o)

    def notify_clipboard_observers(self, status):
        for o in self.clipboard_observers:
            o.update_clipboard(status)

    def push(self, text):
        self.texts.append(text)
        self.notify_clipboard_observers(True)

    def peek(self):
        if len(self.texts) > 0:
            return self.texts[-1]
        
    def pop(self):
        if len(self.texts) > 0:
            if len(self.texts) == 1:
                self.notify_clipboard_observers(False)
            return self.texts.pop()


        
        
    


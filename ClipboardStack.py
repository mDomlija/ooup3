class ClipboardStack:
    
    def __init__(self):
        self.texts = []

    def push(self, text):
        self.texts.append(text)

    def peek(self):
        if len(self.texts) > 0:
            return self.texts[-1]
        
    def pop(self):
        if len(self.texts) > 0:
            return self.texts.pop()
        
        
    


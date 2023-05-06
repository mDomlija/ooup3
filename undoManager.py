class UndoManager:
    
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []


    def undo(self):
        if len(self.undo_stack):
            print('hello')
            action = self.undo_stack.pop()
            action.execute_undo()
            self.redo_stack.append(action)

    def push(self, action):
        self.redo_stack = []
        self.undo_stack.append(action)

    def pop_undo(self):
        if len(self.undo_stack):
            return self.undo_stack()
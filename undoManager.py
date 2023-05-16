class UndoManager:
    
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        self.undo_observers = []
        self.redo_observers = []

    def attach_undo_observer(self, o):
        self.undo_observers.append(o)

    def attach_redo_observer(self, o):
        self.redo_observers.append(o)

    def notify_undo_observers(self, status):
        for o in self.undo_observers:
            o.update_undo(status)
        
    def notify_redo_observers(self, status):
        for o in self.redo_observers:
            o.update_redo(status)


    def undo(self):
        if len(self.undo_stack):
            print('hello')
            action = self.undo_stack.pop()
            action.execute_undo()
            self.redo_stack.append(action)

            if len(self.undo_stack) == 0:
                self.notify_undo_observers(False)
            if len(self.redo_stack) == 1:
                self.notify_redo_observers(True)

    def redo(self):
        if len(self.redo_stack):
            action = self.redo_stack.pop()
            action.execute_do()
            self.undo_stack.append(action)

            if len(self.redo_stack) == 0:
                self.notify_redo_observers(False)
            if len(self.undo_stack) == 1:
                self.notify_undo_observers(True)

    def push(self, action):
        self.redo_stack = []
        self.undo_stack.append(action)
        self.notify_undo_observers(True)

    def pop_undo(self):
        if len(self.undo_stack):
            return self.undo_stack()
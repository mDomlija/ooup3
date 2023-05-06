import textEditorModel
class EditAction:
    def execute_do(self):
        pass

    def execute_undo(self):
        pass 

class InsertAction(EditAction):

    def __init__(self, cursor, char, tem):
        self.cursor = cursor.copy()
        self.char = char
        self.tem = tem

    def execute_do(self):
        self.tem.cursor_location = self.cursor.copy()
        self.tem.insert(self.char)

    def execute_undo(self):
        self.tem.cursor_location = self.cursor.copy()
        self.tem.delete_after()

class InsertStringAction(EditAction):
    def __init__(self, cursor, string, tem):
        self.cursor = cursor.copy()
        self.string = string
        self.tem = tem

    def execute_do(self):
        self.tem.cursor_location = self.cursor.copy()
        self.tem.insert_string(self.string)
        self.after_cursor = self.tem.cursor_location.copy() 

    def execute_undo(self):
        if self.after_cursor == None:
            return
        
        self.tem.selection_range = textEditorModel.LocationRange(self.cursor, self.after_cursor)

        self.tem.delete_selection()

class deleteSelectionAction(EditAction):

    def __init__(self, cursor, selection, tem):
        self.cursor = cursor.copy()
        self.selection = selection
        self.tem = tem 

    def execute_do(self):
        self.tem.selection_range = self.selection
        self.deleted_text = self.tem.get_selection_text()
        self.cursor_after = self.selection.start
        self.tem.delete_selection()

    def execute_undo(self):
        print(self.deleted_text)
        print(self.cursor_after.row)
        print(self.cursor_after.col)
        self.tem.cursor_location = self.cursor_after.copy()
        self.tem.insert_string(self.deleted_text)

class deleteBeforeAction(EditAction):
    def __init__(self, cursor, tem):
        self.cursor = cursor
        self.tem = tem 

    def execute_do(self):
        self.tem.cursor_location = self.cursor.copy()
        self.deleted_char = self.tem.get_char_before()
        self.tem.delete_before()
        self.cursor_after = self.tem.cursor_location

    def execute_undo(self):
        print(self.cursor_after.row)
        print(self.cursor_after.col)
        self.tem.cursor_location = self.cursor_after.copy()
        self.tem.insert(self.deleted_char)
        

    

import tkinter
import tkinter.font as tkfont
import textEditorModel
import ClipboardStack
import editActions
import undoManager

class TextEditor(tkinter.Frame):
    LINE_HEIGHT = 30
    LEFT_PADDING = 20
    FONT = ('Arial', '12')

    def __init__(self, tem):
        super().__init__()
        self.text_editor_model = tem
        self.canvas = tkinter.Canvas(self)
        self.shift_key = False
        self.has_active_selection = False
        self.selection_ids = []
        self.clipboard = ClipboardStack.ClipboardStack()
        self.undo_manager = undoManager.UndoManager()

        tem.attach_cursor_observer(self)
        tem.attach_text_observer(self)
        self.line_ids = []

        self.draw_ui()


    #------------------------------- drawing ----------------------------------------

    def draw_cursor(self):

        font = tkfont.Font(family=self.FONT[0], size=self.FONT[1])

        loc = self.text_editor_model.cursor_location

        current_line = self.text_editor_model.lines[loc.row]
        text_length = font.measure(current_line[0 : loc.col])

        x_position = text_length + self.LEFT_PADDING -1
        y_position = (loc.row  + 1 ) * self.LINE_HEIGHT

        self.cursor_id = self.canvas.create_line(x_position, 
                                y_position, 
                                x_position,
                                y_position + self.LINE_HEIGHT * 0.6 ,
                                fill='#E9967A',
                                width=1
                                )
        
    def draw_ui(self):

        self.master.title("Lyrics")
        self.pack(fill=tkinter.BOTH, expand=1)

        self.draw_text()
        
        self.draw_cursor()
        self.draw_selection()
        self.canvas.pack(fill=tkinter.BOTH, expand=1)

    def draw_text(self):
        canvas = self.canvas
        for i in range(len(self.text_editor_model.lines)):
            line = self.text_editor_model.lines[i]
            line_id = canvas.create_text(self.LEFT_PADDING, self.LINE_HEIGHT * (i + 1), anchor=tkinter.NW, 
                               font=self.FONT, text=line)
            self.line_ids.append(line_id)

                                
                            
    def draw_selection(self):
        if self.text_editor_model.selection_range == None:
            return
        
        font = tkfont.Font(family=self.FONT[0], size=self.FONT[1])
        

        start_row = self.text_editor_model.selection_range.start.row
        start_col = self.text_editor_model.selection_range.start.col
        end_row = self.text_editor_model.selection_range.end.row
        end_col = self.text_editor_model.selection_range.end.col

        rec_ids = []

        if start_row == end_row:
            current_line = self.text_editor_model.lines[start_row]
            left_offset = self.LEFT_PADDING + font.measure(current_line[0 : start_col]) #calcualtes start of the selection area in x axis
            right_border = self.LEFT_PADDING + font.measure(current_line[0 : end_col]) #calculates the end of the selection area in x axis
            top_border = (start_row  + 1 ) * self.LINE_HEIGHT
            rec_id = self.canvas.create_rectangle(left_offset,
                                            top_border,
                                            right_border,
                                            top_border + self.LINE_HEIGHT * 0.65,
                                            outline="#f11", fill="", width=1)
            rec_ids.append(rec_id)
        
        else:
            first_line = self.text_editor_model.lines[start_row]
            left_offset = self.LEFT_PADDING + font.measure(first_line[0 : start_col]) #calcualtes start of the selection area in x axis
            right_border = self.LEFT_PADDING + font.measure(first_line) #calculates the end of the selection area in x axis
            top_border = (start_row  + 1 ) * self.LINE_HEIGHT
            first_rec_id = first_rec = self.canvas.create_rectangle(left_offset,
                                            top_border,
                                            right_border,
                                            top_border + self.LINE_HEIGHT * 0.65,
                                            outline="#f11", fill="", width=1)
            rec_ids.append(first_rec_id)
            
            for row in range(start_row + 1, end_row):
                current_line = self.text_editor_model.lines[row]
                left_offset = self.LEFT_PADDING #calcualtes start of the selection area in x axis
                right_border = self.LEFT_PADDING + font.measure(current_line) #calculates the end of the selection area in x axis
                top_border = (row  + 1 ) * self.LINE_HEIGHT
                rec_id = self.canvas.create_rectangle(left_offset,
                                            top_border,
                                            right_border,
                                            top_border + self.LINE_HEIGHT * 0.65,
                                            outline="#f11", fill="", width=1)
                rec_ids.append(rec_id)
                
            last_line = self.text_editor_model.lines[end_row]
            left_offset = self.LEFT_PADDING #calcualtes start of the selection area in x axis
            right_border = self.LEFT_PADDING + font.measure(last_line[0 : end_col]) #calculates the end of the selection area in x axis
            top_border = (end_row  + 1 ) * self.LINE_HEIGHT
            last_line_id = self.canvas.create_rectangle(left_offset,
                                            top_border,
                                            right_border,
                                            top_border + self.LINE_HEIGHT * 0.65,
                                            outline="#f11", fill="", width=1)
            rec_ids.append(last_line_id)

        self.selection_ids = rec_ids


#--------------------------notify and refresh --------------------------------------------------
    def notify_text(self):
        self.refresh_text()
        
    def refresh_text(self):
        for line in self.line_ids:
            self.canvas.delete(line)

        self.draw_text()
        self.refresh_cursor()

    def notify_cursor(self):
        self.refresh_cursor()
        

    def refresh_cursor(self):
        canvas = self.canvas
        canvas.delete(self.cursor_id)
        self.draw_cursor()

    def refresh_selection(self):
        for rec in self.selection_ids:
            self.canvas.delete(rec)
        
        self.draw_selection()
        
    

    def selection_handler(self, previous_cursor, direction):

        if self.shift_key:
            if self.has_active_selection:
                if self.selection_direction == 'start': 
                    self.text_editor_model.selection_range.set_start(self.text_editor_model.cursor_location)
                elif self.selection_direction == 'end':
                    self.text_editor_model.selection_range.set_end(self.text_editor_model.cursor_location)

                if self.text_editor_model.selection_range.start == self.text_editor_model.selection_range.end:
                    self.selection_direction = direction


            else:
                self.has_active_selection = True
                self.selection_direction = direction
                self.text_editor_model.selection_range = textEditorModel.LocationRange(
                    previous_cursor, self.text_editor_model.cursor_location
                )
            
            self.refresh_selection()
        else:
            self.has_active_selection = False
            self.text_editor_model.selection_range = None
            self.refresh_selection()

#--------------------key binds------------------------------------------------------------------

    def left_key_pressed(self, e):
        previous_cursor = self.text_editor_model.cursor_location.copy()
        self.text_editor_model.move_cursor_left()
        self.selection_handler(previous_cursor, 'start')

    def right_key_pressed(self, e):
        previous_cursor = self.text_editor_model.cursor_location.copy()
        self.text_editor_model.move_cursor_right()
        self.selection_handler(previous_cursor, 'end')

    def up_key_pressed(self, e):
        previous_cursor = self.text_editor_model.cursor_location.copy()
        self.text_editor_model.move_cursor_up()
        self.selection_handler(previous_cursor, 'start')

    def down_key_pressed(self, e):
        previous_cursor = self.text_editor_model.cursor_location.copy()
        self.text_editor_model.move_cursor_down()
        self.selection_handler(previous_cursor, 'end')

    def shift_key_pressed(self, e):
        self.shift_key = True
    
    def shift_key_released(self, e):
        self.shift_key = False

    def backspace_key_pressed(self, e):
        if self.has_active_selection:
            action = editActions.deleteSelectionAction(self.text_editor_model.cursor_location,
                                                       self.text_editor_model.selection_range,
                                                       self.text_editor_model)
            #self.text_editor_model.delete_selection()
            action.execute_do()
            self.undo_manager.push(action)
            self.has_active_selection = False
            self.text_editor_model.selection_range = None
            self.refresh_selection()
        else:
            action = editActions.deleteBeforeAction(self.text_editor_model.cursor_location,
                                                    self.text_editor_model)
            self.undo_manager.push(action)
            action.execute_do()
            #self.text_editor_model.delete_before()
    
    def del_key_pressed(self, e):
        self.text_editor_model.delete_after()
    
    def key_pressed(self, e):
        
        try:
            ord(e.char)
        except:
            print('sepcial key pressed')
            return
        '''
        print(e.char)
        self.text_editor_model.insert(e.char)'''

        action = editActions.InsertAction(self.text_editor_model.cursor_location, e.char, self.text_editor_model)
        action.execute_do()
        self.undo_manager.push(action)


    def ctrl_c_pressed(self, e):
        text = self.text_editor_model.get_selection_text()
        self.clipboard.push(text)

    def ctrl_v_pressed(self, e):
        text = self.clipboard.peek()
        action = editActions.InsertStringAction(self.text_editor_model.cursor_location, text, self.text_editor_model)
        action.execute_do()
        self.undo_manager.push(action)
        #self.text_editor_model.insert_string(text)

    def ctrl_x_pressed(self, e):
        if self.has_active_selection:
            self.ctrl_c_pressed(e)
            self.text_editor_model.delete_selection()
            self.has_active_selection = False
            self.text_editor_model.selection_range = None
            self.refresh_selection()

    def ctrl_z_pressed(self, e):
        self.undo_manager.undo()
        
        




def main():

    root = tkinter.Tk()
    tem = textEditorModel.TextEditorModel('1111\n2222\n3333')
    ex = TextEditor(tem)
    root.geometry("420x250+300+300")
    root.bind('<Left>', ex.left_key_pressed)
    root.bind('<Right>', ex.right_key_pressed)
    root.bind('<Up>', ex.up_key_pressed)
    root.bind('<Down>', ex.down_key_pressed)
    root.bind('<KeyPress-Shift_L>', ex.shift_key_pressed)
    root.bind('<KeyRelease-Shift_L>', ex.shift_key_released)
    root.bind('<BackSpace>', ex.backspace_key_pressed)
    root.bind('<Delete>', ex.del_key_pressed)
    root.bind('<Control-c>', ex.ctrl_c_pressed )
    root.bind('<Control-v>', ex.ctrl_v_pressed )
    root.bind('<Control-x>', ex.ctrl_x_pressed )
    root.bind('<Control-z>', ex.ctrl_z_pressed )

    root.bind('<Key>', ex.key_pressed)

    
    root.mainloop()


if __name__ == '__main__':
    main()
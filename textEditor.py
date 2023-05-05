import tkinter
import tkinter.font as tkfont
import textEditorModel

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

        tem.attach_cursor_observer(self)
        self.line_ids = []

        self.draw_ui()

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


    def notify_text(self):
        
        for line in self.line_ids:
            self.canvas.delete(line)

        self.draw_text()
        
    def refresh_text(self):
        pass

    def notify_cursor(self):
        self.refresh_cursor()
        for line in self.line_ids:
            self.canvas.delete(line)

    def refresh_cursor(self):
        canvas = self.canvas
        canvas.delete(self.cursor_id)
        self.draw_cursor()

    def refresh_selection(self):
        for rec in self.selection_ids:
            self.canvas.delete(rec)
        
        self.draw_selection()
        
    

    def selection_handler(self, previous_cursor):

        if self.shift_key:
            if self.has_active_selection:
                self.text_editor_model.selection_range.set_end(self.text_editor_model.cursor_location)

            else:
                self.has_active_selection = True
                self.text_editor_model.selection_range = textEditorModel.LocationRange(
                    previous_cursor, self.text_editor_model.cursor_location
                )
            
            self.refresh_selection()
        else:
            self.has_active_selection = False
            self.text_editor_model.selection_range = None
            self.refresh_selection()

    def left_key_pressed(self, e):
        previous_cursor = self.text_editor_model.cursor_location.copy()
        self.text_editor_model.move_cursor_left()
        self.selection_handler(previous_cursor)

    def right_key_pressed(self, e):
        previous_cursor = self.text_editor_model.cursor_location.copy()
        self.text_editor_model.move_cursor_right()
        self.selection_handler(previous_cursor)

    def up_key_pressed(self, e):
        previous_cursor = self.text_editor_model.cursor_location.copy()
        self.text_editor_model.move_cursor_up()
        self.selection_handler(previous_cursor)

    def down_key_pressed(self, e):
        previous_cursor = self.text_editor_model.cursor_location.copy()
        self.text_editor_model.move_cursor_down()
        self.selection_handler(previous_cursor)

    def shift_key_pressed(self, e):
        self.shift_key = True
    
    def shift_key_released(self, e):
        self.shift_key = False




def main():

    root = tkinter.Tk()
    tem = textEditorModel.TextEditorModel('ja sam pero.\nglup sam jako \nlol.')
    ex = TextEditor(tem)
    root.geometry("420x250+300+300")
    root.bind('<Left>', ex.left_key_pressed)
    root.bind('<Right>', ex.right_key_pressed)
    root.bind('<Up>', ex.up_key_pressed)
    root.bind('<Down>', ex.down_key_pressed)
    #root.bind('<Down>', ex.selection_handler_decorator(ex.down_key_pressed))
    root.bind('<KeyPress-Shift_L>', ex.shift_key_pressed)
    root.bind('<KeyRelease-Shift_L>', ex.shift_key_released)
    root.bind
    root.mainloop()


if __name__ == '__main__':
    main()
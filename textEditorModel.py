class Location:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def set_row(self, row):
        self.row = row

    def set_col(self, col):
        self.col = col

    def copy(self):
        return Location(self.row, self.col)
    
    def __eq__(self, o):
        if not isinstance(o, Location):
            return False
        return self.row == o.row and self.col == o.col
        


class LocationRange:
    def __init__(self, start, end):
        if end.row < start.row or end.row == start.row and end.col < start.col:
            start, end = end, start

        self.start = start
        self.end = end

    def set_start(self, start):
        if self.end.row < start.row or self.end.row == start.row and self.end.col < start.col:
            self.start = self.end
            self.end = start
        else:
            self.start = start

    def set_end(self, end):
        if end.row < self.start.row or end.row == self.start.row and end.col < self.start.col:
            
            self.end = self.start
            self.start = end
            print(self.start.row)
            print(self.end.row)
        else:
            self.end = end

class TextEditorModel:
    def __init__(self, initialText):
        self.lines = initialText.split('\n')
        self.selection_range = None
        self.cursor_location = Location(0,0)
        self.cursor_observes = []
        self.text_observers = []


    #-----------------------------iterator-------------------------------

    def allLines(self):
        return iter(self.lines)
    
    def linesRange(self, i1, i2):
        if i2 > len(self.lines):
            return self.allLines()
        
        return iter(self.lines[i1:i2])
    
    def get_current_line(self):
        return self.lines[self.cursor_location.row]


    #-------------------------cursor observers------------------------------
    def attach_cursor_observer(self, obs):
        self.cursor_observes.append(obs)

    def dettach_cursor_observer(self, obs):
        if obs in self.cursor_observes:
            self.cursor_observes.remove(obs)

    def notify_cursor_observers(self):
        for o in self.cursor_observes:
            o.notify_cursor()

    #--------------------------text observers--------------------------------

    def attach_text_observer(self, obs):
        self.text_observers.append(obs)

    def dettach_text_observer(self, obs):
        if obs in self.text_observes:
            self.text_observes.remove(obs)

    def notify_text_observers(self):
        for o in self.text_observers:
            o.notify_text()

    #------------------------cursor movement-----------------------------------------


    def move_cursor_left(self):
        if self.cursor_location.col > 0:
            self.cursor_location.col -= 1
            self.notify_cursor_observers()
        elif self.cursor_location.row > 0:
            self.cursor_location.row -= 1
            self.cursor_location.col = len(self.get_current_line())
            self.notify_cursor_observers() 
    
    def move_cursor_right(self):
        if self.cursor_location.col < len(self.get_current_line()):
            self.cursor_location.col += 1
            self.notify_cursor_observers()
        elif self.cursor_location.row < len(self.lines) - 1:
            self.cursor_location.row += 1
            self.cursor_location.col = 0

    def move_cursor_up(self):
        if self.cursor_location.row > 0:
            self.cursor_location.row -= 1
            self.notify_cursor_observers()

    def move_cursor_down(self):
        if self.cursor_location.row < len(self.lines) -1:
            self.cursor_location.row += 1
            self.notify_cursor_observers()

    #----------------------------------deletion---------------------------

    def delete_before(self):
        if self.cursor_location.col == 0:
            if self.cursor_location.row == 0:
                return #don't delete if at the start of the document 
            else:
                line = self.get_current_line()
                row = self.cursor_location.row
                new_cursor_col = len(self.lines[row-1])
                self.lines[self.cursor_location.row - 1] += line
                del self.lines[self.cursor_location.row]
                self.cursor_location = Location(row - 1, new_cursor_col)
                self.notify_cursor_observers()
                self.notify_text_observers()


            return
        
        line = self.get_current_line() 
        index = self.cursor_location.col - 1
        line = line[: index] + line[index+1 :]

        row = self.cursor_location.row

        self.lines[row] = line
        self.move_cursor_left()

        self.notify_text_observers()

    def delete_after(self):
        line = self.get_current_line()
        if self.cursor_location.col == len(line) - 1:
            return #don't delete if at the end of the row
        
        index = self.cursor_location.col
        line = line[: index] + line[index+1 :]

        row = self.cursor_location.row

        self.lines[row] = line

        self.notify_text_observers()

    def delete_selection(self):
        start_row = self.selection_range.start.row
        start_col = self.selection_range.start.col

        end_row = self.selection_range.end.row
        end_col = self.selection_range.end.col

        if start_row == end_row:
            line = self.get_current_line()

            self.lines[start_row] = line[:start_col] + line[end_col :]

        else:
            start_line = self.lines[start_row]
            end_line = self.lines[end_row]

            self.lines[start_row] = start_line[: start_col] + end_line[end_col :]

            self.lines[end_row] = end_line[end_col : ]

            self.lines = self.lines[:start_row + 1] + self.lines[end_row + 1 :]

        self.cursor_location.row = start_row
        self.cursor_location.col = start_col

        

        self.notify_cursor_observers()
        self.notify_text_observers()
    

    #-----------------------------insert operations----------------------------------------


    def insert(self, c):
            
            
        line = self.get_current_line()
        row = self.cursor_location.row
        col = self.cursor_location.col 

        
        
        if ord(c) == 13 or c == '\n':
            
            line_old = line[:col]
            line_new = line[col:]

            self.lines.insert(row + 1, line_new)
            self.lines[row] = line_old

            self.cursor_location = Location(row + 1, 0)
            

            print(self.lines)



        else:


            self.lines[row] = line[: col] + c + line[col:]
            self.move_cursor_right()


        self.notify_text_observers()

    def insert_string(self, s):
        new_lines = s.split('\n')

        current_row = self.cursor_location.row
        current_col = self.cursor_location.col
        
        #handles first line
        current_line = self.get_current_line()
        if len(new_lines) == 1:
            self.lines[current_row] = current_line[: current_col] + new_lines[0] + current_line[current_col :]
            self.cursor_location.col += len(new_lines[0])

        else: 
            if current_row < len(self.lines) - 1:
                self.lines[current_row] = current_line[: current_col] + new_lines[0]
                new_lines[-1] += current_line[current_col :]
                next_row = current_row + 1
                #next_line = self.lines[next_row]
                #self.lines[next_row] = new_lines[-1]
                self.lines = self.lines[: next_row] + new_lines[1 : len(new_lines)] + self.lines[next_row :]
            else:
                new_lines[-1] += current_line[current_col :]
                self.lines[current_row] = self.lines[current_row][:current_col] + new_lines[0]
                self.lines.extend(new_lines[1:])

            self.cursor_location.row = current_row + len(new_lines) - 1
            self.cursor_location.col = len(new_lines[-1]) - len(current_line[current_col :])
        


        self.notify_cursor_observers()
        self.notify_text_observers()

#---------------------------getter methods--------------------------

    def get_selection_coords(self):
        start_row = self.selection_range.start.row
        start_col = self.selection_range.start.col

        end_row = self.selection_range.end.row
        end_col = self.selection_range.end.col

        return start_row, start_col, end_row, end_col

    def get_selection_text(self):
        if self.selection_range == None:
            return ''
        
        start_row, start_col, end_row, end_col = self.get_selection_coords()

        if start_row == end_row:
            return self.lines[start_row][start_col : end_col]
        else:
            first_line = self.lines[start_row][start_col : ]
            last_line = self.lines[end_row][: end_col]

            lines = self.lines[start_row + 1: end_row - 1]

            return '\n'.join([first_line] + lines + [last_line])
        
    def get_char_before(self):
        if self.cursor_location.col == 0:
            return '\n'
        return self.lines[self.cursor_location.row][self.cursor_location.col]

            

        

        

        



    

            

        

    

    


    
        
        
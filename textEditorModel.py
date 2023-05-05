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
        for o in self.text_observes:
            o.notify_text()

    #------------------------cursor movement-----------------------------------------


    def move_cursor_left(self):
        if self.cursor_location.col > 0:
            self.cursor_location.col -= 1
            self.notify_cursor_observers()
    
    def move_cursor_right(self):
        if self.cursor_location.col < len(self.get_current_line()):
            self.cursor_location.col += 1
            self.notify_cursor_observers()

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
            return #don't delete if at the start of the row
        
        line = self.get_current_line()
        index = self.cursor_location.col
        line = line[: index] + line[index+1 :]

        row = self.cursor_location.row

        self.lines[row] = line

        self.notify_text_observers()

    def delete_after(self):
        line = self.get_current_line()
        if self.cursor_location.col == len(line) - 1:
            return #don't delete if at the end of the row
        
        index = self.cursor_location.col + 1
        line = line[: index] + line[index+1 :]

        row = self.cursor_location.row

        self.lines[row] = line

        self.notify_text_observers()

    

    


    
        
        
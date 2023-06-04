
import tkinter
import textEditorModel
import textEditor
import os
import importlib.util
from functools import partial

def find_plugins():
    plugins = []
    current_directory = os.getcwd()

# Iterate over all files in the directory
    for root, dirs, files in os.walk(current_directory):
        for file in files:
            if file.endswith('Plugin.py'):
                file_full = os.path.join(root, file)
                spec = importlib.util.spec_from_file_location('file', file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                plugins.append(module.Plugin())
    
    return plugins


class MenuBar(tkinter.Menu):
    def __init__(self, parent, editor):
        super().__init__(parent)
        self.file_menu = FileMenu(self)
        self.edit_menu = EditMenu(self, editor)
        self.move_menu = MoveMenu(self)
        self.plugin_menu = PluginMenu(self, editor)
        editor.attach_selection_observer(self.edit_menu)
        editor.undo_manager.attach_undo_observer(self.edit_menu)
        editor.undo_manager.attach_redo_observer(self.edit_menu)
        editor.clipboard.attach_clipboard_observer(self.edit_menu)
        self.add_cascade(label="File", menu=self.file_menu)
        self.add_cascade(label="Edit", menu=self.edit_menu)
        self.add_cascade(label="Move", menu=self.move_menu)
        self.add_cascade(label='Plugin', menu=self.plugin_menu)
    

class PluginMenu(tkinter.Menu):
    def __init__(self, parent, editor):
        super().__init__(parent)
        self.tem = editor.text_editor_model

        for plugin in find_plugins():
            action_with_arg = partial(plugin.execute, self.tem)
            self.add_command(label=plugin.get_name(), command=action_with_arg)





class FileMenu(tkinter.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_command(label='Open')
        self.add_command(label='Save')
        self.add_command(label='Exit')

class EditMenu(tkinter.Menu):
    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor
        self.add_command(label='Undo', command=self._undo)
        self.add_command(label='Redo', command=self._redo)
        self.add_command(label='Cut', command=self._cut)
        self.add_command(label='Copy', command=self._copy)
        self.add_command(label='Paste', command=self._paste)
        self.add_command(label='Paste and Take')
        self.add_command(label='Delete selection')
        self.add_command(label='Clear document')

        self.entryconfig(1, state = tkinter.DISABLED)
        self.entryconfig(2, state = tkinter.DISABLED)
        self.entryconfig(3, state = tkinter.DISABLED)
        self.entryconfig(4, state = tkinter.DISABLED)
        self.entryconfig(5, state = tkinter.DISABLED)
        self.entryconfig(6, state = tkinter.DISABLED)
        self.entryconfig(7, state = tkinter.DISABLED)

    def update_selection(self, status):
        state = tkinter.NORMAL if status else tkinter.DISABLED

        self.entryconfig(3, state = state)
        self.entryconfig(4, state = state)
        #self.entryconfig(5, state = state)

    def update_undo(self, status):
        state = tkinter.NORMAL if status else tkinter.DISABLED
        self.entryconfig(1, state = state)

    def update_redo(self, status):
        state = tkinter.NORMAL if status else tkinter.DISABLED
        self.entryconfig(2, state = state)
    
    def update_clipboard(self, status):
        state = tkinter.NORMAL if status else tkinter.DISABLED
        self.entryconfig(5, state = state)





    def _undo(self):
        print('undo menu')
        self.editor.ctrl_z_pressed('z')
    def _redo(self):
        self.editor.ctrl_y_pressed('y')
    def _cut(self):
        self.editor.ctrl_x_pressed('x')
    def _copy(self):
        self.editor.ctrl_c_pressed('c')
    def _paste(self):
        self.editor.ctrl_v_pressed('v')
    def _delete_selection(self):
        self.editor

class MoveMenu(tkinter.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_command(label='Cursor to document start')
        self.add_command(label='Cursor to document end')


if __name__ == '__main__':
    root = tkinter.Tk()
    menubar = MenuBar(root)
    file_menu = FileMenu(menubar)
    edit_menu = EditMenu(menubar)
    move_menu = MoveMenu(menubar)
    menubar.add_cascade(label="File", menu=file_menu)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    menubar.add_cascade(label="Move", menu=move_menu)


    root.config(menu=menubar)
    root.mainloop()
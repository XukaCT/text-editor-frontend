from tkinter import *
from tkinter import filedialog, messagebox
import funtion101 as fn
from tkinter.simpledialog import askstring
import requests


class TextEditor:

    def __init__(self, root, file_path=None):
        self.root = root

        self.create_menu()

        self.text_area = Text(root, wrap="word", undo=False, font=("Consolas", 12))
        self.text_area.pack(expand=True, fill="both")
        self.text_area.bind("<Key>", lambda event: fn.on_key(event, self.text_area))

        self.file_path = file_path
        

    def create_menu(self):
        menu_bar = Menu(self.root)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=lambda: self.save_file())
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)

        self.root.config(menu=menu_bar)

    def save_file(self):
        content = self.text_area.get("1.0", "end-1c")
        filename = askstring("Save File", "Enter filename (e.g. note.txt):")
        if not filename:
            return
        res = requests.post("https://text-editor-frontend-ldxl.onrender.com/save", json={
            "filename": filename,
            "content": content
        })

    def open_file(self):
        filename = askstring("Open File", "Enter filename (e.g. note.txt):")
        if not filename:
            return
        res = requests.get(f"https://text-editor-frontend-ldxl.onrender.com/open/{filename}")
        if res.ok:
            data = res.json()
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", data["content"])
            
            
    def undo(self):
        try:
            fn.undo(self.text_area)
        except Exception:
            pass
    
    def redo(self):
        try:
            fn.redo(self.text_area)
        except Exception:
            pass

if __name__ == "__main__":
    root = Tk()
    root.title("Tkinter Text Editor")
    root.geometry("800x600")
    app = TextEditor(root)
    root.mainloop()
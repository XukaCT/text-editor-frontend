import tkinter as tk
from tkinter import filedialog

# === Globals ===
edit_history = []
redo_stack = []

edit_buffer = ""
delete_buffer = ""
edit_start_index = None
delete_start_index = None
tracking_enabled = True
undo_used = False

# Word boundaries (used to trigger commits)
word_boundaries = {" ", ".", ",", "!", "?", "\n"}

# === Commit Functions ===

def commit_buffer():
    global edit_buffer, edit_start_index
    if edit_buffer:
        edit_history.append({
            "type": "insert",
            "index": edit_start_index,
            "text": edit_buffer
        })
        redo_stack.clear()
        edit_buffer = ""
        edit_start_index = None

def delete_buffer_content():
    global delete_buffer, delete_start_index
    if delete_buffer:
        edit_history.append({
            "type": "delete",
            "index": delete_start_index,
            "text": delete_buffer
        })
        redo_stack.clear()
        delete_buffer = ""
        delete_start_index = None

# === Key Press Handler ===

def on_key(event, text_widget):
    global edit_buffer, delete_buffer, edit_start_index, delete_start_index
    global tracking_enabled, undo_used

    if not tracking_enabled:
        return

    # Clear state if undo was just used
    if undo_used:
        redo_stack.clear()
        undo_used = False
        edit_buffer = ""
        delete_buffer = ""
        edit_start_index = None
        delete_start_index = None

    cursor = text_widget.index("insert")

    # Handle deletion buffer when switching from delete to insert
    if event.keysym != "BackSpace":
        delete_buffer_content()

    # --- Handle Paste (Ctrl+V) ---
    if event.state & 0x4 and event.keysym.lower() == "v":
        try:
            pasted = text_widget.clipboard_get()
            if pasted:
                edit_history.append({
                    "type": "insert",
                    "index": cursor,
                    "text": pasted
                })
                redo_stack.clear()
        except tk.TclError:
            pass
        return

    # --- Handle Bulk Delete (selection + Backspace/Delete) ---
    if event.keysym in ("BackSpace", "Delete"):
        try:
            sel_start = text_widget.index("sel.first")
            sel_end = text_widget.index("sel.last")
            deleted_text = text_widget.get(sel_start, sel_end)
            edit_history.append({
                "type": "delete",
                "index": sel_start,
                "text": deleted_text
            })
            redo_stack.clear()
        except tk.TclError:
            # Normal backspace (no selection)
            if event.keysym == "BackSpace":
                commit_buffer()
                if not delete_buffer:
                    delete_start_index = text_widget.index(f"{cursor} -1c")
                else:
                    delete_start_index = text_widget.index(f"{delete_start_index} -1c")
                deleted_char = text_widget.get(f"{cursor} -1c", cursor)
                delete_buffer = deleted_char + delete_buffer

    # --- Handle Typing ---
    if len(event.char) == 1 and event.char.isprintable():
        if not edit_buffer:
            edit_start_index = cursor
        edit_buffer += event.char
        if event.char in word_boundaries:
            commit_buffer()

# === Undo / Redo ===

def undo(text_widget=None):
    global tracking_enabled, undo_used

    commit_buffer()
    delete_buffer_content()

    if not edit_history:
        return

    tracking_enabled = False

    op = edit_history.pop()
    redo_stack.append(op)
    undo_used = True

    if op["type"] == "insert":
        text_widget.delete(op["index"], f"{op['index']} + {len(op['text'])}c")
    elif op["type"] == "delete":
        text_widget.insert(op["index"], op["text"])

    tracking_enabled = True

def redo(text_widget=None):
    global tracking_enabled, undo_used
    global edit_buffer, delete_buffer, edit_start_index, delete_start_index

    if not redo_stack:
        return

    commit_buffer()
    delete_buffer_content()

    tracking_enabled = False
    undo_used = False

    op = redo_stack.pop()
    edit_history.append(op)

    if op["type"] == "insert":
        text_widget.insert(op["index"], op["text"])
    elif op["type"] == "delete":
        text_widget.delete(op["index"], f"{op['index']} + {len(op['text'])}c")

    tracking_enabled = True

def save(text_widget, file_path):

    if not file_path:
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt"),
                                                                ("Python files", "*.py"),
                                                                ("HTML files", "*.html"),
                                                                ("All files", ".*")])
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_widget.get("1.0", tk.END))    
            file.close()
    else:
        return


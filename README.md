# Simple note-taking app using Python Tinkter on a local host
This app is an implementation of my knowledge in data structures and algorithms. In the app, all functions such as undo, redo, copy, or paste words with an open and save file are coded from scratch through tkinter.

## Instruction 
Download both files and run main.py file only

## More details about the project 
Table index and Stack are implemented to create the undo and redo functions. Every time we press the key which contains `{" ", ".", ",", "!", "?", "\n"}` we consider that as a word and record it down (type, word position from start to end, and content) into an array `edit_history = []`.
So whenever we hit undo, we .pop() from `edit_history = []` to redo (delete if type is insert and vice versa) and move it to `redo_stack = []` for future redo. However, the `redo_stack = []` is reset as a new record is added into `edit_history = []`.




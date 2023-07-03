import tkinter as tk
from tkinter import ttk, Text, Frame
from zoltar_data import zoltar_data
from local_lib import text_box_text, fix_spelling, fix_grammar_spelling

def correct_spelling_button_press(text_box:Text):
    text_data = text_box_text(text_box)
    text_data = fix_spelling(text_data)
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, text_data)

def correct_grammar_spelling_button_press(text_box:Text):
    text_data = text_box.get("1.0", tk.END)
    text_data = fix_grammar_spelling(text_data)
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, text_data)

def undo_typing(textbox:Text):
    try:
        textbox.edit_undo()
    except:
        pass

def redo_typing(textbox:Text):
    try:
        textbox.edit_redo()
    except:
        pass

def Add_Tab(notebook:ttk.Notebook, label:str, text_data:str=""):
    new_tab = tk.Frame(notebook)
    notebook.add(new_tab, text=label)
    notebook.select(new_tab)
    # Add a multiline text box to the new_tab
    text_box = tk.Text(new_tab, background='Dark Slate Gray',foreground='Light Green',undo=True)
    if text_data:
        text_box.insert('1.0', text_data)
    text_box.bind('<Control-z>', func = lambda event: undo_typing(text_box))
    text_box.bind('<Control-y>', func = lambda event: redo_typing(text_box))    
    text_box.config(insertbackground='cyan')
    text_box.pack(fill=tk.BOTH, expand=1)
    text_box.focus_set()
    # Add a button labeled "Correct Spelling"
    button_frame = tk.Frame(new_tab)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    # Add a button labeled "Correct Spelling" at the bottom underneath the text box
    correct_spelling_button = tk.Button(button_frame, text="Correct Spelling", command=lambda: correct_spelling_button_press(text_box))
    correct_spelling_button.pack(side=tk.RIGHT, padx=5)
    # Add a button labeled "Correct Grammar" to the left of the correct_spelling_button
    correct_grammar_spelling_button = tk.Button(button_frame, text="Correct Grammar", command=lambda: correct_grammar_spelling_button_press(text_box))
    correct_grammar_spelling_button.pack(side=tk.RIGHT, padx=5)
    persist(notebook)

def get_first_text_widget(tab:Frame):
    for widget in tab.winfo_children():
        if isinstance(widget, tk.Text):
            return widget
    return None

def persist(notebook: ttk.Notebook):
    if 'Notes' not in zoltar_data: 
        zoltar_data['Notes'] = {}
    for tab_id in notebook.tabs():
        tab = notebook.nametowidget(tab_id)  # Convert tab ID to widget
        tab_name = notebook.tab(tab, "text")
        txt_bx = get_first_text_widget(tab)
        text = text_box_text(txt_bx)
        zoltar_data['Notes'][tab_name] = text

def main():
    root = tk.Tk()
    root.state('zoomed')
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=1)
    Add_Tab(notebook, 'Test')
    root.mainloop()

if __name__ == "__main__":
    main()

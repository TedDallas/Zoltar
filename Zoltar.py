import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from datetime import datetime
import time
import json
# -- local modules -----------
from  zoltar_data import zoltar_data
from zoltar_note import persist, Add_Tab

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -- Events ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def on_new_note():
    root.config(cursor='watch')
    # Check if "Notes" node exists
    if not treeview.exists('Notes'):
        # Add "Notes" node to the treeview
        treeview.insert('', 'end', 'Notes', text='Notes')
    # Add "Note" node under the "Notes" node
    tab_label = 'Note - ['+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"]"
    if tab_label in tree_nodes:
        time.sleep(1)
        tab_label = 'Note - ['+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"]"
    tree_nodes[tab_label] = treeview.insert('Notes', 'end', text=tab_label)
    Add_Tab(notebook,tab_label)
    root.config(cursor='')

def on_save_all():
    try:
        root.config(cursor='watch')
        save_workspace()
    except:
        pass
    finally:
        if root != None:
            root.config(cursor='')

#remove the notebook tab
def on_delete_tab():
    root.config(cursor='watch')
    current_tab = notebook.select()
    if current_tab is not None:
        # Get the tab label
        tab_label = notebook.tab(current_tab, "text")
        # Remove the notebook tab
        notebook.forget(current_tab)        
        # Remove the treeview node with the same label
        treeview.delete(tree_nodes[tab_label])
        del(tree_nodes[tab_label])
    root.config(cursor='')

#when quiting make sure we 
def on_exit():
    try:
        root.config(cursor='watch')
        save_workspace()
        root.config(cursor='')
    except:
        pass
    finally:
        if root != None:
            root.destroy()

# show About dialog
def on_about():
    messagebox.showinfo("About", "Zoltar is a cool productivity tool written by Edward Wayne Johnson.")

# Double click on treeview node, this changes the active tab
def on_double_click(event):
    item = treeview.selection()[0]
    tab_label = treeview.item(item,"text")
    for i in range(notebook.index('end')):
        if notebook.tab(i, 'text') == tab_label:
            notebook.select(i)
            return
    raise ValueError(f"No tab named {tab_label}")

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -- Local Functions  -----------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#save the local workspace to a JSON file
def save_workspace(filename="Zoltar.json"):
    persist(notebook)
    with open(filename, 'w') as f:
        json.dump(zoltar_data, f, indent=4)

#load the local workspace from a JSON file
def load_workspace(filename="Zoltar.json", zdata=dict):
    if os.path.isfile(filename):
        #load dict from JSON file
        zdata = None
        with open(filename) as f:
            zdata = json.load(f)
        #clear all tabs
        for tab in notebook.tabs():
            notebook.forget(tab)
        #load all tabs from dict
        with open(filename) as f:
            zdata = json.load(f)
        #Add "Notes" node to the treeview
        if not treeview.exists('Notes'):
            treeview.insert('', 'end', 'Notes', text='Notes')
        #Add tabs with data
        notes = zdata['Notes']
        for tab_label in notes.keys():
            tree_nodes[tab_label] = treeview.insert('Notes', 'end', text=tab_label)
            Add_Tab(notebook=notebook,label=tab_label, text_data=notes[tab_label])

#display treeview popup menu
def do_treeview_popup(event):
    popup.tk_popup(event.x_root, event.y_root, 0)

#remove selected tab and treeview node
def delete_tab_and_data():
    selected_item_id = treeview.selection()[0]  # get selected item's ID
    selected_item = treeview.item(selected_item_id)  # get selected item's values
    node_label = selected_item['text']
    if node_label not in treview_node_parents: #checks to make sure we are not trying to delete any parent nodes! NO!NO!NO!NO!
        delete_node = messagebox.askyesno('DELETE FOREVER', 'Delete tab and data for - "'+node_label+'" ?')
        if delete_node:
            selected_item_id = treeview.selection()[0]
            for i in range(notebook.index('end')):
                if notebook.tab(i, 'text') == node_label:
                    del(zoltar_data['Notes'][node_label]) #remove data
                    notebook.forget(i) #remove tab
                    treeview.delete(selected_item_id) #remove treeview node
                    return

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -- Object Initializations -----------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
tree_nodes = {} # stores the treeview nodes 
treview_node_parents = ["Notes"]

my_theme = 'equilux'

# Create the main window
root = ThemedTk(theme=my_theme)
root.title("~ZOLTAR~")
root.geometry("1920x1080")
root.state("zoomed")
root.protocol("WM_DELETE_WINDOW", on_exit)

# Set the window icon
root.iconbitmap("Wizard.ico")

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a file menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New Note", command=on_new_note, compound=tk.LEFT)
file_menu.add_command(label="Save", command=on_save_all, accelerator="Ctrl+S")
file_menu.add_command(label="Delete Tab", command=on_delete_tab)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_exit)

# Create a help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=on_about)

# Create a PanedWindow widget
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=1)

# Create the left panel
# left_panel = tk.Frame(paned_window, width=350)
# paned_window.add(left_panel)

# Create the left panel
left_panel = tk.Frame(paned_window)
paned_window.add(left_panel)
paned_window.paneconfigure(left_panel, minsize=350)

# Add a treeview to the left panel
treeview = ttk.Treeview(left_panel)
treeview.pack(fill=tk.BOTH, expand=1)
treeview.bind("<Double-1>", on_double_click)

#Add popup menu to treeview
popup = tk.Menu(root, tearoff=0)
popup.add_command(label="Delete", command=lambda: delete_tab_and_data())
popup.add_command(label="Edit Name", command=lambda: print("Edit"))
treeview.bind("<Button-3>", do_treeview_popup)
treeview.pack()

# Create the right panel
right_panel = tk.Frame(paned_window)
paned_window.add(right_panel)

# Create a Notebook widget inside the right panel
notebook = ttk.Notebook(right_panel)
notebook.pack(fill=tk.BOTH, expand=1)

# Load workspace from JSON file
load_workspace(filename="Zoltar.json", zdata=zoltar_data)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -- Main -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    root.mainloop()

if __name__ == "__main__":
    main()

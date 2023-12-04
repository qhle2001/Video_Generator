import tkinter as tk
from tkinter import ttk
import os

def show_files_and_folders():
    folder_path = folder_path_entry.get()
    folder_path = r"C:\Users\DELL\OneDrive\Documents\Intern\VideoGen"

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        file_list.delete(0, tk.END)  # Clear existing entries

        # Get a list of files and folders in the specified directory
        entries = os.listdir(folder_path)

        # Display files and folders in the listbox
        for entry in entries:
            file_list.insert(tk.END, entry)

            # Bind the double-click event to the list item
            file_list.bind('<Double-1>', on_item_double_click)

def on_item_double_click(event):
    selected_item = file_list.get(file_list.curselection())
    selected_path = os.path.join(folder_path_entry.get(), selected_item)

    if os.path.isdir(selected_path):
        # If the selected item is a directory, show its files and folders
        show_files_in_folder(selected_path)

def show_files_in_folder(folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        file_list.delete(0, tk.END)  # Clear existing entries

        # Get a list of files and folders in the specified directory
        entries = os.listdir(folder_path)

        # Display files and folders in the listbox
        for entry in entries:
            file_list.insert(tk.END, entry)

# Create the main window
root = tk.Tk()
root.title("File Explorer")

# Create UI elements
folder_path_label = tk.Label(root, text="Folder Path:")
folder_path_entry = tk.Entry(root, width=40)
show_button = tk.Button(root, text="Show Files and Folders", command=show_files_and_folders)
file_list = tk.Listbox(root, selectmode=tk.SINGLE, width=50, height=15)
scrollbar = tk.Scrollbar(root, command=file_list.yview)
file_list.configure(yscrollcommand=scrollbar.set)

# Place UI elements in the window
folder_path_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")
folder_path_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w")
show_button.grid(row=0, column=2, pady=5, padx=10, sticky="w")
file_list.grid(row=1, column=0, columnspan=3, pady=5, padx=10, sticky="w")
scrollbar.grid(row=1, column=3, pady=5, sticky="ns")

# Start the GUI event loop
root.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import subprocess
import threading
import time
import sys
import os

class Tab1Content:
    def __init__(self, notebook, root):
        self.root = root
        self.frame = ttk.Frame(notebook)
        # tab_font = ("Arial", 12)
        notebook.add(self.frame, text="Script Generation")

        # Place your code from tab 1 here
        frame = tk.Frame(self.frame)
        frame.pack(pady=10)

        self.entry = tk.Entry(frame, width=50)
        self.entry.pack(side=tk.LEFT, padx=10)

        self.button_run = tk.Button(frame, text="Run", command=self.run_script)
        self.button_run.pack(side=tk.LEFT, padx=10)

        self.button_edit = tk.Button(frame, text="Edit", command=self.edit_script)
        self.button_edit.pack(side=tk.LEFT, padx=10)
        self.button_edit.pack_forget()

        # self.button_save = tk.Button(self.frame, text="Save", command=self.save_text)
        # self.button_save.pack_forget()

        self.output_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=100, height=20)
        self.output_text.pack(pady=10, padx=10, expand=True, fill="both")

        self.progressbar = ttk.Progressbar(self.frame, mode='determinate', length=200)
        self.progressbar.pack(pady=10)

    def run_script(self):
        # Clear the previous output
        self.button_edit.pack_forget()  # Ẩn button "Edit"
        self.output_text.delete(1.0, tk.END)

        # Get the text from the Entry widget
        text_to_pass = self.entry.get()

        # Run scriptgen.py in a separate thread
        threading.Thread(target=self.run_scriptgen, args=(text_to_pass,), daemon=True).start()

    def edit_script(self):
        # Get the content of the generated file

        generated_file_path = "./results/generated_text.txt"
        with open(generated_file_path, "r", encoding='utf-8') as file:
            file_content = file.read()

        # Create a new window to display the content
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Generated Script")

        # Create a text widget to display the content
        edit_text = tk.Text(edit_window, wrap=tk.WORD, width=100, height=30)
        edit_text.pack(pady=10, padx=10, expand=True, fill="both")

        # Insert the content into the text widget
        edit_text.insert(tk.END, file_content)

        # Add button "Save"
        save_button = tk.Button(edit_window, text="Save", command=lambda: self.save_text(edit_text, edit_window))
        save_button.pack(pady=10, padx=20, ipadx=10, ipady=5)

    def save_text(self, edit_text, window):
        # Lấy nội dung từ Text widget
        text_content = edit_text.get("1.0", tk.END)

        with open("results/generated_text.txt", "w", encoding='utf-8') as file:
            file.write(text_content.strip())

        window.destroy()

    def run_scriptgen(self, text_to_pass):

        self.button_run.configure(state="disabled")
        # Configure progressbar
        self.progressbar['value'] = 0
        self.progressbar['maximum'] = 100

        # Start the progressbar
        self.progressbar.start()

        # Run scriptgen.py with the text as a command line argument
        process = subprocess.Popen(["python", "ScriptGen.py", text_to_pass], stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)

        # Update the GUI in real-time with the output
        while True:
            line = process.stdout.readline()
            if not line:
                break
            self.output_text.insert(tk.END, line)
            self.output_text.yview(tk.END)

            # Update progressbar based on the number of lines read
            progress_value = min((len(line) / 100) * 100, 100)
            self.progressbar['value'] = progress_value
            self.root.update_idletasks()

            # Flush stdout to ensure real-time updates
            sys.stdout.flush()

            # Pause for a short time to provide smoother progress updates
            time.sleep(0.1)

        # Wait for the process to finish and get the return code
        return_code = process.wait()

        # Optionally, you can check the return code and handle it as needed
        print("Scriptgen process finished with return code:", return_code)

        # Stop the progressbar
        self.progressbar.stop()

        # Ensure the progressbar shows 100% after the process finishes
        self.progressbar['value'] = 100

        # Display the "Edit" button after the script has finished running
        self.button_run.configure(state="normal")
        self.button_edit.pack()
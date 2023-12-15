import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import subprocess
import threading
import time
import sys

class AudioImage:
    def __init__(self, notebook, root):
        self.root = root
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Audio&Image Generation")

        # Place your code from tab 1 here
        frame = tk.Frame(self.frame)
        frame.pack(pady=10)

        self.button_run = tk.Button(frame, text="Run", command=self.run_script)
        self.button_run.pack(side=tk.LEFT, padx=10)

        self.button_delete = tk.Button(frame, text="Delete", command=self.delete_script)
        self.button_delete.pack(side=tk.LEFT, padx=10)

        self.output_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=100, height=20)
        self.output_text.pack(pady=10, padx=10, expand=True, fill="both")

        self.progressbar = ttk.Progressbar(self.frame, mode='determinate', length=200)
        self.progressbar.pack(pady=10)

    def run_script(self):
        # Clear the previous output
        self.output_text.delete(1.0, tk.END)

        # Run scriptgen.py in a separate thread
        threading.Thread(target=self.run_scriptgen, args=("edit",), daemon=True).start()

    def delete_script(self):
        # Clear the previous output
        self.output_text.delete(1.0, tk.END)

        # Run scriptgen.py in a separate thread
        threading.Thread(target=self.run_scriptgen, args=("delete",), daemon=True).start()
    def run_scriptgen(self, string):
        self.button_run.configure(state="disabled")
        self.button_delete.configure(state="disabled")
        # Configure progressbar
        self.progressbar['value'] = 0
        self.progressbar['maximum'] = 100

        # Start the progressbar
        process = None
        self.progressbar.start()

        # Run scriptgen.py without the text argument
        if string == "edit":
            process = subprocess.Popen(["python", "GenAudioImage.py"], stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        elif string == "delete":
            process = subprocess.Popen(["python", "removefile.py"], stdout=subprocess.PIPE,
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

        self.button_run.configure(state="normal")
        self.button_delete.configure(state="normal")


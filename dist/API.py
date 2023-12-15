import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import scrolledtext
import subprocess
import threading
import time
import sys
from VideoDisplay import WindowsMediaPlayer
import shutil

class API:
    def __init__(self, notebook, root):
        self.root = root
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="API KEY")

        # Place your code from tab 1 here
        frame = tk.Frame(self.frame)
        frame.pack(pady=10)

        frame_button = tk.Frame(self.frame)
        frame_button.pack(side=tk.TOP)

        self.entry = tk.Entry(frame_button, width=50)
        self.entry.pack(side=tk.LEFT, padx=10)

        self.button_save = tk.Button(frame_button, text="Save", command=self.save_text)
        self.button_save.pack(side=tk.RIGHT, padx=10)

        self.output_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=100, height=20)
        self.output_text.pack(pady=10, padx=10, expand=True, fill="both")

    def save_text(self):
        # Lấy nội dung từ Text widget
        text_content = self.entry.get()

        with open("./API_KEY.txt", "w", encoding='utf-8') as file:
            file.write(text_content.strip())

        self.output_text.insert(tk.END, f"Save key successful: {text_content}")
        self.root.update_idletasks()
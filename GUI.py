import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import subprocess
import threading
import time
import sys
import os
from tab1scriptgen import Tab1Content
from tab2AudioImageGen import AudioImage
from tab3VideoGen import Video
from tab4Caption import Caption
from API import API

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Generator")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Create tabs
        self.tab1 = Tab1Content(self.notebook, root)
        self.tab2 = AudioImage(self.notebook, root)
        self.tab3 = Video(self.notebook, root)
        self.tab4 = Caption(self.notebook, root)
        self.tab5 = API(self.notebook, root)

        # Add tabs to the notebook
        self.notebook.add(self.tab1.frame, text="Script Generation")
        self.notebook.add(self.tab2.frame, text="Audio&Image Generation")
        self.notebook.add(self.tab3.frame, text="Video Generation")
        self.notebook.add(self.tab4.frame, text="Subtitles Creation")
        self.notebook.add(self.tab5.frame, text = "API KEY")

        # Bind the notebook tab changed event
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_changed)

    def tab_changed(self, event):
        current_tab = event.widget.tab(event.widget.select(), "text")
        if current_tab == "Video Generation":
            # Reload images in the Video tab
            self.tab3.load_images()
            self.tab3.display_first_image()
            self.tab3.load_first_audio()



if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()

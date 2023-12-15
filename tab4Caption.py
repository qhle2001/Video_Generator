import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import scrolledtext
import subprocess
import threading
import time
import sys
from VideoDisplay import WindowsMediaPlayer
import shutil

class Caption:
    def __init__(self, notebook, root):
        self.root = root
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Subtitles Creation")

        # Place your code from tab 1 here
        frame = tk.Frame(self.frame)
        frame.pack(pady=10)

        frame_button = tk.Frame(self.frame)
        frame_button.pack()

        self.button_run = tk.Button(frame_button, text="Run", command=self.run_script)
        self.button_run.pack(side=tk.LEFT, padx=10)

        self.button_download = tk.Button(frame_button, text="Download", command=self.download_video)
        self.button_download.pack(side=tk.RIGHT)
        self.button_download.pack_forget()

        self.output_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=100, height=20)
        self.output_text.pack(pady=10, padx=10, expand=True, fill="both")

        self.progressbar = ttk.Progressbar(self.frame, mode='determinate', length=200)
        self.progressbar.pack(pady=10)

    def run_script(self):
        # Clear the previous output
        self.button_download.pack_forget()
        self.output_text.delete(1.0, tk.END)

        # Run scriptgen.py in a separate thread
        threading.Thread(target=self.run_scriptgen, daemon=True).start()

    def run_scriptgen(self):
        # Configure progressbar
        self.button_run.configure(state="disabled")
        displaying_video = True
        self.progressbar['value'] = 0
        self.progressbar['maximum'] = 100

        # Start the progressbar
        self.progressbar.start()

        # Run scriptgen.py without the text argument
        process = subprocess.Popen(["python", "Subtitles.py"], stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=False, bufsize=-1)

        # Update the GUI in real-time with the output
        while True:
            line = process.stdout.readline()
            if not line:
                break
            decoded_line = line.decode('utf-8', errors='replace')
            self.output_text.insert(tk.END, decoded_line)
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

        self.button_download.pack()

        # If video is being displayed, show it in the video_display holder
        if displaying_video:
            self.display_video()

    def display_video(self):

        video_path = "./results/output.mp4"
        wmp = WindowsMediaPlayer()
        wmp.main(video_path)

    def download_video(self):
        # Replace "path/to/your/generated/video" with the actual path to your generated video file
        generated_video_path = "./results/output.mp4"

        # Open a file dialog for the user to choose the destination path and file name
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("Video files", "*.mp4"), ("All files", "*.*")],
            title="Save Video As"
        )

        # Check if the user canceled the file dialog
        if not file_path:
            return

        # Download the video to the selected file path
        shutil.copy(generated_video_path, file_path)
        # urlretrieve(generated_video_path, file_path)
        self.output_text.insert(tk.END, f"Video downloaded to: {file_path}\n")
        self.root.update_idletasks()
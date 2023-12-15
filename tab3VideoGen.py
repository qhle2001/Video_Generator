import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from PIL import Image, ImageTk
import os
import subprocess
import threading
import time
import sys
from VideoDisplay import WindowsMediaPlayer
import shutil

class Video:
    def __init__(self, notebook, root):
        self.root = root
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Video Generation")

        frame = tk.Frame(self.frame)
        frame.pack(pady=10, padx=10, side=tk.LEFT)  # Đặt frame ảnh ở bên trái

        # Image Gallery
        self.label = tk.Label(frame, text="Images in the folder:", font=("Arial", 14))
        self.label.pack(pady=10)

        # Create a Listbox to display image names
        self.image_listbox = tk.Listbox(frame, selectmode=tk.SINGLE, height=10)
        self.image_listbox.pack(pady=10, side=tk.TOP)

        # Create Add and Delete buttons
        self.add_button = tk.Button(frame, text="Add", command=self.add_image)
        self.add_button.pack(side = tk.TOP, padx=5)

        self.delete_button = tk.Button(frame, text="Delete", command=self.delete_image)
        self.delete_button.pack(side=tk.TOP, padx=5)

        # Create a Scrollbar for the Listbox
        self.scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link the Listbox and Scrollbar
        self.image_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.image_listbox.yview)

        # Create a Canvas widget for image display
        self.image_display = tk.Canvas(frame, width=400, height=400, background="white")
        self.image_display.pack()

        # Tạo một label để hiển thị tên audio
        self.audio_label = tk.Label(frame, text="Audio File:")
        self.audio_label.pack(side=tk.LEFT, padx=10)

        # Tạo một Text widget để hiển thị tên audio
        self.audio_text = tk.Text(frame, height=1, width=30)
        self.audio_text.pack(side=tk.LEFT, padx=5)

        # Tạo một button để chọn audio file
        self.audio_button = tk.Button(frame, text="Play Audio",
                                      command=lambda: self.play_audio(self.audio_text.get("1.0", tk.END).strip()))
        self.audio_button.pack(side=tk.LEFT, padx=5)

        # Bind selection event to update image display
        self.image_listbox.bind("<<ListboxSelect>>", self.display_selected_image)

        # Load images from the specified folder
        self.load_images()

        # Hiển thị hình ảnh đầu tiên trong thư mục khi chương trình được khởi chạy
        self.display_first_image()

        # Video Generation
        video_frame = tk.Frame(self.frame)
        video_frame.pack(pady=10, padx=10, side=tk.RIGHT)  # Đặt frame video ở bên phải

        # Create a frame to hold Run and Download buttons
        button_frame = ttk.Frame(video_frame)
        button_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.button_run = tk.Button(button_frame, text="Run", command=self.run_script)
        self.button_run.pack(side=tk.LEFT, padx=10)

        # Create a button for video generation and download
        self.download_button = ttk.Button(button_frame, text="Download", command=self.download_video)
        self.download_button.pack(side=tk.RIGHT, padx=10)
        self.download_button.pack_forget()

        scroll = ttk.Frame(video_frame)
        scroll.pack(padx=10, pady=10)

        self.output_text = scrolledtext.ScrolledText(scroll, wrap=tk.WORD, width=150, height=40)
        self.output_text.pack(pady=10, padx=10, expand=True, fill="both")

        self.progressbar = ttk.Progressbar(scroll, mode='determinate', length=200)
        self.progressbar.pack()

        # Create a Canvas widget for video display
        self.video_display = tk.Canvas(video_frame, width=600, height=400)
        self.video_display.pack()

        self.load_first_audio()

    def run_script(self):
        # Clear the previous output
        self.download_button.pack_forget()
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
        process = subprocess.Popen(["python", "VideoGen.py"], stdout=subprocess.PIPE,
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

        self.download_button.pack()

        # If video is being displayed, show it in the video_display holder
        if displaying_video:
            self.display_video()

    def play_audio(self, file_name):

        folder_path = "./audio"
        audio_path = os.path.join(folder_path, file_name)
        wmp = WindowsMediaPlayer()
        wmp.main(audio_path)

    def display_video(self):
        video_path = "./results/new_video.mp4"
        wmp = WindowsMediaPlayer()
        wmp.main(video_path)
        # Replace the following line with your video display logic
        print(f"Displaying video: {video_path}")

    def load_images(self):
        # Replace "path/to/your/image/folder" with the actual path to your image folder
        folder_path = "./images"

        # Clear existing items in the Listbox
        self.image_listbox.delete(0, tk.END)

        # Display each image name in the Listbox
        file_names = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        for image_file in file_names:
            self.image_listbox.insert(tk.END, image_file)

    def add_image(self):
        # Replace "path/to/your/image/folder" with the actual path to your image folder
        folder_path = "./images/"

        # Ask the user to select an image file
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg")],
        )

        if file_path:
            # Get the name of the image file
            image_name = os.path.basename(file_path)

            # Check if the file is not already in the Listbox
            if image_name not in self.image_listbox.get(0, tk.END):
                # Copy the image file to the folder
                destination_path = os.path.join(folder_path, image_name)
                shutil.copy(file_path, destination_path)

                # Update the Listbox with the new image
                self.image_listbox.insert(tk.END, image_name)

                # Load and display the selected image
                # self.display_image(destination_path)
                # destination_path = os.path.join(folder_path, image_name)
                # os.popen(f'copy "{file_path}" "{destination_path}"')
                #
                # # Update the Listbox with the new image
                # self.image_listbox.insert(tk.END, image_name)

    def delete_image(self):
        # Replace "path/to/your/image/folder" with the actual path to your image folder
        folder_path = "images"

        # Get the selected image name from the Listbox
        selected_index = self.image_listbox.curselection()
        if selected_index:
            selected_image = self.image_listbox.get(selected_index)
            selected_image_path = os.path.join(folder_path, selected_image)

            # Remove the image file from the folder
            os.remove(selected_image_path)

            # Remove the image from the Listbox
            self.image_listbox.delete(selected_index)
            # Clear the existing image on the Canvas
            self.image_display.delete("all")

            # Clear the audio_text
            self.audio_text.delete(1.0, tk.END)

    def display_selected_image(self, event):
        # Get the selected image name from the Listbox
        selected_index = self.image_listbox.curselection()
        if selected_index:
            selected_image = self.image_listbox.get(selected_index)

            # Replace "path/to/your/image/folder" with the actual path to your image folder
            folder_path = "images"
            selected_image_path = os.path.join(folder_path, selected_image)


            # Load the selected image and display it on the Canvas
            img = Image.open(selected_image_path)
            # img.thumbnail((400, 400))

            # Resize the image to fit the dimensions of image_display
            img = img.resize((self.image_display.winfo_width(), self.image_display.winfo_height()), Image.ANTIALIAS)

            img_tk = ImageTk.PhotoImage(img)
            self.image_display.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.image_display.image_reference = img_tk

            # Update the audio_text with the corresponding audio file name
            audio_name = self.get_corresponding_audio(selected_index)
            self.audio_text.delete(1.0, tk.END)
            self.audio_text.insert(tk.END, audio_name)

    def display_first_image(self):
        # Get the first image in the Listbox
        first_image = self.image_listbox.get(0)

        # Replace "path/to/your/image/folder" with the actual path to your image folder
        folder_path = "images"
        first_image_path = os.path.join(folder_path, first_image)

        # Load the first image and display it on the Canvas
        img = Image.open(first_image_path)
        # img.thumbnail((400, 400))
        # Resize the image to fit the dimensions of image_display
        img = img.resize((self.image_display.winfo_width(), self.image_display.winfo_height()), Image.ANTIALIAS)

        img_tk = ImageTk.PhotoImage(img)
        self.image_display.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.image_display.image_reference = img_tk

    def load_first_audio(self):
        # Thay đổi đường dẫn thư mục theo thư mục của bạn
        folder_path = "./audio"

        # Lấy danh sách tên tất cả các file audio
        audio_files = [file for file in os.listdir(folder_path) if file.lower().endswith((".mp3", ".wav"))]

        # Nếu có ít nhất một file audio, hiển thị tên audio đầu tiên trong audio_text
        if audio_files:
            first_audio = audio_files[0]
            self.audio_text.delete(1.0, tk.END)
            self.audio_text.insert(tk.END, first_audio)

    def get_corresponding_audio(self, image_index):
        # Replace "path/to/your/audio/folder" with the actual path to your audio folder
        audio_folder_path = "./audio"

        file_names = [file for file in os.listdir(audio_folder_path) if os.path.isfile(os.path.join(audio_folder_path, file))]

        for index in image_index:
            if 0 <= index < len(file_names):
                return file_names[index]
            else:
                return "No matching audio"

    def download_video(self):
        # Replace "path/to/your/generated/video" with the actual path to your generated video file
        generated_video_path = "./results/new_video.mp4"

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
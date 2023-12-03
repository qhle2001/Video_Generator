import os

array_path = ['images', 'videos', 'audio']

for path in array_path:
    folder_path = path
    #Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        #List all files in the folder
        files = os.listdir(folder_path)

        #Iterate through the files and remove each one
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"File '{file_path}' removed successfully.")
            else:
                print(f"Skipping '{file_path}' as it is not a file.")
        print(f"All files in '{folder_path}' removed successfully.")
    else:
        print(f"Folder '{folder_path}' not found.")

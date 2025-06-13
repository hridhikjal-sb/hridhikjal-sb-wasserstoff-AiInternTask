import os

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Could not delete {file_path}: {e}")

def delete_text_files(folder_path: str):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            try:
                os.remove(os.path.join(folder_path, filename))
            except Exception as e:
                print(f"Failed to delete {filename}: {e}")
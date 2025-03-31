from faster_whisper import WhisperModel
import os
import shutil

def save_file(file):
    if file is not None:
        # Ensure the directory exists
        save_dir = "app/data"
        os.makedirs(save_dir, exist_ok=True)  # ✅ Create directory if it doesn't exist

        # Define the full file path
        file_location = os.path.join(save_dir, file.filename)  # ✅ Corrected path format
        
        # Save the file locally
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        return file_location
    else:
        return None  
    
def download_model():
    # Set model path
    model_dir = "./../app/models/whisper_base_en"  # Change to your preferred directory
    model = WhisperModel("base.en", download_root=model_dir)
    return("✅ Model downloaded and stored locally at:", model_dir)

def clear_pycache(directory: str = "/"):
    """
    Recursively deletes all __pycache__ directories in the given directory.
    :param directory: The root directory to search for __pycache__ folders.
    """
    for root, dirs, files in os.walk(directory):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache_path)
            print(f"🗑️ Deleted: {pycache_path}")
import os
import json


# & Decorator to repeat if function is incorrect
def repeat_if_incorrect(func):    
    def wrapper():
        function_return = func()
        while (not function_return):
            function_return = func()
        return function_return
            
    return wrapper


# & Function to convert json to dictionary
def json_to_dict(path_to_json: str = "settings.json") -> dict:
    with open(path_to_json) as file:
        data = json.load(file)
    return data


# & Function to convert dictionary to json
def dict_to_json(data: dict, path_to_json: str = "settings.json"):
    with open(path_to_json, 'w') as file:
        json.dump(data, file)


# & Check if filename is valid
def is_filename_valid(file_name: str) -> bool:
    if not file_name.strip():
        return False
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
    if any(char not in allowed_chars for char in file_name):
        return False
    if not file_name.endswith(".txt"):
        return False
    if len(file_name) > 255:
        return False
    reserved_names = set(["CON", "PRN", "AUX", "NUL"])
    if file_name.upper() in reserved_names:
        return False
    return True


# & Getting path to folder to store notes
@repeat_if_incorrect
def get_path_to_notes() -> str:
    path = input("Enter path to notes: ")
    
    # ! Check if exists
    if not os.path.exists(path):
        print("Path doesn't exist")
        return False
    
    # ! Check if folder is empty
    if len(os.listdir(path)) != 0:
        print("Folder must be empty")
        return False
    
    return path


# & Get note name
@repeat_if_incorrect
def get_note_name() -> str:
    note_name = input("Enter note name: ")
    file_name = note_name+".txt"
    if not is_filename_valid(file_name):
        print("Invalid filename")
        return False
    return note_name


# & Check if notes folder is initialized
def is_initialized() -> bool|dict:
    try: settings = json_to_dict()
    except FileNotFoundError: return False
    return settings


# & Main function
def main():
    # ! Initializing notes folder if not already initialize
    settings = is_initialized()

    if not is_initialized():
        path = get_path_to_notes()
        settings = {"path": path}
        dict_to_json(settings)
    
    path = settings["path"]
    print("Notes folder initialized at "+path)

    # ! Main loop
    while True:
        command = input("Enter command: ")

        # ? Command to exit the program
        if command == "!exit":
            break


if (__name__ == "__main__"):
     main()
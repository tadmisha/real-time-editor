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
    if file_name == "":
        print("Filename cannot be empty")
        return False
    forbidden_chars = set(r"\/:*?\"<>|")
    if any(char in forbidden_chars for char in file_name):
        print("Filename contains invalid characters")
        return False
    if len(file_name) > 255:
        print("Filename is too long")
        return False
    reserved_names = set(["CON", "PRN", "AUX", "NUL"])
    if file_name.upper() in reserved_names:
        print("Filename is in the list of reserved names")
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
        settings = {"path": path, "notes": []}
        dict_to_json(settings)
    
    path = settings["path"]
    print("Notes folder initialized at "+path)

    # ! Main loop
    while True:
        command = input("Enter command: ")

        # ? Command to create new note
        if command == "!new":
            note_name = get_note_name()
            with open(path+"/"+note_name+".txt", "w") as _: ...
            settings["notes"].append(note_name)
            dict_to_json(settings)

        # ? Command to exit the program
        elif command == "!exit":
            break
        
        # ? If command doesn't exist
        else:
            print("Command not supported")
   
        print()


if (__name__ == "__main__"):
     main()
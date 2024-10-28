import os
import json


# & Decorator to repeat if function is incorrect
def repeat_if_incorrect(func, *args, **kwargs):    
    def wrapper(*fargs, **fkwargs):
        function_return = func(*fargs, **fkwargs)
        while (not function_return):
            function_return = func(*fargs, **fkwargs)
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
    if not file_name:
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
def get_note_name(settings: dict) -> str:
    note_name = input("Enter note name: ")
    file_name = note_name+".txt"
    if note_name in settings["notes"]:
        print("Note already exists")
        return False
    if not is_filename_valid(file_name):
        return False
    return note_name


# & Get note name for functions
@repeat_if_incorrect
def get_note_name_for_functions(settings: dict) -> str:
    note_name = input("Enter note name: ")
    if note_name not in settings["notes"]:
        print("Note doesn't exist")
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
    print("Notes folder initialized at "+path+"\n")

    # ! Main loop
    while True:
        command = input("Enter command: ")

        # ? Command to create new note
        if command == "!new":
            note_name = get_note_name(settings)
            with open(path+"/"+note_name+".txt", "w") as _: ...
            settings["notes"].append(note_name)
            dict_to_json(settings)

        # ? Command to read note
        elif command == "!read":
            note_name = get_note_name_for_functions(settings)
            with open(path+"/"+note_name+".txt", "r") as file:
                print(file.read())

        # ? Command to write note
        elif command == "!write":
            note_name = get_note_name_for_functions(settings)
            text = input("Enter text: ")
            with open(path+"/"+note_name+".txt", "w") as file:
                file.write(text)
        
        # ? Command to delete note
        elif command == "!delete":
            note_name = get_note_name_for_functions(settings)
            settings["notes"].remove(note_name)
            os.remove(path+"/"+note_name+".txt")
            dict_to_json(settings)
        
        # ? Command to search for note by keyword
        elif command == "!search":
            keyword = input("Enter keyword: ")
            notes_with_keyword = []
            for note in settings["notes"]:
                with open(path+"/"+note+".txt", "r", encoding="utf-8") as file:
                    if keyword in file.read():
                        notes_with_keyword.append(note)
            print("This keyword is found in the following notes: "+", ".join(notes_with_keyword))

        # ? Command to exit the program
        elif command == "!exit":
            break
        
        # ? If command doesn't exist
        else:
            print("Command not supported")
   
        print()


if (__name__ == "__main__"):
     main()
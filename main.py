import os
import json


# * Text for the help function
help_text = """!help - provides information about all the other commands
!new - creates new note
!write - writes in a chosen note
!read - reads a chosen note
!delete - deletes a chosen note
!search - search notes by keywords
!exit - exits the editor"""


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
    if (not file_name):
        print("Filename cannot be empty")
        return False
    forbidden_chars = set(r"\/:*?\"<>|")
    for char in forbidden_chars:
        if char in file_name:
            print(f"Contains forbidden character \"{char}\"")
    if (len(file_name) > 255):
        print("Filename is too long")
        return False
    reserved_names = set(["CON", "PRN", "AUX", "NUL"])
    if (file_name.upper() in reserved_names):
        print("Filename is in the list of reserved names")
        return False
    
    return True


# & Getting path to folder to store notes
@repeat_if_incorrect
def get_path_to_notes() -> str:
    path = input("Enter path to notes: ")
    
    # ! Check if exists
    if (not os.path.exists(path)):
        print("Path doesn't exist")
        return False
    
    return path


# & Get note name
@repeat_if_incorrect
def get_note_name(settings: dict) -> str:
    note_name = input("Enter note name: ").replace(' ', '')
    file_name = note_name+".txt"
    if (note_name in settings["notes"]):
        print("Note with this name already exists")
        return False
    if (not is_filename_valid(file_name)):
        return False
    return note_name


# & Get note name for functions
@repeat_if_incorrect
def get_note_name_for_functions(settings: dict) -> str:
    note_name = input("Enter note name: ").replace(' ', '')
    if (note_name not in settings["notes"]):
        print("Note doesn't exist")
        return False
    return note_name


# & Check if notes folder is initialized
def get_settings_if_initialized() -> bool|dict:
    empty = False
    try: settings = json_to_dict()
    except FileNotFoundError: return False
    except json.decoder.JSONDecodeError: empty = True
    print(type(settings["notes"]))
    if ((empty) or \
    (not "path" in settings) or \
    (not "notes" in settings) or \
    (type(settings["path"]) != str) or \
    (type(settings["notes"]) != list) or \
    (not any([type(note) == str for note in settings["notes"]]))):
        print("Invalid settings format, write path to your notes folder")
        quit()
        os.remove("settings.json")
        return False
    return settings


# & Main function
def main():
    # ! Initializing notes folder if not already initialize
    # * Contains data from settings.json (folder path and notes names)
    settings = get_settings_if_initialized()

    if (not settings): # If not initialized
        path = get_path_to_notes()
        settings = {"path": path, "notes": []}
        # ^ Adding all the notes (txt files) that are already in the path folder
        files = os.listdir(path)
        for file in files:
            if file.endswith(".txt"):
                settings["notes"].append(file[:-4])
        dict_to_json(settings)
    
    path = settings["path"]
    print("Notes folder initialized at "+path+"\n")

    # ! Main loop
    while True:
        command = input("Enter command: ").replace(' ', '')

        # ? Command that provides information about all the other commands
        if (command == "!help"):
            print(help_text)

        # ? Command to create new note
        elif (command == "!new"):
            note_name = get_note_name(settings)
            with open(path+"/"+note_name+".txt", "w") as _: ...
            settings["notes"].append(note_name)
            dict_to_json(settings)

        # ? Command to read note
        elif (command == "!read"):
            note_name = get_note_name_for_functions(settings)
            with open(path+"/"+note_name+".txt", "r") as file:
                print(file.read())

        # ? Command to write note
        elif (command == "!write"):
            note_name = get_note_name_for_functions(settings)
            text = input("Enter text: ")
            with open(path+"/"+note_name+".txt", "w") as file:
                file.write(text)
        
        # ? Command to delete note
        elif (command == "!delete"):
            note_name = get_note_name_for_functions(settings)
            settings["notes"].remove(note_name)
            os.remove(path+"/"+note_name+".txt")
            dict_to_json(settings)

        # ? Command to list all the notes
        elif (command == "!list"):
            print(", ".join(settings["notes"]))
        
        # ? Command to search for note by keyword
        elif (command == "!search"):
            keyword = input("Enter keyword: ")
            notes_with_keyword = []
            for note in settings["notes"]:
                with open(path+"/"+note+".txt", "r", encoding="utf-8") as file:
                    if keyword in file.read():
                        notes_with_keyword.append(note)
            print("This keyword is found in the following notes: "+", ".join(notes_with_keyword))

        # ? Command to exit the program
        elif (command == "!exit"):
            break
        
        # ? Command doesn't exist
        else:
            print("Command not supported")
   
        print()


if (__name__ == "__main__"):
     main()
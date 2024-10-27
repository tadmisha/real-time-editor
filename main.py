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
        print("Notes folder initialized at "+path)


if (__name__ == "__main__"):
     main()
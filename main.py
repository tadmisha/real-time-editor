import os

# & Decorator to repeat if function is incorrect
def repeat_if_incorrect(func):    
    def wrapper():
        function_return = func()
        while (not function_return):
            function_return = func()
        return function_return
            
    return wrapper


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
    

# & Main function
def main():
    ...


if (__name__ == "__main__"):
     main()
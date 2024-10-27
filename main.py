
# & Decorator to check if input is correct
def repeat_if_incorrect(func):    
    def wrapper():
        function_return = func()
        while (not function_return):
            function_return = func()
        return function_return
            
    return wrapper


# & Main function
def main():
    ...


if (__name__ == "__main__"):
     main()
def print_error(message):
    '''
    Function
    --------
    print error message

    Parameters
    ----------
    message : 
        str : error message
    '''
    print(f"\033[31m{message}\033[0m")
    
    
if __name__ == "__main__":
    print_error("error")
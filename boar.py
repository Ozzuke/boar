#!/usr/bin/env python3

# A program to view, add, edit and export short references for later use (CLI apps, commands, websites, books etc)
# Author Osvald Nigola


import argparse  # module for parsing arguments passed from the command line
import os
import json
import time


def create_data_dir(dotfile_path, dot_config_path, home):
    """Create the directory for storing the application's files"""
    
    # prompt to create the directory
    prompt("It seems no data directory has been set up yet. Proceed?")
    
    # prompt about the location to create the directory in, then create it
    where = prompt(f"\nWhere to create data directory? \n1: {dotfile_path} \n2: {dot_config_path} \nQ to abort \nSelect location",
                   default="1", positive=False, custom=[1, 2])
    if where == "1":
        os.mkdir(dotfile_path)
        print("Created directory at", dotfile_path)
    elif where == "2":
        try:
            os.mkdir(dot_config_path)
            print("Created directory at", dot_config_path)
        except FileNotFoundError:
            print(f"The directory '{home}/.config/' was not found.")
            exit()


def create_defaults(path_loc, create_book=False, create_conf=False, create_history_dir=False):
    """Create the contents to the data folder"""
    
    # the main data structure for keeping the references
    book = [
        {
            "name": "Template Category",
            "short": "temp",
            "items": [
                {
                    "name": "Template entry 1",
                    "desc": "A good description about the entry",
                    "link": "https://example.com"
                },
                {
                    "name": "A second template entry",
                    "desc": None,
                    "link": None
                }
            ],
        }
    ]
    
    # configuration
    conf = {
        "history length": 5,
        "disable colors": False
    }

    # create the book file for storing the data in the book
    if create_book:
        with open(path_loc + "book", "w") as book_file:
            json.dump(book, book_file)
    # create the config file
    if create_conf:
        with open(path_loc + "conf", "w") as conf_file:
            json.dump(conf, conf_file)
    # create the directory to keep the last n copies of the book in for ability to undo actions
    if create_history_dir:
        os.mkdir(path_loc + "history")
        

def prompt(message, default="y", positive=True, negative=True, custom=False, add_expected=True, tries=5, exit_on_false=True, invalid_as_false=False):
    """
    Prompt the user about a choice (yes/no by default)
    message: [str] the message to be displayed at the prompt, e.g. "Proceed with file creation?" (add \n to message for prompt to appear on a new line)
    default: [str] the answer that an empty string (i.e. just pressing enter) is interpreted as ("y" or "n" for default bool, custom string or None otherwise)
    positive: [bool / list] if prompt expects a boolean answer, leave True for default values interpreted as positive ("y" and "yes", case insensitive),
        a list or tuple object for a custom set of answers, False for no positive boolean comparison
    negative: [bool / list] like positive, except for negative boolean (default negatives are "n" and "no", "q" and "quit")
    custom: [False / list] if input matches any of the values in the list, it will be returned, instead of waiting for a boolean response
    add_expected: [bool / str] add expected input to end of message. String for custom addition
    tries: [int] number of times the question prompt can appear (reappearing in case of invalid answer, 1 means an invalid answer causes the application to quit immediately)
    exit_on_false: [bool] call exit() on negative answer, otherwise return False
    invalid_as_false: [bool] in no valid answer given in set tries, interpret it as False
    """
    
    # add expected input to end of message
    if positive and negative and add_expected is True:
        # boolean answer
        if default == "y":
            # default positive
            message += " [Y/n] "
        elif default == "n":
            # default negative
            message += " [y/N] "
        elif not default:
            # no default
            message += " [y/n] "
    elif type(add_expected) != bool:
        message += add_expected
    elif custom and add_expected:
        message += f" {custom} "
        if default:
            message += f"(default {default}) "
    
    for i in range(tries):
        # ask for input
        answ = input(message)
        # convert it to default if applicable
        if answ == "" and default:
            answ = default
        answ = answ.lower()
        
        # convert positive and negative to defaults if applicable
        if positive is True:
            positive = ["y", "yes"]
        if negative is True:
            negative = ["n", "no", "q", "quit"]
        
        # compare answer for a match
        if custom and answ in [str(x).lower() for x in custom]:
            return answ
        if positive and answ in [str(x).lower() for x in positive]:
            return True
        if negative and answ in [str(x).lower() for x in negative]:
            if exit_on_false:
                exit()
            return False
        
        time.sleep(0.5)
    
    # if no valid answer has been given so far
    if invalid_as_false and not exit_on_false:
        return False
    print("Unable to understand")
    exit()
        


def main():
    
    # create partser to parse arguments passed from the command line
    parser = argparse.ArgumentParser(description="Add, edit and view a list of short references.")
    parser.add_argument("foo", nargs="*")  # argument to gather all input from the command line into a list
    args = parser.parse_args().foo  # a list of all non-positional input
    
    # check if passed argument for action is a valid one and store it
    if not args:
        act = "ls"
    elif args[0] in ["add", "addcat", "ls", "rm", "rmcat", "reset", "undo", "export"]:
        act = args.pop(0)
    else:
        exit("Invalid argument.")
    
    # path to data directory
    home = os.path.expanduser("~")
    path = home + "/.boar/"
    path2 = home + "/.config/boar/"
    
    # check if data directory exists and handle appropriately if it doesn't
    if not ( os.path.exists(path) or os.path.exists(path2) ):
        create_data_dir(path, path2, home)
        path = path if os.path.exists(path) else path2
        create_defaults(path, create_book=True, create_conf=True, create_history_dir=True)
    path = path if os.path.exists(path) else path2
    
    # check if required files exist in directory
    if not os.path.exists(path + "book"):
        if prompt("File 'book' missing in directory. Create it now?"):
            create_defaults(path, create_book=True)
    if not os.path.exists(path + "conf"):
        if prompt("File 'conf' missing in directory. Create it now?"):
            create_defaults(path, create_conf=True)
    if not os.path.exists(path + "history"):
        if prompt("Directory 'history' missing in directory. Create it now?"):
            create_defaults(path, create_history_dir=True)
    
    # load data and config from file
    with open(path + "book") as book_file, open(path + "conf") as conf_file:
        # try reading the book file
        try:
            book = json.load(book_file)
        except json.decoder.JSONDecodeError:
            print("Error decoding file 'book'")
            if prompt("Overwrite the file 'book' with defaults?"):
                create_defaults(path, create_book=True)
            book = json.load(book_file)
        
        # try reading the config file
        try:
            conf = json.load(conf_file)
        except json.decoder.JSONDecodeError:
            print("Error decoding config file 'conf'")
            if prompt("Overwrite the file 'conf' with defaults?"):
                create_defaults(path, create_conf=True)
            conf = json.load(conf_file)
    #print(book, conf, sep="\n")
    print("Looks good so far")
    


if __name__ == "__main__":
    main()

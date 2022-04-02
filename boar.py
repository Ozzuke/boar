#!/usr/bin/env python3

# A program to view, add, edit and export short references for later use (CLI apps, commands, websites, books etc)
# Author Osvald Nigola


import argparse  # module for parsing arguments passed from the command line
import os
import json
import time
import string


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
        "disable colors": False,
        "show_links": True
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
        if not os.path.exists(path_loc + "history"):
            os.mkdir(path_loc + "history")
        

def prompt(message, default="y", positive=True, negative=True, custom=False, add_expected=True, tries=3, exit_on_false=True, invalid_as_false=False):
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
        

def ls(args, book, conf):
    """Show the contents of the book or a specific category
    format:
    ID Name (short) – description
    2   Template Category  (temp)
    2.1  - Template entry [L] : a good description about the entry
             link: https://example.com
    2.2  - A second entry :"""
    
    book = book.copy()
    
    # if book is empty, say as much and exit
    if not book:
        print("No items to show.")
        exit()
    
    # if asked for a non-existent category, say as much and exit
    if args and args not in [x["short"] for x in book] + [str(x) for x in range(1, len(book) + 1)]:
        print("Category doesn't exist.")
        exit()
    
    # find the amount of characters the longest ID takes to display
    longest_id = len(str(len(book))) + 1 + len(str(max([len(x["items"]) for x in book])))
    
    print("BOAR – Book Of All References")
    for id1, cat in enumerate(book, 1):
        if not args or args in [str(id1), cat["short"]]:
            # write the category ID
            print(str(id1) + " " * (longest_id - len(str(id1))), end=" ")
            # write the category name
            print(cat["name"], end="  ")
            # write the short version of the category name if present
            if cat["short"]:
                print(f"({cat['short']})")
            else:
                # add newline
                print()
            
            # write out the items in the category
            for id2, item in enumerate(cat["items"], 1):
                # write the item ID
                print(str(id1) + "." + str(id2) + " " * (longest_id - len(str(id1)) - 1 - len(str(id2))), end="  - ")
                # write the item name
                print(item["name"], end=" ")
                # indicate the presence of a link if exists
                if item["link"]:
                    print("[L]", end=" ")
                # add ':' before description
                print(":", end=" ")
                # write the description if it exists
                print(item["desc"] if item["desc"] else "...")
                
                # if link is present, write it in a new line
                if item["link"] and conf["show_links"]:
                    print(" " * (longest_id + 5), "link:", item["link"])
        
        # add newline between categories
        if id1 != len(book) and not args:
            print()
            
    
def addcat(args, book, conf):
    """Add a category to the book, returns the edited book"""
    
    book = book.copy()
    
    # get the category name
    if args:
        cat_name = args
    else:
        cat_name = input("Category name (leave blank to abort): ")
        if not cat_name:
            exit()
    if cat_name.lower() in [x["name"].lower() for x in book]:
        exit("Category with the same name already exists.")
    
    # get the short name for the category
    while True:
        short = input("Short name for category (leave blank to use first four letters): ")
        # exit if needed
        if short == "q":
            exit()
        # create short name from category name
        if not short:
            short = "".join([x for x in cat_name.lower() if x.isalnum()])[:4]  # use only alphanumeric characters
            if not short or short[0].isnumeric() or len(short) < 2:
                print("Unable to generate a short name. Please enter one manually.")
                continue
            if short not in [x["short"] for x in book]:
                break  # all good
            short += str([x["short"] for x in book].count(short) + 1)
            break
        if not short.isalnum() or short[0].isnumeric() or not 2 <= len(short) <= 8:
            print("Short name must be composed of alphanumeric characters, can not start with a number and be 2-8 characters long.")
            continue
        if short not in [x["short"] for x in book]:
            break  # all good
        print("A category with the same short name exists. Consider adding a number at the end.")
    
    # add created category to book
    book.append({
        "name": cat_name,
        "short": short.lower(),
        "items": []
        })
    
    # return the modified book object
    return book


def add(args, book, conf):
    """Adds an object to a category, returns the modified book"""
    
    book = book.copy()
    
    # get the category to add to
    if args:
        args = args.split(" ")
        cat_n = args.pop(0)
        args = "-".join(args)
        
    else:
        cat_n = input("Category name (short) or ID to add to: ")
        if not cat_n:
            exit()
    # check if category exists or if ID is valid
    if cat_n not in [x["short"] for x in book] and not ( cat_n.isnumeric() and 0 < int(cat_n) <= len(book) ):
        exit(f"Category with short name or ID of '{cat_n}' doesn't exist.")
    
    # get the name for the item
    if args:
        name = args
    else:
        name = input("Item name: ")
    if not name:
        exit("Name can't be blank.")
    
    mod_book = []
    # generate new book with selected category added
    for i, cat in enumerate(book, 1):
        
        # if not the selected category, add it to new book unchanged
        if cat_n not in [str(i), cat["short"]]:
            mod_book.append(cat)
            continue
        
        # check if item of the same name does not happen to already be present
        if name.lower() in [x["name"].lower() for x in cat["items"]]:
            exit("Item of the same name already exists in category. You may want to modify it instead.")
        
        # ask for a description of the item
        desc = input("Item description (or leave blank): ")
        desc = desc if desc else None
        
        # ask for a link for the item
        link = input("Item link (or leave blank): ")
        link = link if link else None
        
        cat["items"].append({
            "name": name,
            "desc": desc,
            "link": link
            })
        
        mod_book.append(cat)
    
    return mod_book
        


def main():
    
    # create partser to parse arguments passed from the command line
    parser = argparse.ArgumentParser(description="Add, edit and view a list of short references.")
    parser.add_argument("foo", nargs="*")  # argument to gather all input from the command line into a list
    args = parser.parse_args().foo  # a list of all non-positional input
    
    # check if passed argument for action is a valid one and store it
    if not args:
        act = "ls"
    elif args[0] in ["add", "addcat", "ls", "rm", "rmcat", "edit", "editcat", "reset", "undo", "export", "test"]:
        act = args.pop(0)
    else:
        exit("Invalid operation.")
    
    # convert remaining arguments to a string
    args = " ".join(args)
    
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
    
    if act == "test":
        exit("Looks good so far")
    
    # act according to chosen operation
    elif act == "ls":
        ls(args, book, conf)
        exit()
    elif act == "reset":
        # restore defaults
        if prompt("This will overwrite the book and the config. Proceed?", default="y"): #TODO: set deafult to no
            create_defaults(path, True, True, True)
        exit()
    elif act == "addcat":
        book_edited = addcat(args, book, conf)
    elif act == "add":
        book_edited = add(args, book, conf)
    ls(None, book_edited, conf)


if __name__ == "__main__":
    main()

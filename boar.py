#!/usr/bin/env python3

# A program to view, add, edit and export short references for later use (CLI apps, commands, websites, books etc)
# Author Osvald Nigola


import argparse  # module for parsing arguments passed from the command line
import os
import json
import time


def create_data_dir(local_path_normal, local_path_config):
    """Create the directory for storing the application's files"""
    
    # prompt to create the directory
    for i in range(5):
        do_setup = input("It seems no data directory has been set up yet. Proceed? [Y/n] ")
        if do_setup.lower() in ["y", "yes", ""]:
            break
        elif do_setup.lower() in ["n", "no"]:
            exit()
        if i != 4:
            time.sleep(0.5)
            continue
        exit("Unable to understand.")
    
    # prompt about the location to create the directory in, then create it
    for i in range(5):
        dir_where = input(f"\nWhere to create the directory? \n1: {local_path_normal}  (default) \n2: {local_path_config} \nQ to abort \nSelect location [1-2] (default 1) ")
        if dir_where in ["1", ""]:
            os.mkdir(local_path_normal)
            print("Created directory at", local_path_normal)
            break
        elif dir_where in ["2"]:
            try:
                os.mkdir(local_path_config)
                print("Created directory at", local_path_config)
                break
            except FileNotFoundError:
                print(f"The directory '{os.path.expanduser('~')}/.config/' was not found.")
        elif dir_where.lower() in ["q", "quit", "a", "abort", "n", "no"]:
            exit()
        if i != 4:
            time.sleep(0.5)
            continue
        exit("Unable to understand.")


def create_defaults(path_loc):
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

    # create the file to store the book data in with the template category
    with open(path_loc + "book", "w") as file:
        file.write(json.dumps(book))
    # create the config file
    with open(path_loc + "conf", "w") as file:
        file.write(json.dumps(conf))
    # create the directory to keep the last n copies of the book in for ability to undo actions
    os.mkdir(path_loc + "history")
        

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
    path = os.path.expanduser("~") + "/.boar/"
    path2 = os.path.expanduser("~") + "/.config/boar/"
    
    # check if data directory exists and handle appropriately if it doesn't
    if not (os.path.exists(path) or os.path.exists(path2)):
        create_data_dir(path, path2)
        path = path if os.path.exists(path) else path2
        create_defaults(path)
    path = path if os.path.exists(path) else path2


if __name__ == "__main__":
    main()
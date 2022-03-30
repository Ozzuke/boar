#!/usr/bin/env python3

# A program to view, add, edit and export short references for later use (CLI apps, commands, websites, books etc)
# Author Osvald Nigola


import argparse  # module for parsing arguments passed from the command line
import os
import json


def boar():
    # create partser to parse arguments passed from the command line
    parser = argparse.ArgumentParser(description="Add, edit and view a list of short references.")
    parser.add_argument("foo", nargs="*")  # argument to gather all input from the command line into a list
    args = parser.parse_args().foo  # a list of all non-positional input
    
    # exit if no arguments were passed
    #TODO: possibly change to same as ls
    if not args:
        print("No arguments passed.")
        exit()
    
    # check if passed argument for action is a valid one
    if args[0] in ["add", "addcat", "ls", "lscat", "rm", "rmcat", "reset", "undo", "export"]:
        act = args.pop(0)
    else:
        print("Invalid argument.")
        exit()
    
    # path to data directory
    path = os.path.expanduser("~") + "/.boar/"
    path2 = os.path.expanduser("~") + "/.config/boar/"
    
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
        "history length": 5
    }
    
    # check if data directory exists and handle appropriately
    if os.path.exists(path) or os.path.exists(path2):
        pass
    else:
        # prompt to create the directory
        for i in range(5):
            do_setup = input("It seems no data directory has been set up yet. Proceed? [Y/n] ")
            if do_setup.lower() in ["y", "yes", ""]:
                break
            elif do_setup.lower() in ["n", "no"]:
                exit()
            if i != 4:
                continue
            print("Unable to understand.")
            exit()
        
        # prompt about the location to create the directory in
        for i in range(5):
            dir_where = input(f"Where to create the directory? \n1: {path} (default) \n2: {path2} \nSelect location [1-2] (default 1) ")
            if dir_where in ["1", ""]:
                os.mkdir(path)
                print("Created directory", path)
                break
            elif dir_where in ["2"]:
                try:
                    os.mkdir(path2)
                    print("Created directory", path2)
                    break
                except FileNotFoundError:
                    print(f"The directory '{os.path.expanduser('~')}/.config/' was not found.")
            elif dir_where.lower() in ["q", "n", "no"]:
                exit()
            if i != 4:
                continue
            print("Unable to understand.")
            exit()
        
        print("created dir")


if __name__ == "__main__":
    boar()
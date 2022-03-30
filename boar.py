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
    
    if not args:
        print("No arguments passed.")
        exit()
    
    if args[0] in ["add", "addcat", "ls", "lscat", "rm", "rmcat", "export"]:
        act = args.pop(0)
    else:
        print("Invalid argument.")
        exit()
    
    path = os.path.expanduser("~") + "/.boar/"
    
    with open(os.path.expanduser("~") + "/.vimrc") as testfail:
        print(testfail.read())
    

if __name__ == "__main__":
    boar()
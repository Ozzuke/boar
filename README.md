# boar
`boar` (Book Of All References) is a program for storing items like useful websites, applications with a forgettable name, cool programs to check out later, movies to watch etc. into different categories; items can optionally have a description and a link. Links are normally shown under the name of the item when viewing from the command line, and as hyperlinks of the item name when viewing the exported HTML file in a web browser.


## Installation
The boar.py file contains everything needed to run the program, so it can be run directly or be placed in a directory that's in the `$PATH` environment variable. The following steps will install boar in `$PATH` as `boar`:

Open your terminal and clone the repository to your local machine by running

    git clone https://github.com/ozzuke/boar.git

This should create a directory called `boar` in your current working directory.<br>
There are two ways to install the program: locally (for one user, doesn't require administrative privileges) and globally (for all users, requires administrative privileges).


### Local installation
Create the directory `~/.local/bin` if it doesn't exist already

    mkdir -p $HOME/.local/bin

Check if the directory is in the $PATH environment variable

    [[ $PATH =~ "$HOME/.local/bin" ]] && echo "Found" || echo "Not found"

<br>
If the path was not found in `$PATH`, it needs to be added in your shell config, which is run every time you open your shell:

If you are using `bash` (running `echo $SHELL` returns `/bin/bash` or similar), you can add it to the `$PATH` environment variable by running

    echo 'export PATH="$HOME/.local/bin:$PATH"' >> $HOME/.bashrc

If you are using `zsh` (running `echo $SHELL` returns `/bin/zsh` or similar), you can add it to the `$PATH` environment variable by running

    echo 'export PATH="$HOME/.local/bin:$PATH"' >> $HOME/.zshrc

If you are using `fish` (running `echo $SHELL` returns `/bin/fish` or similar), you can add it to the `$PATH` environment variable by running

    echo 'export PATH="$HOME/.local/bin:$PATH"' >> $HOME/.config/fish/config.fish

If you are using something else, you probably already know what to do.

Reopen your terminal and confirm that the path is now in the `$PATH` environment variable

    [[ $PATH =~ "$HOME/.local/bin" ]] && echo "Found" || echo "Not found"
<br>

Once the path is in the `$PATH` environment variable, you can copy or symlink the boar.py file to the directory `~/.local/bin`. Copying allows the cloned git repository to be deleted but requires the file to be copied again every time the program is updated. If symlinking, the cloned repository can not be deleted, but updating the program requires no extra steps and the update is reflected immediately.<br>
If you cloned the repository to your home directory, the file is going to be located at `~/boar/boar.py`.

Copy:

    cp ~/boar/boar.py ~/.local/bin/boar

Symlink:

    ln -s ~/boar/boar.py ~/.local/bin/boar

You should now be able to run the program by running `boar`.


### Global installation
First check that you have administrative privileges

    sudo -v

You should see a prompt asking for your password. If nothing appears after entering your password correctly, you are good to go. Otherwise you likely don't have administrative privileges and should use the local installation option instead.

Make sure the directory `/usr/local/bin` exists

    [[ -d "/usr/local/bin" ]] && echo "Found" || echo "Not found"

If it wasn't found, create it

    sudo mkdir -p /usr/local/bin

...and reopen the terminal, then confirm that the directory is now in the `$PATH` environment variable

    [[ $PATH =~ "/usr/local/bin" ]] && echo "Found" || echo "Not found"

Copy or symlink the boar.py file to the directory `/usr/local/bin`. Copying allows the cloned git repository to be deleted but requires the file to be copied again every time the program is updated. If symlinking, the cloned repository can not be deleted, but updating the program requires no extra steps and the update is reflected immediately.

If you cloned the repository to your home directory, the file is going to be located at `~/boar/boar.py`.

Copy:

    sudo cp ~/boar/boar.py /usr/local/bin/boar

Symlink:

    sudo ln -s ~/boar/boar.py /usr/local/bin/boar

You should now be able to run the program by running `boar`.


## Usage
- When ran for the first time, it asks to create a directory at either ~/.boar or ~/.config/boar and creates a few files there. The book, by default contains a template entry and two template items.
- `boar ls [category]` - view either all categories and items within them or just a specific category if it's ID (it's position, starting from 1) or short name is passed. Items with a link have `[L]` printed after their name and if configured so, will have the link shown on the line under them. When viewing only a specific category, item links are always shown. Calling `boar` without any arguments is interpreted as `boar ls`.
- `boar ls all` - view all categories and items (by default `boar ls` will show only categories if the total number of categories + items exceeds the configured amount)
- `boar add [category] [item name]` - add an item to a category. Category ID or short name and the name for the item can be passed from the comman line, otherwise they are asked for with a prompt. The program will then prompt for a description and a link to be entered for the item, both of which can be omitted. Absolute links should include the `https://` part if using links in the exported HTML page is desired.
- `boar addcat [category name]` - add a category to the book. Next, a prompt will ask for a short name for the category. It has to consist of 2-8 alphanumeric characters and the first letter can not be a number. If omitted, the program will try to create one from the first four letters, but it might not always be successful or achieve a desired result. Category name will be prompted for if not passed.
- `boar rm [category] [item]` - remove an item from a category. Category can be it's short name or ID, item can be it's name or ID. For convenience, using a dot between two IDs is also accepted, as it's the way item IDs are shown with `ls`. E.g. `boar rm 2.5`. Will be prompted for if not passed.
- `boar rmcat [category]` - remove a category. Category can be it's short name or ID. Will be prompted for if not passed.
- `boar edit [category] [item]` - edit an item. Item can be selected the same way as with `rm`. A prompt will ask for a new name, description and link one by one. Passing an empty string keeps the previous value, passing a configured string (by default 'cl') on either description or link clears the value (sets it to None).
- `boar editcat [category]` - edit a category. Neither the category name or short name can be set to None.
- `boar undo [times]` - undo a change to book. To undo more than once, a number can be passed. The number of previous copies that are retained and thus that can be returned to with `undo` is configurable and is set to 5 by default.
- `boar configure` - view and configure a range of options. All the options are numbered, so a number can be passed to the prompt to edit a value. Passing an empty string exits the program.
- `boar reset` - reset the book and configuration to default. The book will have a template category and two template entries within it. A prompts asks for confirmation before the files are overwritten.
- `boar export [dark|light]` - export the book to an HTML file. Either 'light' or 'dark' can be passed to choose between dark and light mode, otherwise the mode is defined in the configuration (by default it's light mode). The path to the file will be shown once it has been created.

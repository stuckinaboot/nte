# nte
A simple note-taker for unix. So simple that the 'o' in note was too complicated for the name of the program.

## Set-up:
To be able to use nte anywhere, place nte.py in your home directory. Then, open .bash_profile (in your home directory) in your favorite text editor and add the following line:
`alias nte='python ~/nte.py'`
Restart your shell and you are good to go!
Note: There are many other ways to make nte available anywhere, this is just one of the simplest and that's why I'm listing it here

## Taking Notes:
Enter `nte` into your shell and press enter. Then, take a note!
Alternatively, enter `nte "some title to a note" "some message to a note"` to take notes even more quickly.

## Viewing Notes:
Enter `nte v` and view/delete/move notes around.

All notes are stored in a hidden file in your home directory. The file path is `~/.notes.txt`.
This file can be opened/modified/deleted in any text editor and nte will run just fine.

*This program is supposed to be usable by those with very little knowledge of Unix, and the README is designed to reflect that

# PyShell 0.1.0a
# Copyright (c) 2025 SteveGaming62
# All rights reserved. This code cannot be used, modified, or distributed without explicit permission from the author.


# Set up Colorama
try:
    from colorama import *  # Import Colorama
    init(autoreset=True)  # Initialize Colorama
except:
    print("There was an error importing module Colorama. Run \"pip install colorama\" and try again.")
    exit()

# Import os for running bash commands
from os import *

def main():
	uname = input(Fore.BLUE + "Enter your username: " + Style.RESET_ALL)
	prompt = ""
	print(Fore.MAGENTA + Style.BRIGHT + "PyShell v0.1.0a\n" + Style.RESET_ALL + "Type \"exit\" to close PyShell.\n")
    
	while prompt != "exit":
		cdir = getcwd()
		prompt = input(Style.BRIGHT + Fore.BLUE + uname + "@pyshell " + Fore.YELLOW + cdir + Style.RESET_ALL + " $ ")
		if prompt == "bash" or prompt == "sh":
			print(Fore.RED + "You cannot run \"bash\" or \"sh\" in PyShell.")
		else:
			system(prompt)
    
	print(Fore.YELLOW + Style.BRIGHT + "Exiting...")

if __name__ == "__main__":
    main()


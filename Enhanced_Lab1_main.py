# main

from Enhanced_Lab1_GUI import UserInterface
from Enhanced_Lab1_logic import Vote, FileManager
from tkinter import Tk

def main():
    # Initialize the file manager with the CSV file
    filename = "votes.csv"
    file_manager = FileManager(filename)
    
    # Create a vote system using the file manager
    vote_system = Vote(file_manager)
    
    # Create the root window for the Tkinter application
    root = Tk()
    
    # Initialize the user interface with the root window and vote system
    ui = UserInterface(root, vote_system)
    
    # Start the Tkinter event loop
    ui.run()

if __name__ == "__main__":
    main()

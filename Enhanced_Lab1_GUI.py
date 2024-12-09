# GUI

from tkinter import Tk, Label, Button, Entry, Radiobutton, StringVar
from Enhanced_Lab1_logic import Vote, FileManager

class UserInterface:
    def __init__(self, root, vote_system):
        self.root = root
        self.vote_system = vote_system
        self.error_label = None
        self.voter_id_label = None
        self.voter_id_entry = None
        self.vote_button = None
        self.result_label = None
        self.candidate_var = None
        self.voter_id = None
        self.results_button = None

        # Prevent resizing the window
        self.root.resizable(False, False)

        # Initialize the first screen
        self.reset_screen()

    def clear_error(self, *args):
        """Clear error message if the user starts correcting the input."""
        if self.error_label:
            self.error_label.config(text="")

    def process_vote(self):
        """Process the vote entry by checking the voter ID."""
        # Strip spaces from the entered voter ID
        voter_id = self.voter_id_entry.get().strip()
        self.clear_error()

        # Check if the voter ID has already been used
        if not voter_id:
            self.error_label.config(text="Please enter a valid ID.")
            return
        elif voter_id in self.vote_system.file_manager.used_ids:
            self.error_label.config(text="This ID has already voted.")
            return
        
        # Check if the voter ID consists of only digits
        if not voter_id.isdigit():
            self.error_label.config(text="Voter ID must contain only numbers.")
            return

        # Save the entered ID
        self.voter_id = voter_id
        
        # Change the GUI to show the candidates after entering ID
        self.voter_id_label.config(text=f"Voter ID: {voter_id}")
        self.voter_id_entry.destroy()
        self.vote_button.destroy()

        # Remove Results button since we're switching to voting screen
        if self.results_button:
            self.results_button.destroy()

        self.show_candidates()

    def show_candidates(self):
        """Show the candidates after the voter enters a unique ID."""
        Label(self.root, text="Select a candidate:").pack()

        # Create radio buttons for candidates (no default selection)
        self.candidate_var = StringVar(value="")  # Reset the selection variable
        john_button = Radiobutton(self.root, text="John", variable=self.candidate_var, value="1")
        john_button.pack()
        jane_button = Radiobutton(self.root, text="Jane", variable=self.candidate_var, value="2")
        jane_button.pack()

        # Create submit button
        submit_button = Button(self.root, text="Submit Vote", command=self.submit_vote)
        submit_button.pack()

    def submit_vote(self):
        """Submit the selected vote and process it."""
        candidate = self.candidate_var.get()
        
        if candidate == "":
            self.error_label.config(text="Please select a candidate.")
            return
        
        try:
            self.vote_system.vote(self.voter_id, candidate)
            self.show_submission_confirmation()
        except ValueError as e:
            self.error_label.config(text=str(e))

    def show_submission_confirmation(self):
        """Display the vote confirmation screen."""
        # Remove previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Display confirmation message
        confirmation_label = Label(self.root, text="Your vote has been successfully submitted!", fg="green")
        confirmation_label.pack()

        # Button to go back to the first screen
        back_button = Button(self.root, text="Back to Vote", command=self.reset_screen)
        back_button.pack()

    def reset_screen(self):
        """Reset the GUI to the initial voter ID screen."""
        # Remove current widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create error label (recreating it)
        self.error_label = Label(self.root, text="", fg="red")
        self.error_label.pack()

        # Create voter ID entry label
        self.voter_id_label = Label(self.root, text="Enter your unique ID:")
        self.voter_id_label.pack()

        # Create voter ID entry field
        self.voter_id_entry = Entry(self.root)
        self.voter_id_entry.pack()

        # Create vote button
        self.vote_button = Button(self.root, text="Vote", command=self.process_vote)
        self.vote_button.pack()

        # Create result label (it can remain empty)
        self.result_label = Label(self.root, text="")
        self.result_label.pack()

        # Initialize the candidate selection variable (no selection)
        self.candidate_var = StringVar(value="")

        # Add the "Results" button if it doesn't already exist
        self.results_button = Button(self.root, text="Results", command=self.show_results)
        self.results_button.pack()


    def show_results(self):
        """Show the voting results and the winner."""
        # Remove current widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Get the vote counts for each candidate
        john_votes = self.vote_system.get_votes("1")
        jane_votes = self.vote_system.get_votes("2")

        # Display the vote counts
        results_label = Label(self.root, text=f"John: {john_votes} votes\nJane: {jane_votes} votes")
        results_label.pack()

        # Determine the winner
        if john_votes > jane_votes:
            winner_label = Label(self.root, text="John is the winner!", fg="green")
        elif jane_votes > john_votes:
            winner_label = Label(self.root, text="Jane is the winner!", fg="green")
        else:
            winner_label = Label(self.root, text="It's a tie!", fg="orange")
        winner_label.pack()

        # Button to go back to the voting screen
        back_button = Button(self.root, text="Back to Voting", command=self.reset_screen)
        back_button.pack()

    def run(self):
        self.root.mainloop()

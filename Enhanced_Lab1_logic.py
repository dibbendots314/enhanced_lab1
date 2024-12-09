# logic

import csv

class FileManager:
    def __init__(self, file_name='votes.csv'):
        self.file_name = file_name
        self.used_ids = set()  # Initialize the set of used IDs to track during the session
        self.clear_file()  # Clear the file at the start of each session

    def clear_file(self):
        """Clear the contents of the file."""
        with open(self.file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Voter_ID', 'Candidate'])  # Recreate the header row

    def read_votes(self):
        """Read votes from the CSV file."""
        try:
            with open(self.file_name, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                return [row for row in reader]
        except FileNotFoundError:
            return []

    def write_vote(self, voter_id, candidate):
        """Write a new vote to the CSV file."""
        with open(self.file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([voter_id, candidate])

    def add_used_id(self, voter_id):
        """Add the voter ID to the used set."""
        self.used_ids.add(voter_id)

class Vote:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.votes = self.file_manager.read_votes()

    def vote(self, voter_id, candidate):
        """Cast a vote for the given voter ID and candidate."""
        if voter_id in self.file_manager.used_ids:
            raise ValueError("This ID has already voted.")
        
        # Record the vote
        self.file_manager.write_vote(voter_id, candidate)

        # Mark the voter ID as used for this session
        self.file_manager.add_used_id(voter_id)

        # Update internal votes (optional, can be done by reading the file if necessary)
        self.votes.append([voter_id, candidate])

    def get_votes(self, candidate):
        """Return the number of votes for a given candidate."""
        return sum(1 for vote in self.votes if vote[1] == candidate)


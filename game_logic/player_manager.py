import json

class PlayerManager:
    _instance = None

    @staticmethod
    def get_instance():
        """Static access method for the Singleton."""
        if PlayerManager._instance is None:
            PlayerManager()
        return PlayerManager._instance

    def __init__(self):
        """Private constructor to ensure only one instance exists."""
        if PlayerManager._instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            PlayerManager._instance = self
            self.players = {}  # Dictionary to store players (name, cluster): [score, attempts]
            self.leaderboard = []  # List to store leaderboard [(name, cluster), score]
            self.max_attempts = 2  # Max allowed attempts for each player
            self.current_player = None  # Current player (name, cluster)
            self.load_leaderboard()

    def add_player(self, name, cluster):
        """Add a new player if not exists."""
        key = (name, cluster)
        if key not in self.players:
            self.players[key] = [0, self.max_attempts]  # Default score: 0, attempts: 2
        else:
            raise ValueError(f"Player {name} from cluster {cluster} already exists.")

    def player_exists(self, name, cluster):
        """Check if a player with the given name and cluster exists."""
        return (name, cluster) in self.players

    def set_current_player(self, name, cluster):
        """Set the current player."""
        self.current_player = (name, cluster)
    
    
    def get_current_player(self):
        """Return the current player."""
        return self.current_player

    def get_remaining_attempts(self, name = None, cluster = None):
        """Return the remaining attempts for a player."""
        if name is None or cluster is None:
            # If no parameters are passed, use current player
            name, cluster = self.get_current_player()

        if self.player_exists(name, cluster):
            return self.players[(name, cluster)][1]
        return 0

    def decrement_player_attempts(self, name, cluster):
        """Decrement the attempts for a player."""
        if self.player_exists(name, cluster):
            self.players[(name, cluster)][1] -= 1

    def update_leaderboard(self, name=None, cluster=None, score=None):
        """
        Update the leaderboard with the player's score.
        If the player is already in the leaderboard, the highest score between the old score and the new score is kept.

        Parameters:
        name (str, optional): The name of the player. Defaults to None.
        cluster (str, optional): The cluster of the player. Defaults to None.
        score (int, optional): The new score of the player. Defaults to None.

        Returns:
        None
        """
        if name is None or cluster is None or score is None:
            # If no parameters are passed, update the current player
            name, cluster = self.get_current_player()
            score = self.get_player_score()

        key = (name, cluster)

        # Check if the player is already in the leaderboard
        existing_entry = next((entry for entry in self.leaderboard if entry[0] == key), None)

        if existing_entry:
            # If the player is already in the leaderboard, keep the max score
            max_score = max(existing_entry[1], score)
            self.leaderboard = [(k, max_score if k == key else s) for k, s in self.leaderboard]
        else:
            # If the player is not in the leaderboard, add them with the current score
            self.leaderboard.append((key, score))

        # Sort the leaderboard by score in descending order
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x[1], reverse=True)

        # Save the updated leaderboard
        self.save_leaderboard()
    
    def get_player_score(self):
        """
        Retrieve the score of the current player.

        This function retrieves the score of the current player from the players dictionary.
        If the current player is not set, it raises a ValueError.

        Parameters:
        None

        Returns:
        int: The score of the current player.

        Raises:
        ValueError: If the current player is not set.
        """
        if self.current_player:
            return self.players[self.get_current_player()][0]
        else:
            raise ValueError("Current player is not set.")

    def set_player_score(self, score):
        """
        Update the score of the current player.

        The function sets the score of the current player to the maximum of the given score and the current score.
        If the current player is not set, it raises a ValueError.

        Parameters:
        score (int): The score to be set for the current player.

        Returns:
        None

        Raises:
        ValueError: If the current player is not set.
        """
        if self.current_player:
            self.players[self.get_current_player()][0] = max(score, self.get_player_score())
        else:
            raise ValueError("Current player is not set.")

    def get_top_players(self, limit=5):
        """Return the top players from the leaderboard."""
        return self.leaderboard[:limit]
    
    def get_player_rank(self, name, cluster):
        """
        Get the rank of the specified player based on their score in the leaderboard.

        Parameters:
        name (str): The name of the player.
        cluster (str): The cluster the player belongs to.

        Returns:
        int: The rank of the player (1-based). If the player is not found, return -1.
        """
        key = (name, cluster)
        if key not in self.players:
            raise ValueError(f"Player {name} from cluster {cluster} does not exist.")
        
        # Sort leaderboard by score and calculate rank
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x[1], reverse=True)
        
        for rank, (player_key, score) in enumerate(sorted_leaderboard, start=1):
            if player_key == key:
                return rank
        return -1  # Return -1 if the player is not in the leaderboard

    def get_player_rank(self):
        """
        Get the rank of the specified player based on their score in the leaderboard.

        Parameters:
        name (str): The name of the player.
        cluster (str): The cluster the player belongs to.

        Returns:
        int: The rank of the player (1-based). If the player is not found, return -1.
        """
        key = self.get_current_player()
        if key not in self.players:
            name, cluster = key
            raise ValueError(f"Player {name} from cluster {cluster} does not exist.")
        
        # Sort leaderboard by score and calculate rank
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x[1], reverse=True)
        
        for rank, (player_key, score) in enumerate(sorted_leaderboard, start=1):
            if player_key == key:
                return rank
        return -1  # Return -1 if the player is not in the leaderboard
    
    def get_leaderboard(self) -> list:
        """
        Retrieve the leaderboard as a list of tuples. Each tuple contains player's name, cluster, and score.

        Parameters:
        None

        Returns:
        list: A list of tuples representing the leaderboard. Each tuple contains player's name, cluster, and score.
              The list is sorted in descending order based on the score.
        """
        return self.leaderboard

    def save_leaderboard(self):
        """
        Save the leaderboard to a file, converting tuple keys to string keys.

        This function takes the current state of the leaderboard and player data,
        converts the tuple keys to string keys, and saves the data to a JSON file.
        The leaderboard and player data are stored in a dictionary format,
        where the 'players' key contains a dictionary of player data and the 'leaderboard' key
        contains a list of tuples representing the leaderboard.

        Parameters:
        None

        Returns:
        None

        Raises:
        None
        """
        data = {
            'players': {f"{name}:{cluster}": value for (name, cluster), value in self.players.items()},
            'leaderboard': [(f"{name}:{cluster}", score) for (name, cluster), score in self.leaderboard]
        }
        with open('leaderboard.json', 'w') as file:
            json.dump(data, file)


    def load_leaderboard(self):
        """
        Load the leaderboard from a file, converting string keys back to tuple keys.

        This function reads the leaderboard data from a JSON file named 'leaderboard.json'.
        If the file exists, it loads the data and converts the string keys back to tuple keys.
        If the file does not exist, it initializes the players and leaderboard dictionaries with empty values.

        Parameters:
        None

        Returns:
        None

        Raises:
        FileNotFoundError: If the 'leaderboard.json' file does not exist.
        """
        try:
            with open('leaderboard.json', 'r') as file:
                data = json.load(file)
                # Convert string keys back to tuples
                self.players = {tuple(key.split(":")): value for key, value in data.get('players', {}).items()}
                self.leaderboard = [(tuple(key.split(":")), score) for key, score in data.get('leaderboard', [])]
        except FileNotFoundError:
            self.players = {}
            self.leaderboard = []


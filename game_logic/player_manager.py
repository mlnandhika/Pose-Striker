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

    def get_player_attempts(self, name, cluster):
        """Return the remaining attempts for a player."""
        if self.player_exists(name, cluster):
            return self.players[(name, cluster)][1]
        return 0

    def decrement_player_attempts(self, name, cluster):
        """Decrement the attempts for a player."""
        if self.player_exists(name, cluster):
            self.players[(name, cluster)][1] -= 1

    def update_leaderboard(self, name, cluster, score):
        """Update the leaderboard with the player's score."""
        key = (name, cluster)
        if self.player_exists(name, cluster):
            self.leaderboard.append((key, score))
            self.leaderboard = sorted(self.leaderboard, key=lambda x: x[1], reverse=True)  # Sort by score
            self.save_leaderboard()

    def get_top_players(self, limit=5):
        """Return the top players from the leaderboard."""
        return self.leaderboard[:limit]

    def save_leaderboard(self):
        """Save the leaderboard to a file."""
        data = {
            'players': self.players,
            'leaderboard': self.leaderboard
        }
        with open('leaderboard.json', 'w') as file:
            json.dump(data, file)

    def load_leaderboard(self):
        """Load the leaderboard from a file."""
        try:
            with open('leaderboard.json', 'r') as file:
                data = json.load(file)
                self.players = data.get('players', {})
                self.leaderboard = data.get('leaderboard', [])
        except FileNotFoundError:
            self.players = {}
            self.leaderboard = []

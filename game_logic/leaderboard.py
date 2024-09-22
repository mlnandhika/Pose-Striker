class Leaderboard:
    def __init__(self):
        self.players = []

    def add_player(self, name, score):
        self.players.append((name, score))
        self.players = sorted(self.players, key=lambda x: x[1], reverse=True)

    def get_top_players(self, limit=5):
        return self.players[:limit]

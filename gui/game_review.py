import tkinter as tk
from gui.components import ScrollableLeaderboard

class GameReview(tk.Frame):
    def __init__(self, parent, player_name, player_cluster, player_score, leaderboard, chances):
        super().__init__(parent)
        self.player_name = player_name
        self.player_cluster = player_cluster
        self.player_score = player_score
        self.leaderboard = leaderboard
        self.chances = chances
        
        # Get the player's rank in the leaderboard
        player_rank = self.get_player_rank()

        # Congratulatory message based on the player's rank
        if player_rank == 1:
            message = "You Did It!"
        elif player_rank <= 5:
            message = "You Made It!"
        elif player_rank <= 10:
            message = "Not Bad!"
        else:
            message = "Nice Try!"
        
        # Congratulation label
        self.congrats_label = tk.Label(self, text=message, font=("Arial", 24))
        self.congrats_label.pack(pady=10)
        
        # Leaderboard display
        self.leaderboard_label = tk.Label(self, text="Leaderboard", font=("Arial", 14))
        self.leaderboard_label.pack(pady=5)

        self.leaderboard_display = ScrollableLeaderboard(self)
        self.leaderboard_display.pack(pady=10)
        self.update_leaderboard()

        # Player's ranking row (only show if player is not in top 5)
        if player_rank > 5:
            self.player_ranking_label = tk.Label(self, text=f"Your Rank: {player_rank} (Score: {self.player_score})")
            self.player_ranking_label.pack(pady=10)

        # Attempts left label
        self.attempts_label = tk.Label(self, text=f"Attempts Left: {self.chances}")
        self.attempts_label.pack(pady=5)

        # Play Again button (only show if attempts are left)
        if self.chances > 0:
            self.play_again_button = tk.Button(self, text="Play Again", command=self.play_again,bg="gold2")
            self.play_again_button.pack(pady=5)
        
        # Main Menu button
        self.main_menu_button = tk.Button(self, text="Main Menu", command=self.return_to_main_menu,bg="gold2")
        self.main_menu_button.pack(pady=5)

    def update_leaderboard(self):
        top_players = self.leaderboard.get_top_players()
        self.leaderboard_display.update_leaderboard(top_players)

    def get_player_rank(self):
        for index, (name, score) in enumerate(self.leaderboard.players):
            if name == self.player_name and score == self.player_score:
                return index + 1
        return len(self.leaderboard.players) + 1

    def play_again(self):
        self.pack_forget()  # Hide review frame
        # Go back to the main game frame (this part depends on how you manage transitions)
        from gui.game_frame import GameFrame
        game_frame = GameFrame(self.master, self.player_name, self.player_cluster, self.leaderboard, self.chances)
        game_frame.pack(fill=tk.BOTH, expand=True)

    def return_to_main_menu(self):
        self.pack_forget()
        # Go back to main menu
        from gui.main_menu import MainMenu
        main_menu = MainMenu(self.master, self.leaderboard)
        main_menu.pack(fill=tk.BOTH, expand=True)

        

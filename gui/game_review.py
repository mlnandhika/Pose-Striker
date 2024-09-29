import tkinter as tk
from gui.components import ScrollableLeaderboard
from game_logic.player_manager import PlayerManager

class GameReview(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Player's rank and score have been added to the leaderboad in end_game() in game_frame.py
        # Here, we only need to get the rank
        self.pm = PlayerManager.get_instance()
        player_rank = self.pm.get_player_rank()

        # Congratulatory message based on the player's rank
        if player_rank == 1:
            message = "You Did It!"
        elif player_rank <= 5:
            message = "You Made It!"
        elif player_rank <= 10:
            message = "Not Bad!"
        else:
            message = "Nice Try!"

        # Create the leaderboard frame with background color
        leaderboard_frame = tk.Frame(self, bg="gold2", bd=0)
        leaderboard_frame.place(relx=0.5, rely=0.43, anchor=tk.CENTER, width=600, height=450)

        # Congratulation label
        self.congrats_label = tk.Label(self, text=message, font=("Arial", 50))
        self.congrats_label.pack(pady=10)
        self.congrats_label.place(relx=0.5, rely= 0.09, anchor=tk.CENTER)
        
        # Leaderboard display
        self.leaderboard_label = tk.Label(self, text="Leaderboard", font=("Arial", 20),bg="gold2")
        self.leaderboard_label.pack(pady=5)
        self.leaderboard_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.leaderboard_display = ScrollableLeaderboard(self)
        self.leaderboard_display.update_leaderboard(self.pm.get_leaderboard())
        self.leaderboard_display.pack(pady=10)
        self.leaderboard_display.place(relx=0.5, rely=0.45, anchor=tk.CENTER, width=550, height=380)

        # Player's ranking row (only show if player is not in top 5)
        if player_rank > 5:
            self.player_ranking_label = tk.Label(self, text=f"Your Rank: {player_rank} (Score: {self.pm.get_player_score()})",font=("Arial", 17))
            self.player_ranking_label.pack(pady=10)
            self.player_ranking_label.place(relx=0.5, rely=0.74, anchor=tk.CENTER)

        # Attempts left label
        chances = self.pm.get_remaining_attempts()
        self.attempts_label = tk.Label(self, text=f"Attempts Left: {chances}",font=("Arial", 17))
        self.attempts_label.pack(pady=5)
        self.attempts_label.place(relx=0.5, rely=0.79,anchor=tk.CENTER)

        # Play Again button (only show if attempts are left)
        if chances > 0:
            self.play_again_button = tk.Button(self, text="Play Again", command=self.play_again, bg="gold2")
            self.play_again_button.pack(pady=5)
            self.play_again_button.place(relx=0.7, rely=0.93, anchor=tk.CENTER, width=80, height=40)
        
        # Main Menu button
        self.main_menu_button = tk.Button(self, text="Main Menu", command=self.return_to_main_menu,bg="gold2")
        self.main_menu_button.pack(pady=5)
        self.main_menu_button.place(relx=0.3, rely=0.93, anchor=tk.CENTER, width=80, height=40)

    def play_again(self):
        self.pack_forget()  # Hide review frame
        # Go back to the main game frame (this part depends on how you manage transitions)
        from gui.game_frame import GameFrame
        game_frame = GameFrame(self.master)
        game_frame.pack(fill=tk.BOTH, expand=True)

    def return_to_main_menu(self):
        self.pack_forget()
        # Go back to main menu
        from gui.main_menu import MainMenu
        main_menu = MainMenu(self.master)
        main_menu.pack(fill=tk.BOTH, expand=True)

        

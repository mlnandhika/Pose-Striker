import tkinter as tk
from gui.components import ScrollableLeaderboard, DropdownMenu
from gui.game_frame import GameFrame
from game_logic.player_manager import PlayerManager

class MainMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        self.title = tk.Label(self, text="Pose Striker", font=("Arial", 24))
        self.title.pack(pady=10)

        # Leaderboard label
        self.leaderboard_label = tk.Label(self, text="Leaderboard", font=("Arial", 14))
        self.leaderboard_label.pack(pady=5)

        # Scrollable leaderboard
        self.leaderboard_display = ScrollableLeaderboard(self)
        self.leaderboard_display.pack(pady=10)
        self.update_leaderboard()

        # Input fields (Player Name and Cluster)
        self.name_frame = tk.Frame(self)
        self.name_frame.pack(pady=5)
        self.name_label = tk.Label(self.name_frame, text="Player Name:")
        self.name_label.pack(side=tk.LEFT)
        self.name_entry = tk.Entry(self.name_frame)
        self.name_entry.pack(side=tk.LEFT, padx=10)

        self.cluster_frame = tk.Frame(self)
        self.cluster_frame.pack(pady=5)
        self.cluster_dropdown = DropdownMenu(self.cluster_frame, ["Cluster 1", "Cluster 2", "Cluster 3"])
        
        # Start button
        self.start_button = tk.Button(self, text="Start", command=self.start_game)
        self.start_button.pack(pady=10)

    def update_leaderboard(self):
        pm = PlayerManager.get_instance()
        self.leaderboard_display.update_leaderboard(pm.get_leaderboard())

    def start_game(self):
        player_name = self.name_entry.get()
        player_cluster = self.cluster_dropdown.get()
        
        if player_name and player_cluster:
            pm = PlayerManager.get_instance()
            player_exist = pm.player_exists(player_name, player_cluster)
            chances = pm.get_remaining_attempts(player_name, player_cluster)
            if not player_exist or player_exist and chances:
                if not player_exist:
                    pm.add_player(player_name, player_cluster)
                pm.set_current_player(player_name, player_cluster)

                self.pack_forget()  # Hide main menu
                game_frame = GameFrame(self.master)
                game_frame.pack(fill=tk.BOTH, expand=True)

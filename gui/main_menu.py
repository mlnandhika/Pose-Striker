import tkinter as tk
from gui.components import ScrollableLeaderboard, DropdownMenu
from gui.game_frame import GameFrame

class MainMenu(tk.Frame):
    def __init__(self, parent, leaderboard):
        super().__init__(parent)
        self.leaderboard = leaderboard

        # Background Color
        self.config(bg="snow")

        # Title
        self.title = tk.Label(self, text="Pose Striker", font=("Impact", 24))
        self.title.pack(pady=10)

        # create the leaderboard frame
        self.create_leaderboard_frame()
        self.create_player_input_section()

    def create_player_input_section(self):
        # Input fields (Player Name and Cluster)

        # Name input
        self.name_frame = tk.Frame(self,bg="gold2")
        self.name_frame.pack(pady=5)
        self.name_frame.place (relx=0.5, rely=0.7, anchor=tk.CENTER, width=250, height=30)
        self.name_label = tk.Label(self.name_frame, text="Nama :",bg="gold2")
        self.name_label.pack(side=tk.LEFT)
        self.name_entry = tk.Entry(self.name_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=10)

        #cluster dropdown
        self.cluster_frame = tk.Frame(self,bg="gold2")
        self.cluster_frame.pack(pady=5)
        self.cluster_frame.place(relx=0.5, rely=0.76, anchor=tk.CENTER, width=250, height=50)
        self.cluster_dropdown = DropdownMenu(self.cluster_frame, ["Cluster 1", "Cluster 2", "Cluster 3"])

        # Start button
        self.start_button = tk.Button(self, text="Start", command=self.start_game,bg="OliveDrab1")
        self.start_button.pack(pady=30)
        self.start_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER, width=100, height=30)

    def create_leaderboard_frame(self):
         #Create the leaderboard frame with background color
        leaderboard_frame = tk.Frame(self, bg="gold2", bd=0)
        leaderboard_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=600, height=450)

        # Label for the leaderboard
        leaderboard_label = tk.Label(leaderboard_frame, text="LEADERBOARD", bg="gold2", fg="black",font=("Arial", 14))
        leaderboard_label.pack(pady=10)

        # Box for leaderboard content
        leaderboard_box = tk.Frame(leaderboard_frame, bg="gold2", bd=0)
        leaderboard_box.place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=580, height=380)

        # Scrollable leaderboard display
        self.leaderboard_display = ScrollableLeaderboard(leaderboard_box)
        self.leaderboard_display.place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=550, height=380)
        self.leaderboard_display.pack(pady=10)

        self.update_leaderboard()

    def update_leaderboard(self):
        self.leaderboard_display.update_leaderboard(self.leaderboard.get_top_players())

    def start_game(self):
        player_name = self.name_entry.get()
        player_cluster = self.cluster_dropdown.get()
        if player_name and player_cluster:
            self.pack_forget()  # Hide main menu
            game_frame = GameFrame(self.master, player_name, player_cluster, self.leaderboard, chances=3)
            game_frame.pack(fill=tk.BOTH, expand=True)

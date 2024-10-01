import tkinter as tk
from PIL import Image, ImageTk
from gui.components import ScrollableLeaderboard, DropdownMenu
from gui.game_frame import GameFrame
from game_logic.player_manager import PlayerManager

class MainMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Load and resize background image using Pillow
        image = Image.open(r"assets/decor/main_menu.png")
        resized_image = image.resize((1600,900), Image.LANCZOS)  # Resize image using LANCZOS

        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relx=0, y=0, relwidth=1, relheight=1)  # Make it full screen
        
        # create the leaderboard frame
        self.create_leaderboard_frame()
        self.create_player_input_section()

    def create_player_input_section(self):
        # Input fields (Player Name and Cluster)

        # Name input
        self.name_frame = tk.Frame(self, bg="gold2")
        self.name_frame.pack(pady=5)
        self.name_frame.place(relx=0.512, rely=0.79, anchor=tk.CENTER, width=240, height=30)
        self.name_label = tk.Label(self.name_frame, font='Arial 17 bold', fg="#384987", text="NAMA :", bg="gold2")
        self.name_label.pack(side=tk.LEFT)
        self.name_entry = tk.Entry(self.name_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=10)

        # Cluster dropdown
        self.cluster_frame = tk.Frame(self, bg="gold2")
        self.cluster_frame.pack(pady=5)
        self.cluster_frame.place(relx=0.5, rely=0.84, anchor=tk.CENTER, width=300, height=40)
        self.cluster_dropdown = DropdownMenu(self.cluster_frame, ["Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4", 
                                                                  "Cluster 5", "Cluster 6", "Cluster 7", "Cluster 8", 
                                                                  "Cluster 9", "Cluster 10", "Cluster 11", "Cluster 12", 
                                                                  "Cluster 13", "Cluster 14", "Cluster 15", "Cluster 16", 
                                                                  "Cluster 17", "Cluster 18", "Cluster 19", "Cluster 20", 
                                                                  "Cluster 21", "Cluster 22"])

        # Load start button image
        start_image = Image.open(r"assets/decor/start.png")
        start_image_resized = start_image.resize((150, 40), Image.LANCZOS)  # Resize if needed
        self.start_image_tk = ImageTk.PhotoImage(start_image_resized)

        # Start button with image
        self.start_button = tk.Button(self, image=self.start_image_tk, command=self.start_game, bg="#EC008C", bd=0)
        self.start_button.pack(pady=30)
        self.start_button.place(relx=0.5, rely=0.92, anchor=tk.CENTER, width=150, height=40)


    def create_leaderboard_frame(self):

        # Box for leaderboard content
        leaderboard_box = tk.Frame(self, bg="gold2", bd=0)
        leaderboard_box.place(relx=0.5, rely=0.47, anchor=tk.CENTER, width=580, height=380)

        # Scrollable leaderboard display
        self.leaderboard_display = ScrollableLeaderboard(leaderboard_box)
        self.leaderboard_display.place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=550, height=380)
        self.leaderboard_display.pack(pady=10)

        self.update_leaderboard()

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

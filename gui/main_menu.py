import tkinter as tk
from PIL import Image, ImageTk
from gui.components import ScrollableLeaderboard, DropdownMenu
from gui.game_frame import GameFrame
from game_logic.player_manager import PlayerManager

class MainMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Background Color
        self.config(bg="#111")

        # Title
        self.title = tk.Label(self,fg="snow", text="    Pose Striker    ", font='FreeMono 50 bold',bg="#111")
        self.title.pack(pady=10)

        # create the leaderboard frame
        self.create_leaderboard_frame()
        self.create_player_input_section()

        # Memuat gambar PNG 1
        Image.MAX_IMAGE_PIXELS = None
        self.image1 = Image.open(r"C:\\Users\\acern\\Hansel\\Pose-Striker\\assets\\main\\1.png")
        self.new_size1 = (200, 200)  # Ukuran gambar yang diubah
        self.resized_image1 = self.image1.resize(self.new_size1, Image.Resampling.LANCZOS)
        self.photo1 = ImageTk.PhotoImage(self.resized_image1)
        self.image_label1 = tk.Label(self, image=self.photo1, bg="#111", highlightthickness=0)
        self.image_label1.place(relx=0.85, rely=0.99, anchor=tk.SW, width=200, height=200)

        # Memuat gambar PNG 2
        self.image2 = Image.open(r"C:\\Users\\acern\\Hansel\\Pose-Striker\\assets\\main\\2.png")
        self.new_size2 = (200, 200)  # Ukuran gambar yang diubah
        self.resized_image2 = self.image2.resize(self.new_size2, Image.Resampling.LANCZOS)
        self.photo2 = ImageTk.PhotoImage(self.resized_image2)
        self.image_label2 = tk.Label(self, image=self.photo2, bg="#111", highlightthickness=0)
        self.image_label2.place(relx=0.70, rely=0.99, anchor=tk.SW, width=200, height=200)

        # Memuat gambar PNG 3
        self.image3 = Image.open(r"C:\\Users\\acern\\Hansel\\Pose-Striker\\assets\\main\\3.png")
        self.new_size3 = (200, 200)  # Ukuran gambar yang diubah
        self.resized_image3 = self.image3.resize(self.new_size3, Image.Resampling.LANCZOS)
        self.photo3 = ImageTk.PhotoImage(self.resized_image3)
        self.image_label3 = tk.Label(self, image=self.photo3, bg="#111", highlightthickness=0)
        self.image_label3.place(relx=0.20, rely=0.99, anchor=tk.SW, width=200, height=200)

        # Memuat gambar PNG 4
        self.image4 = Image.open(r"C:\\Users\\acern\\Hansel\\Pose-Striker\\assets\\main\\4.png")
        self.new_size4 = (200, 200)  # Ukuran gambar yang diubah
        self.resized_image4 = self.image4.resize(self.new_size4, Image.Resampling.LANCZOS)
        self.photo4 = ImageTk.PhotoImage(self.resized_image4)
        self.image_label4 = tk.Label(self, image=self.photo4, bg="#111", highlightthickness=0)
        self.image_label4.place(relx=0.01, rely=0.99, anchor=tk.SW, width=200, height=200)

        # Memuat gambar PNG 5
        self.image5 = Image.open(r"C:\\Users\\acern\\Hansel\\Pose-Striker\\assets\\main\\Logo_Universitas_Brawijaya.png")
        self.new_size5 = (100,100)  # Ukuran gambar yang diubah
        self.resized_image5 = self.image5.resize(self.new_size5, Image.Resampling.LANCZOS)
        self.photo5 = ImageTk.PhotoImage(self.resized_image5)
        self.image_label5 = tk.Label(self, image=self.photo5, bg="#111", highlightthickness=0)
        self.image_label5.place(relx=0.01, rely=0.13, anchor=tk.SW, width=100, height=100)

        # Memuat gambar PNG 4
        self.image6 = Image.open(r"C:\\Users\\acern\\Hansel\\Pose-Striker\\assets\\main\\Filkom_UB.png")
        self.new_size6 = (200, 100)  # Ukuran gambar yang diubah
        self.resized_image6 = self.image6.resize(self.new_size6, Image.Resampling.LANCZOS)
        self.photo6 = ImageTk.PhotoImage(self.resized_image6)
        self.image_label6 = tk.Label(self, image=self.photo6, bg="#111", highlightthickness=0)
        self.image_label6.place(relx=0.08, rely=0.13, anchor=tk.SW, width=200, height=100)

        # Memuat gambar PNG 4
        self.image7 = Image.open(r"C:\\Users\\acern\\Hansel\\Pose-Striker\\assets\\main\\Logo_Robotiik_HD_Logo.png")
        self.new_size7 = (100, 100)  # Ukuran gambar yang diubah
        self.resized_image7 = self.image7.resize(self.new_size7, Image.Resampling.LANCZOS)
        self.photo7 = ImageTk.PhotoImage(self.resized_image7)
        self.image_label7 = tk.Label(self, image=self.photo7, bg="#111", highlightthickness=0)
        self.image_label7.place(relx=0.21, rely=0.13, anchor=tk.SW, width=100, height=100)

    def create_player_input_section(self):
        # Input fields (Player Name and Cluster)

        # Name input
        self.name_frame = tk.Frame(self,bg="#111")
        self.name_frame.pack(pady=5)
        self.name_frame.place (relx=0.516, rely=0.7, anchor=tk.CENTER, width=240, height=30)
        self.name_label = tk.Label(self.name_frame, font='Arial 17 bold',fg="snow",text="NAMA :",bg="#111")
        self.name_label.pack(side=tk.LEFT)
        self.name_entry = tk.Entry(self.name_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=10)

        #cluster dropdown
        self.cluster_frame = tk.Frame(self,bg="#111")
        self.cluster_frame.pack(pady=5)
        self.cluster_frame.place(relx=0.5, rely=0.76, anchor=tk.CENTER, width=300, height=40)
        self.cluster_dropdown = DropdownMenu(self.cluster_frame, ["Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4", "Cluster 5", "Cluster 6", "Cluster 7", "Cluster 8", "Cluster 9", "Cluster 10", "Cluster 11", "Cluster 12", "Cluster 13", "Cluster 14", "Cluster 15", "Cluster 16", "Cluster 17", "Cluster 18", "Cluster 19", "Cluster 20", "Cluster 21", "Cluster 22"])

        # Start button
        self.start_button = tk.Button(self, text="START", font='FreeMono 17',command=self.start_game,bg="#EC008C")
        self.start_button.pack(pady=30)
        self.start_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER, width=100, height=30)

    def create_leaderboard_frame(self):
         #Create the leaderboard frame with background color
        leaderboard_frame = tk.Frame(self, bg="gold2", bd=0)
        leaderboard_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=600, height=450)

        # Label for the leaderboard
        leaderboard_label = tk.Label(leaderboard_frame, text="LEADERBOARD", bg="gold2", fg="black",font='Arial 23 bold')
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

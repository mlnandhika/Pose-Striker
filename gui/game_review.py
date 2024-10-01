import tkinter as tk
from gui.components import ScrollableLeaderboard
from game_logic.player_manager import PlayerManager
from PIL import Image, ImageTk


class GameReview(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Load and resize background image using Pillow
        image = Image.open(r"assets/decor/game review.png")
        resized_image = image.resize((1600, 900), Image.LANCZOS)  # Resize image using LANCZOS

        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relx=0, y=0, relwidth=1, relheight=1)  # Make it full screen

        # Player's rank and score have been added to the leaderboard in end_game() in game_frame.py
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

        # Congratulatory image based on the player's rank
        if player_rank == 1:
            image_message = r"assets/decor/did.png"  # Path for the first rank image
        elif player_rank <= 5:
            image_message = r"assets/decor/made.png"  # Path for the rank 2-5 image
        elif player_rank <= 10:
            image_message = r"assets/decor/not.png"  # Path for the rank 6-10 image
        else:
            image_message = r"assets/decor/nice.png"  # Path for the rank 11+ image

        # Load and display the congratulatory image
        congrats_image = Image.open(image_message)
        congrats_resized_image = congrats_image.resize((412, 105), Image.LANCZOS)  # Adjust the size as needed
        self.congrats_image = ImageTk.PhotoImage(congrats_resized_image)

        self.congrats_label = tk.Label(self, image=self.congrats_image, bg="#D6AC18")
        self.congrats_label.pack(pady=0)
        self.congrats_label.place(relx=0.5, rely=0.09, anchor=tk.CENTER)

        self.leaderboard_display = ScrollableLeaderboard(self)
        self.leaderboard_display.update_leaderboard(self.pm.get_leaderboard())
        self.leaderboard_display.place(relx=0.5, rely=0.48, anchor=tk.CENTER, width=550, height=357)

        # Player's ranking row (only show if player is not in top 5)
        if player_rank > 5:
            self.player_ranking_label = tk.Label(self, text=f"Your Rank: {player_rank} (Score: {self.pm.get_player_score()})", font=('Arial 22 bold'), fg="#384987", bg="#E6CF00")
            self.player_ranking_label.pack(pady=10)
            self.player_ranking_label.place(relx=0.5, rely=0.76, anchor=tk.CENTER)

        # Attempts left label
        chances = self.pm.get_remaining_attempts()
        self.attempts_label = tk.Label(self, text=f"Attempts Left: {chances}", font=('Arial 17 bold'), fg="#384987", bg="#E6CF00")
        self.attempts_label.pack(pady=5)
        self.attempts_label.place(relx=0.5, rely=0.795, anchor=tk.CENTER)

        # Play Again button (only show if attempts are left)
        if chances > 0:
            self.play_again_button_image = Image.open(r"assets/decor/play again.png")  # Path to play again image
            self.play_again_button_image_resized = self.play_again_button_image.resize((131, 35), Image.LANCZOS)  # Resize
            self.play_again_button_image_tk = ImageTk.PhotoImage(self.play_again_button_image_resized)

            self.play_again_button = tk.Button(self, image=self.play_again_button_image_tk, command=self.play_again, bg="gold2")
            self.play_again_button.pack(pady=5)
            self.play_again_button.place(relx=0.6, rely=0.88, anchor=tk.CENTER, width=150, height=45)

            # Main Menu button
            self.main_menu_button_image = Image.open(r"assets/decor/menu.png")  # Path to main menu image
            self.main_menu_button_image_resized = self.main_menu_button_image.resize((131, 35), Image.LANCZOS)  # Resize
            self.main_menu_button_image_tk = ImageTk.PhotoImage(self.main_menu_button_image_resized)

            self.main_menu_button = tk.Button(self, image=self.main_menu_button_image_tk, command=self.return_to_main_menu, bg="gold2")
            self.main_menu_button.pack(pady=5)
            self.main_menu_button.place(relx=0.4k, rely=0.88, anchor=tk.CENTER, width=150, height=45)

        else:
            self.main_menu_button_image = Image.open(r"assets/decor/menu.png")  # Path to main menu image
            self.main_menu_button_image_resized = self.main_menu_button_image.resize((131, 35), Image.LANCZOS)  # Resize
            self.main_menu_button_image_tk = ImageTk.PhotoImage(self.main_menu_button_image_resized)

            self.main_menu_button = tk.Button(self, image=self.main_menu_button_image_tk, command=self.return_to_main_menu, bg="gold2")
            self.main_menu_button.pack(pady=5)
            self.main_menu_button.place(relx=0.5, rely=0.88, anchor=tk.CENTER, width=150, height=45)

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

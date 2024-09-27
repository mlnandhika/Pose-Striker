import tkinter as tk

from camera.camera_feed import CameraFeed
from game_logic.player_manager import PlayerManager
from PIL import Image, ImageTk
import threading
import time

class GameFrame(tk.Frame):
    def __init__(self, parent, timer_running=True):
        super().__init__(parent)
        self.time_left = 3  # Time limit for the game

        # Display score and time left
        pm = PlayerManager.get_instance()
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(pady=5)
        self.score_label = tk.Label(self.top_frame, text=f"Score: {pm.get_player_score()}")
        self.score_label.pack(side=tk.LEFT, padx=10)
        self.timer_label = tk.Label(self.top_frame, text=f"Time left: {self.time_left}")
        self.timer_label.pack(side=tk.LEFT, padx=10)

        # Reference image and video feed
        self.middle_frame = tk.Frame(self)
        self.middle_frame.pack(pady=10)

        self.reference_img = Image.open("assets/reference_poses/dummy_pose1.jpg")
        self.reference_img = self.reference_img.resize((200, 200), resample=3)
        self.reference_imgtk = ImageTk.PhotoImage(self.reference_img)
        self.reference_label = tk.Label(self.middle_frame, image=self.reference_imgtk)
        self.reference_label.pack(side=tk.LEFT, padx=20)

        self.video_label = tk.Label(self.middle_frame)
        self.video_label.pack(side=tk.LEFT, padx=20)

        self.camera_feed = CameraFeed(self.video_label)
        self.timer_running = timer_running
        threading.Thread(target=self.update_timer, daemon=True).start()

        # Give up button
        self.give_up_button = tk.Button(self, text="Give Up", command=self.end_game)
        self.give_up_button.pack(pady=10)

    def update_timer(self):
        while self.time_left > 0 and self.timer_running:
            time.sleep(1)
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}")
        if self.timer_running: # this is executed upon timer timeout, not upon Give Up button press
            self.end_game()

    def end_game(self):
        pm = PlayerManager.get_instance()
        pm.decrement_player_attempts(*pm.get_current_player())
        pm.update_leaderboard()

        self.timer_running = False
        self.camera_feed.stop()
        self.pack_forget()

        # Transition to session review
        from gui.game_review import GameReview
        game_review = GameReview(self.master)
        game_review.pack(fill=tk.BOTH, expand=True)

    def change_ref_photo(self):
        pass
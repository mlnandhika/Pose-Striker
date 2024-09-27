import tkinter as tk

from camera.camera_feed import CameraFeed
from game_logic.player_manager import PlayerManager
from game_logic.game_logic import GameLogic
from PIL import Image, ImageTk
import threading
import time
import os

class GameFrame(tk.Frame):
    def __init__(self, parent, timer_running=True):
        super().__init__(parent)
        self.time_left = 90  # Time limit for the game

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

        # Define the possible extensions
        extensions = ['.png', '.jpg', '.jpeg']

        # Create the list of reference images
        reference_poses_dir = 'assets/reference_poses/'
        self.reference_images = [
            f'{reference_poses_dir}dummy_pose{str(i).zfill(2)}{ext}'
            for i in range(1, 21)
            for ext in extensions
            if os.path.exists(f'{reference_poses_dir}dummy_pose{str(i).zfill(2)}{ext}')
        ]
        self.pose_id = 0

        self.reference_img = Image.open(self.reference_images[self.pose_id])
        # self.reference_img = self.reference_img.resize((200, 200), resample=3)
        self.reference_imgtk = ImageTk.PhotoImage(self.reference_img)
        self.reference_label = tk.Label(self.middle_frame, image=self.reference_imgtk)
        self.reference_label.pack(side=tk.LEFT, padx=20)

        self.video_label = tk.Label(self.middle_frame)
        self.video_label.pack(side=tk.LEFT, padx=20)

        self.camera_feed = CameraFeed(self.video_label)
        self.timer_running = timer_running
        threading.Thread(target=self.update_timer, daemon=True).start()

        # Give up button
        self.give_up_button = tk.Button(self, text="Give Up", command=self.end_game,bg="gold2")
        self.give_up_button.pack(pady=10)

        # Game Logic initialization
        self.game_logic = GameLogic(self.reference_images, self.camera_feed, self.update_score)
        self.game_logic.start_game()

    def update_timer(self):
        while self.time_left > 0 and self.timer_running:
            time.sleep(1)
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}")
        if self.timer_running: # this is executed upon timer timeout, not upon Give Up button press
            self.end_game()
    
    def update_score(self):
        pm = PlayerManager.get_instance()
        self.score_label.config(text=f"Score: {pm.get_player_score()}")
        self.change_ref_photo()

    def end_game(self):
        pm = PlayerManager.get_instance()
        pm.decrement_player_attempts(*pm.get_current_player())
        pm.update_leaderboard()

        self.game_logic.end_game()
        self.timer_running = False
        self.camera_feed.stop()
        self.pack_forget()

        # Transition to session review
        from gui.game_review import GameReview
        game_review = GameReview(self.master)
        game_review.pack(fill=tk.BOTH, expand=True)

    def change_ref_photo(self):
        self.pose_id += 1
        self.pose_id %= len(self.reference_images)

        # Step 1: Load a new image
        self.reference_img = Image.open(self.reference_images[self.pose_id])

        # Step 2: Create a new ImageTk.PhotoImage object
        self.reference_imgtk = ImageTk.PhotoImage(self.reference_img)

        # Step 3: Update the label to display the new image
        self.reference_label.config(image=self.reference_imgtk)

        # Step 4: Keep a reference to the new image to avoid garbage collection
        self.reference_label.image = self.reference_imgtk
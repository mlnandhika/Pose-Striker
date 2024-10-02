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
        self.time_left = 60  # Time limit for the game

        # Load and resize background image using Pillow
        image = Image.open(r"assets/decor/game frame.png")
        resized_image = image.resize((1600,900), Image.LANCZOS)  # Resize image using LANCZOS

        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relx=0, y=0, relwidth=1, relheight=1)  # Make it full screen

        pm = PlayerManager.get_instance()

        # Middle frame for reference image, score, timer, and combo
        self.middle_frame = tk.Frame(self)
        self.middle_frame.pack(pady=0)  # Set pady to 0 for no vertical padding

        # Define the possible extensions
        extensions = ['.png', '.jpg', '.jpeg', '.webp']

        # Create the list of reference images
        reference_poses_dir = 'assets/reference_poses/'
        self.reference_images = [os.path.join(reference_poses_dir, file) for file in os.listdir(reference_poses_dir) if os.path.splitext(file)[1].lower() in extensions]

        self.pose_id = 0

        # Step 1: Load a new image
        self.reference_img = Image.open(self.reference_images[self.pose_id])
        self.reference_img = self.reference_img.resize((700, 525), resample=3)

        # Step 2: Create a new ImageTk.PhotoImage object
        self.reference_imgtk = ImageTk.PhotoImage(self.reference_img)

        # Reference label without background color
        self.reference_label = tk.Label(self.middle_frame, image=self.reference_imgtk)
        self.reference_label.pack(side=tk.LEFT, padx=0)  # Set padx to 0 for no horizontal paddin

        # Frame for score, timer, and combo inside reference image
        self.overlay_frame = tk.Frame(self.middle_frame)
        self.overlay_frame.place(x=20, y=20)

        # Score label (Top-left)
        self.score_label = tk.Label(self.overlay_frame, text=f"Score: {pm.get_player_score()}", font=("Arial", 30))
        self.score_label.pack(side=tk.LEFT, padx=10)

        # Combo label (Top-right)
        self.combo_label = tk.Label(self.overlay_frame, text="", font=("Arial", 30))
        self.combo_label.pack(side=tk.LEFT, padx=50)

        # Timer label (Centered)
        self.timer_label = tk.Label(self.overlay_frame, text=f"Time left: {self.time_left}", font=("Arial", 30))
        self.timer_label.pack(side=tk.LEFT, padx=70)

        # Pose label
        self.match_status_label = tk.Label(self.middle_frame, text="No match", font=("Arial", 30), fg="red")
        self.match_status_label.pack(side=tk.TOP, pady=0)

        # Video feed label without background color
        self.video_label = tk.Label(self.middle_frame, width=750, height=750)
        self.video_label.pack(side=tk.RIGHT, padx=0)  # Set padx to 0 for no horizontal padding

        self.camera_feed = CameraFeed(self.video_label)
        self.timer_running = timer_running
        threading.Thread(target=self.update_timer, daemon=True).start()

        # Skip Pose button
        self.skip_pose_button = tk.Button(self, text="Skip Pose", command=self.skip_pose, bg="gold2")
        self.skip_pose_button.place(relx=0.46, rely=0.85, anchor=tk.CENTER, width=100, height=30)

        # Give up button
        self.give_up_button = tk.Button(self, text="Give Up", command=self.end_game, bg="#C7253E")
        self.give_up_button.place(relx=0.55, rely=0.85, anchor=tk.CENTER, width=100, height=30)

        # Game Logic initialization
        self.game_logic = GameLogic(self.reference_images, self.camera_feed, self.update_score, self.update_combo_text, self.update_match_status)
        self.game_logic.start_game()

    def update_timer(self):
        while self.time_left > 0 and self.timer_running:
            time.sleep(1)
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}")
        if self.timer_running:  # this is executed upon timer timeout, not upon Give Up button press
            self.end_game()

    def update_score(self):
        pm = PlayerManager.get_instance()
        self.score_label.config(text=f"Score: {pm.get_player_score()}")
        self.change_ref_photo()

    def update_combo_text(self, combo):
        if combo > 1:
            self.combo_label.config(text=f'{combo}x')
        else:
            self.combo_label.config(text="")
    
    def update_match_status(self, match):
        if match:
            self.match_status_label.config(text="Pose Match", fg="green")
        else:
            self.match_status_label.config(text="No match", fg="red")

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

    def skip_pose(self):
        self.change_ref_photo()
        self.game_logic.next_photo()

    def change_ref_photo(self):
        self.pose_id += 1
        self.pose_id %= len(self.reference_images)

        # Step 1: Load a new image
        self.reference_img = Image.open(self.reference_images[self.pose_id])
        self.reference_img = self.reference_img.resize((700, 525), resample=3)

        # Step 2: Create a new ImageTk.PhotoImage object
        self.reference_imgtk = ImageTk.PhotoImage(self.reference_img)

        # Step 3: Update the label to display the new image
        self.reference_label.config(image=self.reference_imgtk)

        # Step 4: Keep a reference to the new image to avoid garbage collection
        self.reference_label.image = self.reference_imgtk

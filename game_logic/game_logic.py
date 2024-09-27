import threading
import time
import cv2
from game_logic.pose_detector import PoseDetector
from game_logic.player_manager import PlayerManager

def current_time_ms():
    return round(time.time() * 1000)

class GameLogic:
    def __init__(self, reference_images, camera_feed, on_score_update):
        """
        Initialize GameLogic.

        Parameters:
        reference_images (list): List of paths to reference images.
        camera_feed (CameraFeed): Object to get live camera feed.
        on_score_update (function): Callback to update the score in the UI.
        """
        self.game_running = True
        self.pm = PlayerManager.get_instance()
        self.reference_images = reference_images
        self.camera_feed = camera_feed
        self.on_score_update = on_score_update
        self.pose_id = 0
        self.combo_timeout = 5000
        self.last_match_time = 0
        self.max_combo = 10
        self.score_multiplier = 1  # Adjust this value to control score multiplier

        # Load initial reference image and pose detector
        self.current_reference_image = cv2.imread(self.reference_images[self.pose_id])
        self.pose_detector = PoseDetector()

    def compare_poses(self):
        """
        Compare the pose from the camera feed with the reference pose.
        Display the reference pose and live pose with landmarks drawn.
        """
        reference_pose_img, reference_pose = self.pose_detector.get_pose_img_and_landmarks(self.current_reference_image)

        while self.game_running:
            img = self.camera_feed.get_frame()
            live_pose_img, live_pose = self.pose_detector.get_pose_img_and_landmarks(img)

            # Display both images side by side
            # cv2.imshow('Reference Pose', reference_img_with_landmarks)
            cv2.imshow('Live Pose', live_pose_img)
            cv2.imshow('Ref Pose', reference_pose_img)

            # Compare poses
            if len(live_pose) != 0 and len(reference_pose) != 0:
                match = self.pose_detector.compare_pose(reference_pose, live_pose)
                if match:
                    self.last_match_time = current_time_ms()  # Reset combo timer
                    self.update_score()

                    # Load a new reference image when a pose is successfully matched
                    self.pose_id = (self.pose_id + 1) % len(self.reference_images)
                    self.current_reference_image = cv2.imread(self.reference_images[self.pose_id])
                    reference_pose = self.pose_detector.get_pose_landmarks(self.current_reference_image)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.game_running = False

        cv2.destroyAllWindows()

    def update_score(self):
        """
        Update player score based on the current multiplier and combo status.
        """
        if self.is_combo():
            self.score_multiplier += 1
            self.score_multiplier %= self.max_combo + 1
        else:
            self.score_multiplier = 1  # Reset multiplier if no consecutive match

        gain = 1 * self.score_multiplier
        new_score = self.pm.get_player_score() + gain
        self.pm.set_player_score(new_score)
        self.on_score_update()  # Callback to update score text in the UI

    def start_game(self):
        """
        Start the game logic in a separate thread.
        """
        threading.Thread(target=self.compare_poses, daemon=True).start()
    
    def is_combo(self):
        """
        Check if the player has made a consecutive match within the given timeout.
        """
        current_time = current_time_ms()
        if current_time - self.last_match_time < self.combo_timeout:
            return True
        else:
            self.last_match_time = current_time
            return False

    def end_game(self):
        """
        Logic for ending the game and decreasing chances after the session ends.
        """
        self.game_running = False

import threading
import random
from game_logic.pose_comparison import PoseDetector

class GameLogic:
    def __init__(self, reference_images, camera_feed, on_score_update, on_chances_update, chances):
        """
        Initialize GameLogic.

        Parameters:
        reference_images (list): List of paths to reference images.
        camera_feed (CameraFeed): Object to get live camera feed.
        on_score_update (function): Callback to update the score in the UI.
        on_chances_update (function): Callback to update chances in the UI.
        chances (int): Number of chances (attempts) the player has.
        """
        self.reference_images = reference_images
        self.camera_feed = camera_feed
        self.pose_detector = PoseDetector()
        self.on_score_update = on_score_update
        self.on_chances_update = on_chances_update
        self.score = 0
        self.chances = chances
        self.current_reference_image = random.choice(self.reference_images)

    def compare_poses(self):
        """
        Compare the pose from the camera feed with the reference pose.
        """
        reference_pose = self.pose_detector.find_pose_from_image(self.current_reference_image)

        while True:
            live_pose = self.camera_feed.capture_frame()
            if live_pose is not None:
                match = self.pose_detector.compare_pose(reference_pose, live_pose)
                if match:
                    self.score += 1
                    self.on_score_update(self.score)

                    # Load a new reference image when a pose is successfully matched
                    self.current_reference_image = random.choice(self.reference_images)
                    reference_pose = self.pose_detector.find_pose_from_image(self.current_reference_image)

    def start_game(self):
        """
        Start the game logic in a separate thread.
        """
        threading.Thread(target=self.compare_poses, daemon=True).start()

    def end_game(self):
        """
        Logic for ending the game and decreasing chances after the session ends.
        """
        if self.chances > 0:
            self.chances -= 1
        self.on_chances_update(self.chances)

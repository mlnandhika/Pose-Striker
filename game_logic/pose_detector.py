import cv2
import mediapipe as mp
import math
import time

class PoseDetector:
    def __init__(self, static_image_mode=False, model_complexity=1, smooth=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detection_con=0.5, track_con=0.5):
        """
        Initializes the PoseDetector object with the specified parameters.

        Parameters:
        mode (bool, optional): Whether to use static image mode. Defaults to False.
        model_complexity (int, optional): Complexity of the pose detection model. Defaults to 2.
        smooth (bool, optional): Whether to smooth the landmarks. Defaults to True.
        enable_segmentation (bool, optional): Enable pose segmentation. Defaults to False.
        smooth_segmentation (bool, optional): Whether to smooth the segmentation. Defaults to True.
        detection_con (float, optional): Minimum detection confidence threshold. Defaults to 0.5.
        track_con (float, optional): Minimum tracking confidence threshold. Defaults to 0.5.
        """
        self.pose = mp.solutions.pose.Pose(static_image_mode=static_image_mode,
                                           model_complexity=model_complexity,
                                           smooth_landmarks=smooth,
                                           enable_segmentation=enable_segmentation,
                                           smooth_segmentation=smooth_segmentation,
                                           min_detection_confidence=detection_con,
                                           min_tracking_confidence=track_con)
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None
        self.landmarks = []
        self.complete_landmarks = []
        self.final_landmarks = []
        self.max_estimation_attempts = 10  # Max attempts for pose estimation

    def get_pose_img(self, img, reprocess=True):
        """
        Detects and draws the pose on the input image.

        Parameters:
        img (numpy.ndarray): Input image in BGR format.

        Returns:
        numpy.ndarray: Image with pose landmarks drawn.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if reprocess:
            self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        return img

    def get_pose_landmarks(self, img, draw=False):
        """
        Detects pose landmarks from the input image and optionally draws the keypoints.

        Parameters:
        img (numpy.ndarray): Input image in BGR format.
        draw (bool, optional): Whether to draw the keypoints. Defaults to False.

        Returns:
        list: A list of tuples (ID, x, y) for each detected landmark.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        self.landmarks = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.landmarks.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.landmarks

    def get_complete_pose_landmarks(self, img, required_landmarks=None):
        """
        Detects and returns complete pose landmarks from the input image. If the required landmarks are not detected,
        it continuously captures frames until all required landmarks are found.

        Parameters:
        img (numpy.ndarray): Input image in BGR format.
        required_landmarks (list, optional): List of landmark IDs required for a complete pose. Defaults to [11, 12, 13, 14, 15, 16, 23, 24].

        Returns:
        list: A list of tuples (ID, x, y) for each detected landmark.
        """
        if required_landmarks is None:
            required_landmarks = [11, 12, 13, 14, 15, 16, 19, 20, 23, 24]

        attempts = 0
        current_landmarks = self.get_pose_landmarks(img)
        self.complete_landmarks = current_landmarks
        prev_n_fulfilled = 0
        n_fulfilled, is_complete = self.is_pose_complete(current_landmarks, required_landmarks)

        while not is_complete and attempts < self.max_estimation_attempts:
            prev_n_fulfilled = n_fulfilled

            current_landmarks = self.get_pose_landmarks(img)
            n_fulfilled, is_complete = self.is_pose_complete(self.complete_landmarks, required_landmarks)

            # If the current estimation than the previous, update the best landmarks
            if n_fulfilled > prev_n_fulfilled:
                self.complete_landmarks = current_landmarks

            attempts += 1

        if not is_complete:
            raise Exception('Cannot get complete landmarks for the image!')

        # print(self.complete_landmarks)
        return self.complete_landmarks

    def get_pose_img_and_landmarks(self, img):
        """
        Detects pose landmarks and draws them on the input image.

        Parameters:
        img (numpy.ndarray): Input image in BGR format.

        Returns:
        tuple: (img, landmarks) - The image with pose landmarks drawn and a list of landmark tuples (ID, x, y).
        """
        self.final_landmarks = self.get_complete_pose_landmarks(img)
        img = self.get_pose_img(img, reprocess=False)
        return img, self.final_landmarks

    def find_angle(self, img, p1, p2, p3, draw=True):
        """
        Calculates the angle between three points.

        Parameters:
        img (numpy.ndarray): Input image for drawing.
        p1, p2, p3 (int): IDs of the three keypoints forming the angle.
        draw (bool, optional): Whether to draw the angle and lines on the image. Defaults to True.

        Returns:
        float: The angle in degrees between the three points.
        """
        x1, y1 = self.landmarks[p1][1:]
        x2, y2 = self.landmarks[p2][1:]
        x3, y3 = self.landmarks[p3][1:]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        angle = angle + 360 if angle < 0 else angle

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

    def compare_pose(self, pose1, pose2, threshold=23):
        """
        Compares two poses by checking the angles formed by various keypoints.

        Parameters:
        pose1, pose2 (list): List of landmarks from the two poses.
        threshold (int, optional): Maximum angle difference allowed for a match. Defaults to 25.

        Returns:
        bool: True if the poses match within the given threshold, False otherwise.
        """
        angles_to_compare = [
            (11, 13, 15),  # Left elbow
            (12, 14, 16),  # Right elbow
            (13, 11, 23),  # Left shoulder-hip
            (14, 12, 24),  # Right shoulder-hip
            (11, 12, 24),  # Shoulder-torso
            (12, 11, 23),  # Shoulder-torso reverse
        ]

        for p1, p2, p3 in angles_to_compare:
            angle1 = self.__calculate_angle(pose1, p1, p2, p3)
            angle2 = self.__calculate_angle(pose2, p1, p2, p3)
            print(f'angle{abs(angle1 - angle2)}')
            if abs(angle1 - angle2) > threshold:
                return False
        return True

    def is_pose_complete(self, landmarks, required_landmarks):
        """
        Check if all required landmarks are detected.

        Parameters:
        landmarks (list): List of detected landmarks.
        required_landmarks (list): List of landmark indices required for a complete pose.

        Returns:
        bool: True if all required landmarks are present, False otherwise.
        """
        detected_landmarks = [lm[0] for lm in landmarks]
        n_fulfilled = len(required_landmarks)
        for req in required_landmarks:
            if req not in detected_landmarks:
                n_fulfilled -= 1
        return (n_fulfilled, n_fulfilled == len(required_landmarks))

    def __calculate_angle(self, pose, p1, p2, p3):
        """
        Helper function to calculate the angle between three keypoints.

        Parameters:
        pose (list): List of landmarks.
        p1, p2, p3 (int): IDs of the keypoints forming the angle.

        Returns:
        float: Angle in degrees.
        """
        x1, y1 = pose[p1][1:]
        x2, y2 = pose[p2][1:]
        x3, y3 = pose[p3][1:]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        return angle + 360 if angle < 0 else angle

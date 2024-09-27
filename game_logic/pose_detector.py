import cv2
import mediapipe as mp
import time
import math
import os
import random

class PoseDetector():
    def __init__(self, mode=False, model_complexity=2, smooth=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detection_con=0.5, track_con=0.5):
        """
        Initializes a PoseDetector object with the specified parameters.

        Parameters:
        mode (bool, optional): A flag indicating whether to use static image mode. Defaults to False.
        model_complexity (int, optional): The complexity of the pose detection model. Defaults to 2.
        smooth (bool, optional): A flag indicating whether to smooth the landmarks. Defaults to True.
        enable_segmentation (bool, optional): A flag indicating whether to enable pose segmentation. Defaults to False.
        smooth_segmentation (bool, optional): A flag indicating whether to smooth the pose segmentation. Defaults to True.
        detection_con (float, optional): The minimum detection confidence threshold. Defaults to 0.5.
        track_con (float, optional): The minimum tracking confidence threshold. Defaults to 0.5.

        Returns:
        None
        """
        self.mode = mode
        self.model_complexity = model_complexity
        self.smooth = smooth
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detection_con = detection_con
        self.track_con = track_con

        self.mpDraw = mp.solutions.drawing_utils

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode,
                                     model_complexity=self.model_complexity,
                                     smooth_landmarks=self.smooth,
                                     enable_segmentation=self.enable_segmentation,
                                     smooth_segmentation=self.smooth_segmentation,
                                     min_detection_confidence=self.detection_con,
                                     min_tracking_confidence=self.track_con)
        
    def get_pose_img(self, img, draw=True):
        """
        Detects and optionally draws the pose in the input image.

        Parameters:
        img (numpy.ndarray): The input image in BGR format. The function converts it to RGB internally.
        draw (bool, optional): A flag indicating whether to draw the detected pose on the image. Defaults to True.

        Returns:
        numpy.ndarray: The input image with the detected pose drawn if the 'draw' parameter is True.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img
    
    def get_pose_landmarks(self, img, draw=True):
        """
        This function finds and stores the positions of keypoints in the pose detected in the input image.

        Parameters:

        img (numpy.ndarray): The input image in RGB format.
        draw (bool, optional): A flag indicating whether to draw the keypoints on the image. Defaults to True.

        Returns:
        list: A list of tuples, where each tuple contains the ID, x-coordinate, and y-coordinate of a keypoint.
        """
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def find_angle(self, img, p1, p2, p3, draw=True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

    def compare_pose(self, pose1, pose2, threshold=10):
        match = True
        angles_to_compare = [(11, 13, 15), (12, 14, 16)]  # left and right elbows

        for p1, p2, p3 in angles_to_compare:
            angle1 = self.calculateAngle(pose1, p1, p2, p3)
            angle2 = self.calculateAngle(pose2, p1, p2, p3)
            if abs(angle1 - angle2) > threshold:
                match = False
                break
        return match
    
    def __calculate_angle(self, pose, p1, p2, p3):
        x1, y1 = pose[p1][1:]
        x2, y2 = pose[p2][1:]
        x3, y3 = pose[p3][1:]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        return angle# Return score or match result

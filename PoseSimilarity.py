import cv2
import mediapipe as mp
import time
import math
import os
import random

class poseDetector():
    def __init__(self, mode=False, model_complexity=2, smooth=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.smooth = smooth
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode,
                                     model_complexity=self.model_complexity,
                                     smooth_landmarks=self.smooth,
                                     enable_segmentation=self.enable_segmentation,
                                     smooth_segmentation=self.smooth_segmentation,
                                     min_detection_confidence=self.detectionCon,
                                     min_tracking_confidence=self.trackCon)
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img
    
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
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

    def comparePoses(self, pose1, pose2, threshold=10):
        match = True
        angles_to_compare = [(11, 13, 15), (12, 14, 16)]  # left and right elbows

        for p1, p2, p3 in angles_to_compare:
            angle1 = self.calculateAngle(pose1, p1, p2, p3)
            angle2 = self.calculateAngle(pose2, p1, p2, p3)
            if abs(angle1 - angle2) > threshold:
                match = False
                break
        return match
    
    def calculateAngle(self, pose, p1, p2, p3):
        x1, y1 = pose[p1][1:]
        x2, y2 = pose[p2][1:]
        x3, y3 = pose[p3][1:]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        return angle

def getRandomImage(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    random_image = random.choice(image_files)
    return os.path.join(folder_path, random_image)  

def main():
    reference_image_folder = 'img'

    # Initial random reference image selection
    random_image_path = getRandomImage(reference_image_folder)
    ref_img = cv2.imread(random_image_path)
    
    detector = poseDetector()
    
    # Get the pose from the reference image
    ref_img = detector.findPose(ref_img)
    ref_pose = detector.findPosition(ref_img, draw=False)
    
    # Start webcam
    cap = cv2.VideoCapture(0)
    
    match_start_time = 0  # To track the start of the match
    match_duration = 0    # Total matching time
    threshold_time = 1    # Time threshold for match (in seconds)
    
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findPose(img, draw=False)
        live_pose = detector.findPosition(img, draw=True)
        
        # Compare the live pose with the reference pose
        if len(ref_pose) != 0 and len(live_pose) != 0:
            if detector.comparePoses(ref_pose, live_pose):
                cv2.putText(img, "Pose Match!", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                if match_start_time == 0:
                    match_start_time = time.time()
                match_duration = time.time() - match_start_time
                if match_duration >= threshold_time:
                    # Pose has matched for threshold time, load new reference image
                    print("Pose Matched for 3 seconds! Changing reference image.")
                    random_image_path = getRandomImage(reference_image_folder)
                    ref_img = cv2.imread(random_image_path)
                    ref_img = detector.findPose(ref_img)
                    ref_pose = detector.findPosition(ref_img, draw=False)
                    match_start_time = 0  # Reset match timer
            else:
                match_start_time = 0  # Reset match timer if poses don't match
                cv2.putText(img, "No Match", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

        else:
            match_start_time = 0  # Reset match timer if poses aren't detected
        
        # Display the webcam feed and the reference image in separate windows
        cv2.imshow("Webcam Feed", img)
        cv2.imshow("Reference Pose", ref_img)
        
        # Press 'q' to exit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
main()

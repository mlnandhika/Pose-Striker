import cv2
from PIL import Image, ImageTk

class CameraFeed:
    def __init__(self, label):
        self.label = label
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.frame = None
        self.update_feed()

    def update_feed(self):
        if self.running:
            ret, self.frame = self.cap.read()
            if ret:
                self.frame = cv2.flip(self.frame, 1)
                frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.config(image=imgtk)
            self.label.after(10, self.update_feed)

    def stop(self):
        self.running = False
        self.cap.release()
    
    def get_frame(self):
        return self.frame

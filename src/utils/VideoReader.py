import time
import cv2


# This class for video reading and processing
class VideoReader:
    def __init__(self, filename):
        self.videoCapture = cv2.VideoCapture(filename)
        self.totalFrames = int(self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.timeStamp = self.videoCapture.get(cv2.CAP_PROP_POS_MSEC)
        self.currentFrame = 0
        self.isUsingCamera = True if (filename == 0 or filename.lower() == "camera") else False
        self.startTimeStamp = time.time()

    def readFrame(self):
        if not self.videoCapture.isOpened():
            print("Error opening video stream or file")
            raise TypeError
        elif self.videoCapture.isOpened():
            ret, frame = self.videoCapture.read()
            self.currentFrame += 1
        else:
            return None
        return frame

    def readFrameByTimeStamp(self):
        if not self.videoCapture.isOpened():
            print("Error opening video stream or file")
            raise TypeError
        elif self.videoCapture.isOpened():
            ret, frame = self.videoCapture.read()
            self.videoCapture.set(cv2.CAP_PROP_POS_MSEC, self.timeStamp)
            self.currentFrame += 1
        else:
            return None
        return frame

    def readNextFrame(self):
        ret, frame = self.videoCapture.read()
        return frame

    def readManyFrames(self, num_frames=1):
        framesList = []
        for _ in range(num_frames):
            if self.videoCapture.isOpened():
                ret, frame = self.videoCapture.read()
                if ret is False or frame is None:
                    return None
                framesList.append(frame)
                self.currentFrame += 1
            else:
                return None
        return framesList

    def setupStatusBox(self, image):
        cv2.rectangle(image, (20, 20), (435, 160), (0, 0, 0), -1)
        cv2.putText(image, "Repetition : " + str(counter),
                    (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, "Knee-joint angle : " + str(min_ang),
                    (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Hip angle:
        cv2.putText(image, "Hip-joint angle : " + str(min_ang_hip),
                    (30, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    def getFrameWidth(self):
        return self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)

    def getFrameHeight(self):
        return self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def getVideoFps(self):
        return self.videoCapture.get(cv2.CAP_PROP_FPS)

    def getTimeStamp(self):
        if self.isUsingCamera:
            return (time.time() - self.startTimeStamp) * 1000
        return self.videoCapture.get(cv2.CAP_PROP_POS_MSEC)

    def isOpened(self):
        return self.videoCapture.isOpened()

    def get_current_frame(self):
        return self.currentFrame

    def get_total_frames(self):
        return self.totalFrames

    def release(self):
        self.videoCapture.release()

    def __del__(self):
        self.release()


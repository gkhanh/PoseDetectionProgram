import cv2


# This class for video reading and processing
class VideoReader:
    def __init__(self, filename):
        self.cap = cv2.VideoCapture(filename)
        self.totalFrames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.timeStamp = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        self.currentFrame = 0

    def readFrame(self):
        if not self.cap.isOpened():
            print("Error opening video stream or file")
            raise TypeError
        elif self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret is False or frame is None:
                return None
            self.currentFrame += 1
        else:
            return None
        return frame

    def readManyFrames(self, num_frames=1):
        framesList = []
        for _ in range(num_frames):
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret is False or frame is None:
                    return None
                framesList.append(frame)
                self.currentFrame += 1
            else:
                return None
        return framesList

    def getFrameWidth(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    def getFrameHeight(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def getVideoFps(self):
        return self.cap.get(cv2.CAP_PROP_FPS)

    def getTimeStamp(self):
        return self.timeStamp

    def openedVideo(self):
        return self.cap.isOpened()

    def getVideoFPS(self):
        return self.cap.get(cv2.CAP_PROP_FPS)

    def get_current_frame(self):
        return self.currentFrame

    def get_total_frames(self):
        return self.totalFrames

    def release(self):
        self.cap.release()

    def __del__(self):
        self.release()

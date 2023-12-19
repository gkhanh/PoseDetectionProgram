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
            if ret:  # check if frame is read successfully
                frame = self.resizeFrameToAspectRatio(frame)
                self.currentFrame += 1
            else:
                print("Video ended!")
                return None
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

    def resizeFrameToAspectRatio(self, frame, size=(800, 600), aspectRatio=(4, 3)):
        # Resize frame
        frame = cv2.resize(frame, size)
        # Calculate aspect ratio of resized frame
        height, width, _ = frame.shape
        newAspectRatio = width / height
        targetAspectRatio = aspectRatio[0] / aspectRatio[1]
        # If the aspect ratios do not match, adjust the frame size
        if newAspectRatio != targetAspectRatio:
            # Calculate the new width or height and resize the frame
            if newAspectRatio > targetAspectRatio:
                newWidth = int(targetAspectRatio * height)
                startX = (width - newWidth) // 2
                frame = frame[:, startX:startX + newWidth, :]
            else:
                newHeight = int(width / targetAspectRatio)
                startY = (height - newHeight) // 2
                frame = frame[startY:startY + newHeight, :, :]
        return frame

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

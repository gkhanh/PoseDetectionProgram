import csv
import cv2
import mediapipe as mp


class PoseDetector:
    def __init__(self, videoPath, outputCSV, alpha=0.5):
        self.videoPath = videoPath
        self.outputCSV = outputCSV
        self.alpha = alpha
        self.frameNumber = 0
        self.csvData = []
        self.previousKeypoints = None
        self.mpPose = mp.solutions.pose

    def processVideo(self):
        mpPose = mp.solutions.pose
        mpDrawing = mp.solutions.drawing_utils
        pose = mpPose.Pose()
        cap = cv2.VideoCapture(self.videoPath)

        if not cap.isOpened():
            print("Error opening video stream or file")
            raise TypeError

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(frameRGB)

            if result.pose_landmarks:
                landmarks = result.pose_world_landmarks.landmark
                if self.previousKeypoints is None:
                    self.previousKeypoints = landmarks

                for i, landmark in enumerate(landmarks):
                    landmark.x = self.alpha * landmark.x + (1 - self.alpha) * self.previousKeypoints[i].x
                    landmark.y = self.alpha * landmark.y + (1 - self.alpha) * self.previousKeypoints[i].y
                    landmark.z = self.alpha * landmark.z + (1 - self.alpha) * self.previousKeypoints[i].z

                self.previousKeypoints = landmarks

                mpDrawing.draw_landmarks(frame, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
                self.writeBlackbox(result.pose_landmarks.landmark)

            cv2.namedWindow('MediaPipe Pose', cv2.WINDOW_NORMAL)
            resize = cv2.resize(frame, (1920, 1080))
            cv2.imshow('MediaPipe Pose', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            self.frameNumber += 1

        cap.release()
        cv2.destroyAllWindows()
        self.saveCSVData()

    def writeBlackbox(self, landmarks):
        for idx, landmark in enumerate(landmarks):
            self.csvData.append(
                [self.frameNumber, self.mpPose.PoseLandmark(idx).name, landmark.x, landmark.y, landmark.z])

    def saveCSVData(self):
        with open(self.outputCSV, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['frameNumber', 'landmark', 'x', 'y', 'z'])
            csv_writer.writerows(self.csvData)


if __name__ == "__main__":
    videoPath = 'media/video2.mp4'
    outputCSV = './output/output.csv'
    tracker = PoseDetector(videoPath, outputCSV)
    tracker.processVideo()

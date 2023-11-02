import cv2
import mediapipe as mp
from src.VideoReader import VideoReader

# Threshold values for recognizing objects
VISIBILITY_THRESHOLD = 0.5
PRESENCE_THRESHOLD = 0.5

mpPose = mp.solutions.pose
mpDrawing = mp.solutions.drawing_utils
pose = mpPose.Pose()


class PoseDetector:
    def __init__(self, videoPath, listener, alpha=0.5):
        self.videoPath = videoPath
        self.listener = listener
        self.alpha = alpha
        self.frameNumber = 0
        self.previousKeypoints = None
        self.mpPose = mp.solutions.pose

    def extractingLandmark(self):
        video = VideoReader(self.videoPath)
        if not video.openedVideo():
            print("Error opening video stream or file")
            raise TypeError
        while video.openedVideo():
            frame = video.readFrame()
            ret = video.cap.read()
            if not ret:
                print("Error processing images (maybe stream end?)")
                break
            if frame is not None:
                frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = pose.process(frameRGB)
                if result is not None and result.pose_landmarks:
                    landmarks = result.pose_world_landmarks.landmark
                    if self.previousKeypoints is None:
                        self.previousKeypoints = landmarks

                    for i, landmark in enumerate(landmarks):
                        landmark.x = round((self.alpha * landmark.x + (1 - self.alpha) * self.previousKeypoints[i].x),
                                           3)
                        landmark.y = round((self.alpha * landmark.y + (1 - self.alpha) * self.previousKeypoints[i].y),
                                           3)
                        landmark.z = round((self.alpha * landmark.z + (1 - self.alpha) * self.previousKeypoints[i].z),
                                           3)
                    self.previousKeypoints = landmarks
                    mpDrawing.draw_landmarks(frame, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
                    self.notifyListener(result.pose_landmarks.landmark)
                    # Extract landmarks
                    try:
                        # Get coordinates
                        shoulder = [landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                    landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].y,
                                    landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].z]

                        elbow = [landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value].x,
                                 landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value].y,
                                 landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value].z]

                        wrist = [landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].x,
                                 landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].y,
                                 landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].z]

                        hip = [landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].x,
                               landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].y,
                               landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].z]

                        knee = [landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].x,
                                landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].y,
                                landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].z]

                        ankle = [landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].x,
                                 landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].y,
                                 landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].z]

                    except:
                        pass

                cv2.namedWindow('MediaPipe Pose', cv2.WINDOW_NORMAL)
                cv2.imshow('MediaPipe Pose', frame)
            else:
                print("Frame empty! (maybe stream end?)")
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            self.frameNumber += 1
        video.release()
        cv2.destroyAllWindows()

    def notifyListener(self, landmarks):
        for idx, landmark in enumerate(landmarks):
            self.listener([
                self.frameNumber,
                self.mpPose.PoseLandmark(idx).name,
                landmark.x,
                landmark.y,
                landmark.z
            ])
        return self.listener

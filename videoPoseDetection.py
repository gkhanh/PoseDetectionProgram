import csv

import cv2
import mediapipe as mp


def write_landmarks_to_csv(landmarks, frame_number, csv_data):
    print(f"Landmark coordinates for frame {frame_number}:")
    for idx, landmark in enumerate(landmarks):
        print(f"{mp_pose.PoseLandmark(idx).name}: (x: {landmark.x}, y: {landmark.y}, z: {landmark.z})")
        csv_data.append([frame_number, mp_pose.PoseLandmark(idx).name, landmark.x, landmark.y, landmark.z])
    print("\n")


video_path = 'media/video2.mp4'
output_csv = './output/output3.csv'

# Initialize MediaPipe Pose and Drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()
# Open the video file
cap = cv2.VideoCapture(video_path)

frame_number = 0
csv_data = []

# previous frame keypoint
previous_keypoints = None
# smoothing factor
alpha = 0.7

if cap.isOpened() == False:
    print("Error opening video stream or file")
    raise TypeError

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Process the frame with MediaPipe Pose
    result = pose.process(frame_rgb)
    # Draw the pose landmarks on the frame
    if result.pose_landmarks:
        landmarks = result.pose_world_landmarks.landmark
        if previous_keypoints is None:
            previous_keypoints = landmarks
        # Apply the low-pass filter to the keypoints
        for i, landmark in enumerate(landmarks):
            landmark.x = alpha * landmark.x + (1 - alpha) * previous_keypoints[i].x
            landmark.y = alpha * landmark.y + (1 - alpha) * previous_keypoints[i].y
            landmark.z = alpha * landmark.z + (1 - alpha) * previous_keypoints[i].z
        previous_keypoints = landmarks

        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # Add the landmark coordinates to the list and print them
        write_landmarks_to_csv(result.pose_landmarks.landmark, frame_number, csv_data)
    cv2.namedWindow('MediaPipe Pose', cv2.WINDOW_NORMAL)
    resize = cv2.resize(frame, (1920, 1080))
    # Display the frame
    cv2.imshow('MediaPipe Pose', frame)
    # Exit if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frame_number += 1

cap.release()
cv2.destroyAllWindows()

# Save the CSV data to a file
with open(output_csv, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['frame_number', 'landmark', 'x', 'y', 'z'])
    csv_writer.writerows(csv_data)

import cv2
import time
import os
import numpy as np
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
import pickle
import csv
import threading
import random
from win32com.client import Dispatch

def speak(message):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(message)

# Load models and data
facedetect_path = 'data/haarcascade_frontalface_default.xml'
names_path = 'data/names.pkl'
faces_data_path = 'data/faces_data.pkl'

if not os.path.isfile(facedetect_path):
    print(f"Error: File {facedetect_path} not found.")
    exit()

if not os.path.isfile(names_path) or not os.path.isfile(faces_data_path):
    print(f"Error: File {names_path} or {faces_data_path} not found.")
    exit()

facedetect = cv2.CascadeClassifier(facedetect_path)
with open(names_path, 'rb') as w:
    LABELS = pickle.load(w)
with open(faces_data_path, 'rb') as f:
    FACES = pickle.load(f)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)
COL_NAMES = ['NAME', 'TIME', 'STATUS']

camera_busy = False
processed_frame = None
attendance_data = []
pause_time = 0
pause_event = threading.Event()

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    attendance = []
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        attendance = [str(output[0]), str(timestamp), "true"]
        break  # Stop after the first detected face
    return frame, attendance

def capture_and_process_frames():
    global attendance_data, processed_frame, camera_busy, capture_interval
    while True:
        if pause_event.is_set():
            start_pause_time = time.time()
            record_pause_start(start_pause_time)
            time.sleep(pause_time)
            record_pause_end(start_pause_time + pause_time)
            pause_event.clear()
        if not camera_busy:
            camera_busy = True
            video = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow backend
            video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Higher resolution
            video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Higher resolution
            start_time = time.time()
            detected = False
            while time.time() - start_time < 5:  # Try for 5 seconds
                ret, frame = video.read()
                if not ret:
                    print("Failed to capture frame")
                    continue
                processed_frame, attendance = process_frame(frame)
                cv2.imshow("Camera", processed_frame)
                if attendance:
                    attendance_data.append(attendance)
                    detected = True
                    break  # Stop processing after the first valid result
                if cv2.waitKey(1) == ord('q'):
                    break
            video.release()
            cv2.destroyAllWindows()
            if not detected:
                ts = time.time()
                date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
                attendance_data.append(["Unknown", timestamp, "false"])
            save_attendance()
            camera_busy = False
            capture_interval = random.uniform(10, 55)  # Random interval between 10 to 55 seconds
            time.sleep(capture_interval)

def record_pause_start(start_time):
    date = datetime.fromtimestamp(start_time).strftime("%d-%m-%Y")
    timestamp = datetime.fromtimestamp(start_time).strftime("%H:%M-%S")
    pause_record = ["Paused", timestamp, "Start"]
    save_pause_record(pause_record, date)

def record_pause_end(end_time):
    date = datetime.fromtimestamp(end_time).strftime("%d-%m-%Y")
    timestamp = datetime.fromtimestamp(end_time).strftime("%H:%M-%S")
    pause_record = ["Paused", timestamp, "End"]
    save_pause_record(pause_record, date)

def save_pause_record(record, date):
    if not os.path.exists("pause"):
        os.makedirs("pause")
    file_path = f"pause/Pause_{date}.csv"
    exist = os.path.isfile(file_path)
    with open(file_path, "a") as csvfile:
        writer = csv.writer(csvfile)
        if not exist:
            writer.writerow(["STATUS", "TIMESTAMP", "TYPE"])
        writer.writerow(record)

def save_attendance(record=None):
    global attendance_data
    if record is None and len(attendance_data) > 0:
        record = attendance_data.pop(0)
    if record:
        date = datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y")
        exist = os.path.isfile(f"Attendance/Attendance_{date}.csv")
        if exist:
            with open(f"Attendance/Attendance_{date}.csv", "a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(record)
        else:
            with open(f"Attendance/Attendance_{date}.csv", "a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(record)

def check_for_pause_command():
    global pause_time, pause_event
    while True:
        command = input("Enter command (10min or 20min to pause): ").strip()
        if command == "10min":
            pause_time = 40  # 10 minutes in seconds
            pause_event.set()
        elif command == "20min":
            pause_time = 1200  # 20 minutes in seconds
            pause_event.set()
        else:
            print("Invalid command. Please enter '10min' or '20min'.")

capture_interval = random.uniform(10, 55)  # Random interval between 10 to 55 seconds for testing
capture_thread = threading.Thread(target=capture_and_process_frames)
capture_thread.start()

command_thread = threading.Thread(target=check_for_pause_command)
command_thread.start()

try:
    while True:
        if cv2.waitKey(1) == ord('q'):
            break
finally:
    capture_thread.join()
    command_thread.join()
    cv2.destroyAllWindows()

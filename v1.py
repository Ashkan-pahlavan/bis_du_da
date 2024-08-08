import cv2
import time
import os
import numpy as np
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
import pickle
import csv
import threading
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
    global attendance_data, processed_frame, camera_busy
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
            video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Lower resolution
            video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Lower resolution
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
        #break?

capture_interval = 15  # Capture frame every 20 seconds for testing
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



##################################################################################################main3.py
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
import tkinter as tk
from tkinter import messagebox
from win32com.client import Dispatch
import requests
import json
from decimal import Decimal, InvalidOperation

# Constants
API_URL = 'https://55ixs3z8q0.execute-api.eu-central-1.amazonaws.com/st'  # آدرس URL API Gateway شما
FACEDETECT_PATH = 'data/haarcascade_frontalface_default.xml'
NAMES_PATH = 'data/names.pkl'
FACES_DATA_PATH = 'data/faces_data.pkl'
COL_NAMES = ['NAME', 'TIME', 'STATUS']

class FaceRecognitionApp:
    def __init__(self):
        self._load_models()
        self.attendance_data = []
        self.pause_event = threading.Event()
        self.camera_busy = False
        self.processed_frame = None
        self.pause_time = 0
        self.capture_interval = random.uniform(10, 55)  # Random interval between 10 to 55 seconds for testing
        self._initialize_gui()

    def _load_models(self):
        """Load face detection and recognition models."""
        if not os.path.isfile(FACEDETECT_PATH):
            messagebox.showerror("Error", f"File {FACEDETECT_PATH} not found.")
            exit()

        if not os.path.isfile(NAMES_PATH) or not os.path.isfile(FACES_DATA_PATH):
            messagebox.showerror("Error", f"File {NAMES_PATH} or {FACES_DATA_PATH} not found.")
            exit()

        self.facedetect = cv2.CascadeClassifier(FACEDETECT_PATH)
        with open(NAMES_PATH, 'rb') as f:
            self.labels = pickle.load(f)
        with open(FACES_DATA_PATH, 'rb') as f:
            self.faces = pickle.load(f)

        self.knn = KNeighborsClassifier(n_neighbors=5)
        self.knn.fit(self.faces, self.labels)

    def _initialize_gui(self):
        """Initialize the GUI."""
        self.root = tk.Tk()
        self.root.title("Face Recognition and Detection")
        self.root.geometry("950x400")
        self.root.configure(bg='#2c3e50')  # Dark blue background

        # Create and place buttons for attendance
        self._create_button("Start Attendance", "#27ae60", self.start_attendance, 0)
        self._create_button("10 Minuten Pause", "#f1c40f", self.zehn_minuten_pause_click, 1)
        self._create_button("20 Minuten Pause", "#e67e22", self.zwanzig_minuten_pause_click, 2)
        self._create_button("Ende", "#e74c3c", self.ende_button_click, 3)

        # Create a Canvas widget for dynamic field
        self.canvas = tk.Canvas(self.root, width=600, height=200, bg="white", bd=2, relief="solid")
        self.canvas.grid(row=1, column=0, columnspan=4, pady=20)

        # Create a label for "Ausname"
        ausname_label = tk.Label(self.root, text="Ausname", relief="solid", width=15, height=2, bg="#2c3e50", fg="white", font=("Helvetica", 12))
        ausname_label.grid(row=1, column=4, padx=20, pady=20)

        # Start the application
        self.root.mainloop()

    def _create_button(self, text, color, command, column):
        """Helper method to create a button."""
        button = tk.Button(self.root, text=text, bg=color, fg="white", font=("Helvetica", 12), command=command, padx=20, pady=10, relief="flat", bd=0)
        button.grid(row=0, column=column, padx=20, pady=20)

    def start_attendance(self):
        """Handle start button click."""
        messagebox.showinfo("Info", "Start Attendance")
        threading.Thread(target=self.capture_and_process_frames, daemon=True).start()

    def zehn_minuten_pause_click(self):
        """Handle 10-minute pause button click."""
        messagebox.showinfo("Info", "10 Minuten Pause-Button wurde geklickt")
        self.pause_time = 600  # 10 minutes in seconds
        self.pause_event.set()

    def zwanzig_minuten_pause_click(self):
        """Handle 20-minute pause button click."""
        messagebox.showinfo("Info", "20 Minuten Pause-Button wurde geklickt")
        self.pause_time = 1200  # 20 minutes in seconds
        self.pause_event.set()

    def ende_button_click(self):
        """Handle end button click."""
        self.send_attendance_to_api()
        messagebox.showinfo("Info", "Ende-Button wurde geklickt")
        self.root.quit()

    def speak(self, message):
        """Use TTS to speak a message."""
        speak = Dispatch("SAPI.SpVoice")
        speak.Speak(message)

    def process_frame(self, frame):
        """Process a frame to detect faces and recognize them."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.facedetect.detectMultiScale(gray, 1.3, 5)
        attendance = []
        for (x, y, w, h) in faces:
            crop_img = frame[y:y+h, x:x+w]
            resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
            output = self.knn.predict(resized_img)
            timestamp = datetime.now().strftime("%H:%M:%S")
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
            cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            attendance = [str(output[0]), timestamp, "true"]
            break  # Stop after the first detected face
        return frame, attendance

    def capture_and_process_frames(self):
        """Capture frames from the camera and process them."""
        while True:
            if self.pause_event.is_set():
                self._handle_pause()
                self.pause_event.clear()

            if not self.camera_busy:
                self.camera_busy = True
                video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                start_time = time.time()
                detected = False

                while time.time() - start_time < 5:
                    ret, frame = video.read()
                    if not ret:
                        print("Failed to capture frame")
                        continue
                    self.processed_frame, attendance = self.process_frame(frame)
                    cv2.imshow("Camera", self.processed_frame)
                    if attendance:
                        self.attendance_data.append(attendance)
                        detected = True
                        break
                    if cv2.waitKey(1) == ord('q'):
                        break

                video.release()
                cv2.destroyAllWindows()
                if not detected:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    self.attendance_data.append(["Unknown", timestamp, "false"])
                self.save_attendance()
                self.camera_busy = False
                self.capture_interval = random.uniform(10, 55)  # Random interval between 10 to 55 seconds
                time.sleep(self.capture_interval)

    def _handle_pause(self):
        """Handle pause event."""
        start_pause_time = time.time()
        self.record_pause_start(start_pause_time)
        time.sleep(self.pause_time)
        self.record_pause_end(start_pause_time + self.pause_time)

    def record_pause_start(self, start_time):
        """Record the start of a pause."""
        date = datetime.fromtimestamp(start_time).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(start_time).strftime("%H:%M:%S")
        pause_record = ["Paused", timestamp, "Start"]
        self.save_pause_record(pause_record, date)

    def record_pause_end(self, end_time):
        """Record the end of a pause."""
        date = datetime.fromtimestamp(end_time).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(end_time).strftime("%H:%M:%S")
        pause_record = ["Paused", timestamp, "End"]
        self.save_pause_record(pause_record, date)

    def save_pause_record(self, record, date):
        """Save a pause record to a CSV file."""
        if not os.path.exists("pause"):
            os.makedirs("pause")
        file_path = f"pause/Pause_{date}.csv"
        self._save_record(file_path, record, ["STATUS", "TIMESTAMP", "TYPE"])

    def save_attendance(self):
        """Save the attendance record to a CSV file."""
        if self.attendance_data:
            record = self.attendance_data.pop(0)
            date = datetime.now().strftime("%d-%m-%Y")
            if not os.path.exists("Attendance"):
                os.makedirs("Attendance")
            file_path = f"Attendance/Attendance_{date}.csv"
            self._save_record(file_path, record, COL_NAMES)

    def _save_record(self, file_path, record, headers):
        """Helper method to save a record to a CSV file."""
        exist = os.path.isfile(file_path)
        with open(file_path, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not exist:
                writer.writerow(headers)
            writer.writerow(record)

    def analyze_attendance(self):
        attendance_dir = 'Attendance'
        results = []

        attendance_files = [f for f in os.listdir(attendance_dir) if f.startswith("Attendance_") and f.endswith(".csv")]
        attendance_files.sort(key=lambda x: datetime.strptime(x.split("_")[1].split(".")[0], "%d-%m-%Y"), reverse=True)

        for filename in attendance_files:
            date_str = filename.split("_")[1].split(".")[0]
            date = datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")

            true_count = 0
            false_count = 0
            total_count = 0
            name = None  # Initialize name variable

            with open(os.path.join(attendance_dir, filename), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    total_count += 1
                    name = row['NAME']  # Get the name from the row
                    if row['STATUS'] == 'true':
                        true_count += 1
                    elif row['STATUS'] == 'false':
                        false_count += 1

            if total_count > 0:
                try:
                    true_percentage = Decimal(true_count) / Decimal(total_count) * Decimal(100)
                    false_percentage = Decimal(false_count) / Decimal(total_count) * Decimal(100)

                    results.append({
                        'name': name,  # Add the name to the results
                        'date': date,
                        'true_percentage': str(round(true_percentage, 1)),  # Convert to string
                        'false_percentage': str(round(false_percentage, 1))  # Convert to string
                    })
                except InvalidOperation:
                    print("InvalidOperation error occurred while calculating percentages.")
                    continue

        return results

    def send_to_api(self, data):
        try:
            # Wrap the data in a JSON body as required by your API Gateway
            payload = {
                "body": json.dumps(data)
            }
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                print("Data successfully sent to API.")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def send_attendance_to_api(self):
        attendance_data = self.analyze_attendance()
        if attendance_data:
            last_record = attendance_data[0]  # Get the latest record
            self.send_to_api(last_record)  # Send only the latest record
            print("Data has been sent to API:")
            print(json.dumps(last_record, indent=2, default=str))

if __name__ == "__main__":
    app = FaceRecognitionApp()



#####################################################addface 
import cv2
import pickle
import numpy as np
import os

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Load the face detection model
facedetect_path = 'data/haarcascade_frontalface_default.xml'
if not os.path.isfile(facedetect_path):
    print(f"Error: File {facedetect_path} not found.")
    exit()

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(facedetect_path)

faces_data = []

i = 0

name = input("Enter Your Name: ")

while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to capture image")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50))
        if len(faces_data) < 100 and i % 10 == 0:
            faces_data.append(resized_img)
        i += 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_data) == 100:
        break

video.release()
cv2.destroyAllWindows()

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(len(faces_data), -1)

# Save name data
names_path = 'data/names.pkl'
if not os.path.isfile(names_path):
    names = [name] * len(faces_data)
    with open(names_path, 'wb') as f:
        pickle.dump(names, f)
else:
    with open(names_path, 'rb') as f:
        names = pickle.load(f)
    names.extend([name] * len(faces_data))
    with open(names_path, 'wb') as f:
        pickle.dump(names, f)

# Save faces data
faces_data_path = 'data/faces_data.pkl'
if not os.path.isfile(faces_data_path):
    with open(faces_data_path, 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open(faces_data_path, 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)
    with open(faces_data_path, 'wb') as f:
        pickle.dump(faces, f)

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
from decimal import Decimal

# Constants
API_URL = 'https://ea4ws37afh.execute-api.eu-central-1.amazonaws.com/st/attendify'
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
        self.capture_interval = random.uniform(10, 55)
        self._initialize_gui()

    def _load_models(self):
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
        self.root = tk.Tk()
        self.root.title("Face Recognition and Detection")
        self.root.geometry("950x400")
        self.root.configure(bg='#2c3e50')

        self._create_button("Start Attendance", "#27ae60", self.start_attendance, 0)
        self._create_button("10 Minuten Pause", "#f1c40f", self.zehn_minuten_pause_click, 1)
        self._create_button("20 Minuten Pause", "#e67e22", self.zwanzig_minuten_pause_click, 2)
        self._create_button("Ende", "#e74c3c", self.ende_button_click, 3)

        self.canvas = tk.Canvas(self.root, width=600, height=200, bg="white", bd=2, relief="solid")
        self.canvas.grid(row=1, column=0, columnspan=4, pady=20)

        ausname_label = tk.Label(self.root, text="Ausname", relief="solid", width=15, height=2, bg="#2c3e50", fg="white", font=("Helvetica", 12))
        ausname_label.grid(row=1, column=4, padx=20, pady=20)

        self.root.mainloop()

    def _create_button(self, text, color, command, column):
        button = tk.Button(self.root, text=text, bg=color, fg="white", font=("Helvetica", 12), command=command, padx=20, pady=10, relief="flat", bd=0)
        button.grid(row=0, column=column, padx=20, pady=20)

    def start_attendance(self):
        messagebox.showinfo("Info", "Start Attendance")
        threading.Thread(target=self.capture_and_process_frames, daemon=True).start()

    def zehn_minuten_pause_click(self):
        messagebox.showinfo("Info", "10 Minuten Pause-Button wurde geklickt")
        self.pause_time = 10 # 10 seconds for testing
        self.pause_event.set()

    def zwanzig_minuten_pause_click(self):
        messagebox.showinfo("Info", "20 Minuten Pause-Button wurde geklickt")
        self.pause_time = 20  # 20 seconds for testing
        self.pause_event.set()

    def ende_button_click(self):
        self.send_attendance_to_api()
        messagebox.showinfo("Info", "Ende-Button wurde geklickt")
        self.root.quit()

    def speak(self, message):
        speak = Dispatch("SAPI.SpVoice")
        speak.Speak(message)

    def process_frame(self, frame):
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
            break
        return frame, attendance

    def capture_and_process_frames(self):
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
                self.capture_interval = random.uniform(10, 55)
                time.sleep(self.capture_interval)

    def _handle_pause(self):
        start_pause_time = time.time()
        self.record_pause_start(start_pause_time)
        time.sleep(self.pause_time)
        self.record_pause_end(start_pause_time + self.pause_time)

    def record_pause_start(self, start_time):
        date = datetime.fromtimestamp(start_time).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(start_time).strftime("%H:%M:%S")
        pause_record = ["Paused", timestamp, "Start"]
        if self.pause_time == 10:
            self.save_pause_record(pause_record, date, "pause")
        elif self.pause_time == 20:
            self.save_pause_record(pause_record, date, "pause2")

    def record_pause_end(self, end_time):
        date = datetime.fromtimestamp(end_time).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(end_time).strftime("%H:%M:%S")
        pause_record = ["Paused", timestamp, "End"]
        if self.pause_time == 10:
            self.save_pause_record(pause_record, date, "pause")
        elif self.pause_time == 20:
            self.save_pause_record(pause_record, date, "pause2")

    def save_pause_record(self, record, date, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_path = f"{folder_name}/Pause_{date}.csv"
        self._save_record(file_path, record, ["STATUS", "TIMESTAMP", "TYPE"])

    def save_attendance(self):
        if self.attendance_data:
            record = self.attendance_data.pop(0)
            date = datetime.now().strftime("%d-%m-%Y")
            if not os.path.exists("Attendance"):
                os.makedirs("Attendance")
            file_path = f"Attendance/Attendance_{date}.csv"
            self._save_record(file_path, record, COL_NAMES)

    def _save_record(self, file_path, record, headers):
        exist = os.path.isfile(file_path)
        with open(file_path, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not exist:
                writer.writerow(headers)
            writer.writerow(record)

    def analyze_attendance(self):
        attendance_dir = 'Attendance'
        results = []

        for filename in sorted(os.listdir(attendance_dir)):
            if filename.startswith("Attendance_") and filename.endswith(".csv"):
                try:
                    date_str = filename.split("_")[1].split(".")[0]
                    date = datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
                except ValueError:
                    print(f"Skipping file due to incorrect date format: {filename}")
                    continue

                true_count = 0
                false_count = 0
                total_count = 0
                name_counts = {}

                with open(os.path.join(attendance_dir, filename), 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        total_count += 1
                        name = row['NAME']
                        if row['STATUS'] == 'true':
                            true_count += 1
                            name_counts[name] = name_counts.get(name, 0) + 1
                        elif row['STATUS'] == 'false':
                            false_count += 1

                most_common_name = max(name_counts, key=name_counts.get) if name_counts else "Unknown"

                if total_count > 0:
                    true_percentage = round(Decimal(true_count) / Decimal(total_count) * Decimal(100), 2)
                    false_percentage = round(Decimal(false_count) / Decimal(total_count) * Decimal(100), 2)

                    results.append({
                        'name': most_common_name,
                        'date': date,
                        'true_percentage': str(true_percentage),
                        'false_percentage': str(false_percentage)
                    })

        return results

    def analyze_pause(self, pause_dir='pause'):
        pause_data = []

        if os.path.exists(pause_dir):
            latest_file = sorted(os.listdir(pause_dir))[-1]
            date_str = latest_file.split("_")[1].split(".")[0]
            date = datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")

            with open(os.path.join(pause_dir, latest_file), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    pause_data.append({
                        'status': row['STATUS'],
                        'timestamp': row['TIMESTAMP'],
                        'type': row['TYPE']
                    })

        return {'date': date, 'pause_data': pause_data}

    def send_to_api(self, data):
        try:
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
        pause_data = self.analyze_pause()
        pause_20_data = self.analyze_pause(pause_dir='pause2')  # Analyze 20-minute pause data

        if attendance_data and pause_data:
            last_attendance_record = attendance_data[-1]
            combined_data = {
                'attendance': last_attendance_record,
                'pause': pause_data,
                'pause_20_data': pause_20_data['pause_data']  # Include 20-minute pause data
            }
            self.send_to_api(combined_data)
            print("Data has been sent to API:")
            print(json.dumps(combined_data, indent=2, default=str))

if __name__ == "__main__":
    app = FaceRecognitionApp()

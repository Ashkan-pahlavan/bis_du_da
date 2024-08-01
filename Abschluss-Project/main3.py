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
import tkinter as tk
from tkinter import messagebox

# Constants
FACEDETECT_PATH = 'data/haarcascade_frontalface_default.xml'
NAMES_PATH = 'data/names.pkl'
FACES_DATA_PATH = 'data/faces_data.pkl'
COL_NAMES = ['NAME', 'TIME', 'STATUS']
CAPTURE_INTERVAL = 15  # Capture frame every 15 seconds

class FaceRecognitionApp:
    def __init__(self):
        self._load_models()
        self.attendance_data = []
        self.pause_event = threading.Event()
        self.camera_busy = False
        self.processed_frame = None
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
        self.root.title("Identify")
        self.root.geometry("800x400")
        self.root.configure(bg='#f0f0f0')

        # Create and place buttons
        self._create_button("Start", "#4CAF50", self.start_button_click, 0)
        self._create_button("10 Minuten Pause", "#FFEB3B", self.zehn_minuten_pause_click, 1)
        self._create_button("20 Minuten Pause", "#FFC107", self.zwanzig_minuten_pause_click, 2)
        self._create_button("Ende", "#F44336", self.ende_button_click, 3)

        # Create a Canvas widget for dynamic field
        self.canvas = tk.Canvas(self.root, width=600, height=200, bg="white", bd=2, relief="solid")
        self.canvas.grid(row=1, column=0, columnspan=4, pady=20)

        # Create a label for "ausname"
        ausname_label = tk.Label(self.root, text="Ausname", relief="solid", width=15, height=2, bg="#f0f0f0", font=("Helvetica", 12))
        ausname_label.grid(row=1, column=4, padx=20, pady=20)

        # Start the application
        self.root.mainloop()

    def _create_button(self, text, color, command, column):
        """Helper method to create a button."""
        button = tk.Button(self.root, text=text, bg=color, fg="white", font=("Helvetica", 12), command=command, padx=20, pady=10)
        button.grid(row=0, column=column, padx=20, pady=20)

    def start_button_click(self):
        """Handle start button click."""
        messagebox.showinfo("Info", "Start-Button wurde geklickt")
        threading.Thread(target=self.capture_and_process_frames, daemon=True).start()

    def zehn_minuten_pause_click(self):
        """Handle 10-minute pause button click."""
        messagebox.showinfo("Info", "10 Minuten Pause-Button wurde geklickt")
        self.pause_event.set()

    def zwanzig_minuten_pause_click(self):
        """Handle 20-minute pause button click."""
        messagebox.showinfo("Info", "20 Minuten Pause-Button wurde geklickt")
        self.pause_event.set()

    def ende_button_click(self):
        """Handle end button click."""
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
            crop_img = frame[y:y+h, x:x+w, :]
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
                video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
                video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
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
                time.sleep(CAPTURE_INTERVAL)

    def _handle_pause(self):
        """Handle pause event."""
        start_pause_time = time.time()
        self.record_pause_start(start_pause_time)
        time.sleep(40)  # Automatically end pause after 40 seconds
        self.record_pause_end(start_pause_time + 40)

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

if __name__ == "__main__":
    app = FaceRecognitionApp()

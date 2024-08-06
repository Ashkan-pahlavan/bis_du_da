import cv2
import pickle
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox

class FaceDetectionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Face Detection")
        self.root.geometry("400x300")
        self.root.configure(bg='#2c3e50')  # Dark blue background

        # Create an entry field for name
        name_label = tk.Label(self.root, text="Enter Your Name:", bg='#2c3e50', fg="white", font=("Helvetica", 14))
        name_label.pack(pady=(20, 10))

        self.name_entry = tk.Entry(self.root, font=("Helvetica", 14), width=30)
        self.name_entry.pack(pady=(0, 20))

        # Create a button to start face detection
        start_button = tk.Button(self.root, text="Start Face Detection", bg="#27ae60", fg="white", font=("Helvetica", 14), command=self.start_face_detection, relief="flat", bd=0)
        start_button.pack(pady=(10, 20))

        self.root.mainloop()

    def start_face_detection(self):
        if not os.path.exists('data'):
            os.makedirs('data')

        facedetect_path = 'data/haarcascade_frontalface_default.xml'
        if not os.path.isfile(facedetect_path):
            messagebox.showerror("Error", f"File {facedetect_path} not found.")
            return

        video = cv2.VideoCapture(0)
        facedetect = cv2.CascadeClassifier(facedetect_path)

        faces_data = []
        i = 0
        name = self.name_entry.get()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty.")
            return

        while True:
            ret, frame = video.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture image.")
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

        messagebox.showinfo("Info", "Face data collection completed.")

if __name__ == "__main__":
    FaceDetectionApp()

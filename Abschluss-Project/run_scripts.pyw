import tkinter as tk
import subprocess

def run_main3():
    # Full path to main3.py
    subprocess.run(['python', r"C:/Users/Ashkan_pahlavan/Documents/Abschluss-project/Abschluss-Project/main3.py"])

def run_main4():
    # Full path to main4.py
    subprocess.run(['python', r'C:/Users/Ashkan_pahlavan/Documents/Abschluss-project/Abschluss-Project/main4.py'])

# Initialize the main window
root = tk.Tk()
root.title("Choose Script")

# Styling the main window
root.configure(bg="white")
root.geometry("300x200")

# Add the buttons directly to the main window
btn_main3 = tk.Button(root, text="Attendify Board", command=run_main3, bg="#007ACC", fg="white", font=("Helvetica", 14))
btn_main3.pack(pady=10, padx=20)

btn_main4 = tk.Button(root, text="Face Detection", command=run_main4, bg="#007ACC", fg="white", font=("Helvetica", 14))
btn_main4.pack(pady=10, padx=20)

# Start the Tkinter event loop
root.mainloop()
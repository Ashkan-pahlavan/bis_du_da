from cryptography.fernet import Fernet
import os

# Path to the key file
key_path = 'C:/Users/Ashkan_pahlavan/Documents/Abschluss-project/Abschluss-Project/key.key'
with open(key_path, 'rb') as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# Define the project directory
project_dir = 'C:/Users/Ashkan_pahlavan/Documents/Abschluss-project/Abschluss-Project'

# List of files to exclude from encryption
files_to_exclude = ['encrypt_files.py', 'decrypt_files.py']

# Encrypt each file with specific extensions, excluding certain files
extensions_to_encrypt = ['.py', '.csv']
for root, dirs, files in os.walk(project_dir):
    for file in files:
        if file in files_to_exclude:
            continue
        if any(file.endswith(ext) for ext in extensions_to_encrypt):
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                original_data = f.read()
            encrypted_data = cipher_suite.encrypt(original_data)
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
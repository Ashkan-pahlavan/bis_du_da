from cryptography.fernet import Fernet
import os

# Path to the key file
key_path = 'C:/Users/Ashkan_pahlavan/Documents/Abschluss-project/Abschluss-Project/key.key'
with open(key_path, 'rb') as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# Define the project directory
project_dir = 'C:/Users/Ashkan_pahlavan/Documents/Abschluss-project/Abschluss-Project'

# List of files to exclude from decryption
files_to_exclude = ['decrypt_files.py', 'encrypt_files.py']

# Decrypt each file with specific extensions, excluding certain files
extensions_to_decrypt = ['.py', '.csv']
for root, dirs, files in os.walk(project_dir):
    for file in files:
        if file in files_to_exclude:
            continue
        if any(file.endswith(ext) for ext in extensions_to_decrypt):
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            try:
                decrypted_data = cipher_suite.decrypt(encrypted_data)
                with open(file_path, 'wb') as f:
                    f.write(decrypted_data)
            except Exception as e:
                print(f"Error decrypting {file_path}: {e}")
                
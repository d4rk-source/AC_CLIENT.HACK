import keyboard
import pyautogui
import time

while True:
    if keyboard.is_pressed("space"):
        # Press space continuously while the key is held down
        while keyboard.is_pressed("space"):
            pyautogui.press('space')
            print("space should be pressed")
            time.sleep(0.1)  # Adjust sleep time as needed                    
    time.sleep(0.01)  # Slight delay to reduce CPU usage when waiting

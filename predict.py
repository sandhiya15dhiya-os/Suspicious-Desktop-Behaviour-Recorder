import time
import keyboard
import pickle
import os
import cv2
import numpy as np
from PIL import ImageGrab
from twilio.rest import Client

# -----------------
# Load trained model
# -----------------
with open("model.pkl", "rb") as f:
    clf = pickle.load(f)

# Ensure folders exist
if not os.path.exists("../alerts"):
    os.makedirs("../alerts")

# -----------------
# SCREEN CAPTURE
# -----------------
def capture_screen():
    img = ImageGrab.grab()
    path = f"../alerts/screen_{int(time.time())}.png"
    img.save(path)
    return path

# -----------------
# INTRUDER WEBCAM CAPTURE
# -----------------
def capture_intruder():
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    ret, frame = cap.read()
    path = f"../alerts/intruder_{int(time.time())}.png"
    cv2.imwrite(path, frame)
    cap.release()
    return path

# -----------------
# SMS ALERT
# -----------------
def send_sms_alert(screen, intruder):
    ACCOUNT_SID = "YOUR_TWILIO_SID"
    AUTH_TOKEN = "YOUR_AUTH_TOKEN"
    TWILIO_NUMBER = "+1XXXXXXXXXX"
    YOUR_NUMBER = "+91XXXXXXXXXX"

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    msg = f"""
⚠ ALERT – Suspicious Activity Detected!

Screen Capture: {screen}
Intruder Photo: {intruder}
Time: {time.ctime()}
"""

    client.messages.create(
        body=msg,
        from_=TWILIO_NUMBER,
        to=YOUR_NUMBER
    )
    print("✔ SMS Sent!")

# -----------------
# LIVE KEY MONITOR
# -----------------
pressed_times = []

def on_key(e):
    if e.event_type != 'down':
        return

    t = time.time()
    pressed_times.append(t)

    if len(pressed_times) > 2:
        times = np.diff(pressed_times[-10:])
        avg = np.mean(times)
        var = np.var(times)
        total = len(times)

        result = clf.predict([[avg, var, total]])[0]

        if result == 1:
            print("⚠ Intruder detected!")
            screen = capture_screen()
            intruder = capture_intruder()
            send_sms_alert(screen, intruder)

keyboard.hook(on_key)
keyboard.wait()

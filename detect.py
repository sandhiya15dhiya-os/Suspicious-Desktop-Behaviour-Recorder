from pynput import mouse, keyboard
import time
import joblib
import cv2
import pyautogui
import csv
import os

model = joblib.load("../model/model.pkl")

alert_folder = "../alerts"
os.makedirs(alert_folder, exist_ok=True)

events = []

def predict_intruder():
    if len(events) < 5:
        return 0
    timestamps = [e[0] for e in events[-5:]]
    v1 = [e[2] for e in events[-5:]]
    v2 = [e[3] for e in events[-5:]]

    avg_ts = sum(timestamps)/5
    avg_v1 = sum(v1)/5
    avg_v2 = sum(v2)/5

    X = [[avg_ts, avg_v1, avg_v2]]
    pred = model.predict(X)[0]
    return pred

def capture_intruder_data():
    ts = int(time.time())

    img = pyautogui.screenshot()
    img_path = f"{alert_folder}/intruder_{ts}.png"
    img.save(img_path)

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(f"{alert_folder}/cam_{ts}.png", frame)
    cap.release()

    with open(f"{alert_folder}/log_{ts}.txt", "w") as f:
        f.write("Intruder detected!\n")
        f.write(f"Timestamp: {ts}\n")

    print("ALERT: Intruder detected! Evidence saved.")

def on_move(x, y):
    events.append([time.time(), "move", x, y])
    if predict_intruder() == 1:
        capture_intruder_data()

def on_click(x, y, button, pressed):
    num = hash(str(button)) % 10000
    events.append([time.time(), "click", num, 1 if pressed else 0])
    if predict_intruder() == 1:
        capture_intruder_data()

def on_press(key):
    num = hash(str(key)) % 10000
    events.append([time.time(), "key", num, 1])
    if predict_intruder() == 1:
        capture_intruder_data()

def on_release(key):
    num = hash(str(key)) % 10000
    events.append([time.time(), "key", num, 0])
    if predict_intruder() == 1:
        capture_intruder_data()

mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

print("SDBR Intruder Detection Running...")
print("Press CTRL+C to stop.")

try:
    while True:
        time.sleep(0.05)
except KeyboardInterrupt:
    print("Stopped.")

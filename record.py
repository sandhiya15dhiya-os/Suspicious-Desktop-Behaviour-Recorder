import keyboard
import time
import csv
import os

# Directory to store data
data_dir = "data_user"
os.makedirs(data_dir, exist_ok=True)

# CSV file to store typing samples
filename = os.path.join(data_dir, "record_data.csv")

print("\n=== SDBR PROJECT: TYPING DATA RECORDER ===")
print("Press any keys... your keystroke pattern is being recorded.")
print("Press ESC to stop recording.\n")

press_times = {}
rows = []


def on_key_event(event):
    global press_times, rows

    # Key pressed
    if event.event_type == "down":
        press_times[event.name] = time.time()

    # Key released
    elif event.event_type == "up":
        if event.name in press_times:
            press_time = press_times[event.name]
            release_time = time.time()

            duration = release_time - press_time  # hold time

            rows.append(duration)
            print(f"Key: {event.name} | Duration: {duration:.4f} sec")

    # Stop recording when ESC pressed
    if event.name == "esc":
        return False


keyboard.hook(on_key_event)
keyboard.wait("esc")

print("\nRecording stopped. Saving file...")

# Save to CSV
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["duration"])
    for r in rows:
        writer.writerow([r])

print(f"Saved typing sample → {filename}")

import keyboard
import time
import pandas as pd
import os

# Create folder if not exists
if not os.path.exists("../data_user"):
    os.makedirs("../data_user")

filename = f"../data_user/data_{int(time.time())}.csv"

data = []
print("Collecting keystroke data... Press ESC to stop.")

def on_key(e):
    if e.event_type == 'down':
        t = time.time()
        data.append([e.name, t])

keyboard.hook(on_key)
keyboard.wait('esc')

df = pd.DataFrame(data, columns=["key", "time"])
df.to_csv(filename, index=False)

print(f"Saved: {filename}")

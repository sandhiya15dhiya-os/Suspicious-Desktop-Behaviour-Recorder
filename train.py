import pandas as pd
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# ------------------------------
# FOLDER WHERE TYPING DATA IS SAVED
# ------------------------------
folder = "../data_user"
files = os.listdir(folder)

X = []
y = []

# ------------------------------
# LOAD ALL CSV DATA
# ------------------------------
for f in files:
    df = pd.read_csv(os.path.join(folder, f))
    
    # Skip empty files
    if len(df) < 2:
        continue
    
    # Try to detect numeric column automatically
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        print(f"Skipping {f}, no numeric column found.")
        continue
    
    col = numeric_cols[0]   # pick the first numeric column
    times = df[col].diff().dropna()
    
    avg = times.mean()
    var = times.var()
    total = len(df)

    X.append([avg, var, total])
    y.append(0)  # normal user

# ------------------------------
# SYNTHETIC ATTACKER DATA (for demo)
# ------------------------------
for _ in range(100):
    X.append([np.random.uniform(0.01, 0.03),
              np.random.uniform(0.0001, 0.003),
              np.random.randint(10, 40)])
    y.append(1)  # suspicious

# ------------------------------
# TRAIN RANDOM FOREST CLASSIFIER
# ------------------------------
clf = RandomForestClassifier()
clf.fit(X, y)

# ------------------------------
# SAVE MODEL
# ------------------------------
with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)

print("✅ model.pkl created successfully!")
print("Features used: [avg_interval, variance, total_keys]")
print("Normal user samples:", len([v for v in y if v==0]))
print("Suspicious samples:", len([v for v in y if v==1]))

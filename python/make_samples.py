import os
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
raw_folder = os.path.join(script_dir, "..", "data")
sample_folder = os.path.join(script_dir, "..", "data", "sample")

os.makedirs(sample_folder, exist_ok=True)

N_ROWS = 200  # how many sample rows per file

for f in os.listdir(raw_folder):
    if f.endswith(".csv"):
        path = os.path.join(raw_folder, f)
        df = pd.read_csv(path, nrows=N_ROWS)
        out_path = os.path.join(sample_folder, f)
        df.to_csv(out_path, index=False)
        print(f"Saved sample: {f} ({len(df)} rows)")

print("\nDone. Sample files are in data/sample/")
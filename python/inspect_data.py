import pandas as pd
import os

data_folder = "../data"   # relative to python/ folder

for f in os.listdir(data_folder):
    if f.endswith(".csv"):
        path = os.path.join(data_folder, f)
        df = pd.read_csv(path, nrows=5)
        print("=" * 60)
        print(f"FILE: {f}")
        print(df.dtypes)
        print(df.head())
        print()
for f in os.listdir(data_folder):
    if f.endswith(".csv"):
        path = os.path.join(data_folder, f)
        # count rows without loading whole file into memory
        with open(path, encoding="utf-8", errors="ignore") as file:
            row_count = sum(1 for _ in file) - 1  # minus header
        print(f"{f}: {row_count} rows")
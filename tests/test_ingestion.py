from pathlib import Path

from src.reporting.ingestion import load_data


DATA_DIR = Path("data/raw")

print("loading client data...")

data = load_data(DATA_DIR)

print("\nLoaded datasets:")

for name, dataframe in data.items():
    print(f"\n{name.upper()}")
    print("-" * 40)
    print(dataframe.info())
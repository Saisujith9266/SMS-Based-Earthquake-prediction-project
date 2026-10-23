"""Download a reproducible earthquake catalog CSV from the public USGS API.

Example:
python download_usgs_dataset.py --start 2015-01-01 --end 2025-01-01 --min-magnitude 2.5
"""
import argparse
from pathlib import Path
import pandas as pd
import requests

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--end", default="2025-01-01")
    parser.add_argument("--min-magnitude", type=float, default=2.5)
    parser.add_argument("--output", default="data/usgs_earthquakes.csv")
    args = parser.parse_args()
    params = {
        "format": "csv", "starttime": args.start, "endtime": args.end,
        "minmagnitude": args.min_magnitude, "orderby": "time-asc"
    }
    response = requests.get(URL, params=params, timeout=120)
    response.raise_for_status()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(response.content)
    frame = pd.read_csv(output)
    print(f"Saved {len(frame):,} earthquake records to {output.resolve()}")
    print("Columns:", ", ".join(frame.columns))
    print("Source: USGS Earthquake Catalog API")
if __name__ == "__main__":
    main()

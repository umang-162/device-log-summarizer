"""
Telemetry Summary (standard library `csv` + `json`)

Reads device_telemetry.csv (columns: device_id, status, temperature), groups by
device_id, computes total records, mean temperature and ERROR count, removes
devices whose mean temperature is strictly > 80.0, writes output.json and prints
a summary table.
"""

import csv
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "device_telemetry.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "output.json")
TEMP_THRESHOLD = 80.0


def load_telemetry(path):
    """Read the CSV and return a dict: device_id -> {'temps': [...], 'errors': int, 'records': int}."""
    groups = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"device_id", "status", "temperature"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain columns: {sorted(required)}")

        for line_no, row in enumerate(reader, start=2):
            device = (row.get("device_id") or "").strip()
            if not device:
                print(f"  [warn] line {line_no}: missing device_id, skipped")
                continue

            g = groups.setdefault(device, {"temps": [], "errors": 0, "records": 0})
            g["records"] += 1

            if (row.get("status") or "").strip().upper() == "ERROR":
                g["errors"] += 1

            try:
                g["temps"].append(float(row.get("temperature")))
            except (TypeError, ValueError):
                print(f"  [warn] line {line_no}: bad temperature '{row.get('temperature')}', not averaged")
    return groups


def aggregate(groups):
    """Build the per-device summary, keeping only devices with avg temp <= 80.0."""
    results, excluded = [], []
    for device in sorted(groups):
        g = groups[device]
        avg = round(sum(g["temps"]) / len(g["temps"]), 2) if g["temps"] else None
        summary = {
            "device_id": device,
            "total_records": g["records"],
            "avg_temperature": avg,
            "error_count": g["errors"],
        }
        if avg is not None and avg > TEMP_THRESHOLD:
            excluded.append(summary)
        else:
            results.append(summary)
    return results, excluded


def print_table(rows, excluded):
    header = f"| {'Device ID':<10} | {'Records':>7} | {'Avg Temp (C)':>12} | {'Errors':>6} |"
    border = "+" + "-" * (len(header) - 2) + "+"
    print("\nDEVICE LOG SUMMARY")
    print(border)
    print(header)
    print(border)
    for r in rows:
        avg = f"{r['avg_temperature']:.2f}" if r["avg_temperature"] is not None else "N/A"
        print(f"| {r['device_id']:<10} | {r['total_records']:>7} | {avg:>12} | {r['error_count']:>6} |")
    print(border)
    print(f"Devices kept: {len(rows)}")
    if excluded:
        names = ", ".join(f"{e['device_id']} ({e['avg_temperature']:.2f})" for e in excluded)
        print(f"Filtered out (avg temp > {TEMP_THRESHOLD}): {names}")


def main():
    try:
        groups = load_telemetry(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: '{os.path.basename(INPUT_FILE)}' not found in {BASE_DIR}.")
        print("Create the CSV file next to this script and run again.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not groups:
        print("No data rows found in the CSV. Nothing to summarise.")
        sys.exit(0)

    results, excluded = aggregate(groups)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print_table(results, excluded)
    print(f"\nSaved aggregated data to {os.path.basename(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()

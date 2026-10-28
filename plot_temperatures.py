"""
Temperature Chart (matplotlib)

Loads output.json (created by telemetry_summary.py) and draws a bar chart of the average
temperature per device. Saves it as temperature_chart.png and opens a window.
"""

import json
import os
import sys

import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "output.json")
CHART_FILE = os.path.join(BASE_DIR, "temperature_chart.png")
TEMP_THRESHOLD = 80.0


def load_results(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: output.json not found. Run 'python telemetry_summary.py' first.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: output.json is not valid JSON. Re-run 'python telemetry_summary.py'.")
        sys.exit(1)


def plot(results):
    rows = [r for r in results if r.get("avg_temperature") is not None]
    if not rows:
        print("No devices with temperature data to plot.")
        sys.exit(0)

    devices = [r["device_id"] for r in rows]
    temps = [r["avg_temperature"] for r in rows]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(devices, temps, color="#4C72B0", edgecolor="black", width=0.6)

    # value label on top of each bar
    for bar, t in zip(bars, temps):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
                f"{t:.1f}", ha="center", va="bottom", fontsize=10, zorder=3,
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none"))

    ax.axhline(TEMP_THRESHOLD, color="red", linestyle="--", linewidth=1.2,
               label=f"Filter threshold ({TEMP_THRESHOLD:.0f} °C)")

    ax.set_title("Average Temperature per Device", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Device ID", fontsize=12)
    ax.set_ylabel("Average Temperature (°C)", fontsize=12)
    ax.set_ylim(0, max(max(temps), TEMP_THRESHOLD) * 1.15)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.set_axisbelow(True)
    ax.legend(loc="upper right")

    # Fix for overlapping x-axis labels (see PROMPT_LOG.md)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(CHART_FILE, dpi=150)
    print(f"Chart saved to {os.path.basename(CHART_FILE)}")

    if "--no-show" not in sys.argv:
        plt.show()


if __name__ == "__main__":
    plot(load_results(INPUT_FILE))

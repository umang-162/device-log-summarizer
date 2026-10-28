# PROMPT_LOG.md

A record of how the AI assistant was used to build the charting step (`plot_temperatures.py`) of the Device Log Summarizer, including one bug and how it was fixed.

---

## 1. Initial prompt

> Write a Python script using matplotlib that loads `output.json` and generates a bar chart comparing the average temperature per device. Each entry in the JSON has `device_id`, `total_records`, `avg_temperature` and `error_count`. Give the chart a clear title and axis labels.

### AI's first response (summary)

The AI produced a short script:

```python
import json
import matplotlib.pyplot as plt

with open("output.json") as f:
    data = json.load(f)

devices = [d["device_id"] for d in data]
temps = [d["avg_temperature"] for d in data]

plt.bar(devices, temps)
plt.title("Average Temperature per Device")
plt.xlabel("Device ID")
plt.ylabel("Average Temperature")
plt.show()
```

---

## 2. Bug observed

When tested with a larger dataset that used long device names (for example `WAREHOUSE-SENSOR-NORTH-01`, `WAREHOUSE-SENSOR-SOUTH-02` …), the chart had these problems:

- **Overlapping x-axis labels** – the long device IDs ran into each other and were unreadable.
- **Labels cut off** – the bottom of the labels was clipped by the figure edge.
- The default figure size was too small, and there was no temperature unit on the y-axis.
- The script crashed with `FileNotFoundError` if `telemetry_summary.py` had not been run first.

---

## 3. Follow-up prompt

> The x-axis labels overlap and get cut off when device names are long. Please fix the layout: rotate the labels, make sure nothing is clipped, use a bigger figure, show the value on top of each bar, add the °C unit and a dashed line for the 80 °C threshold. Also handle the case where `output.json` is missing with a friendly message instead of a crash, and save the chart as a PNG.

### AI's fix (summary)

- Increased the figure size: `plt.subplots(figsize=(10, 6))`.
- Rotated tick labels: `plt.xticks(rotation=45, ha="right")`.
- Called `plt.tight_layout()` before saving/showing so labels are not clipped.
- Added value labels above each bar and a red dashed `axhline` at 80 °C.
- Changed the y-axis label to `Average Temperature (°C)`.
- Wrapped file loading in `try/except` for `FileNotFoundError` and `json.JSONDecodeError`.
- Saved the chart to `temperature_chart.png` (`dpi=150`).

---

## 4. Result

After the follow-up, the chart rendered cleanly with readable, non-overlapping labels. The final version is in `plot_temperatures.py`.

## 5. Lesson learned

Ask for layout handling (label rotation, `tight_layout`, figure size) up front when the labels on an axis can be long or numerous, and always ask for error handling around file inputs.

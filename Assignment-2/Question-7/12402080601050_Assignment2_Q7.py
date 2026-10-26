import json

def read_file(path):
    with open(path, "r") as file:
        for line in file:
            yield line

def transform(lines):
    corrupted = 0

    for line in lines:
        try:
            data = json.loads(line)

            device = data["device_id"]
            temp = float(data["temperature_c"])
            humidity = float(data["humidity"])

            if not device or not 0 <= humidity <= 100:
                raise ValueError

            yield device, temp

        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            corrupted += 1
            yield None, corrupted

def etl(path):
    summary = {}
    corrupted = 0

    for device, value in transform(read_file(path)):
        if device is None:
            corrupted = value
            continue

        if device not in summary:
            summary[device] = {
                "count": 0, "min": value,
                "max": value, "sum": 0
            }

        s = summary[device]
        s["count"] += 1
        s["min"] = min(s["min"], value)
        s["max"] = max(s["max"], value)
        s["sum"] += value

    for device in sorted(summary):
        s = summary[device]
        avg = s["sum"] / s["count"]

        print(
            f"{device} count={s['count']} "
            f"min={s['min']:g} max={s['max']:g} "
            f"avg={avg:.2f} corrupted={corrupted}"
        )

# Run program
path = input("Enter JSONL file path: ")
etl(path)

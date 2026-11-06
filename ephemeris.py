import csv
import json
from ephemeris import interpolate_state
from io import StringIO
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"

KM_TO_M = 1000.0


def parse_ephemeris(raw_result):
    if "$$SOE" not in raw_result or "$$EOE" not in raw_result:
        raise ValueError("Invalid Horizons ephemeris response")

    data_section = raw_result.split("$$SOE", 1)[1]
    data_section = data_section.split("$$EOE", 1)[0]

    records = []

    for row in csv.reader(StringIO(data_section)):
        if not row or len(row) < 8:
            continue

        try:
            jd_tdb = float(row[0].strip())
            calendar_date = row[1].strip()

            values = [
                float(value.strip())
                for value in row[2:8]
            ]

            if not all(math.isfinite(value) for value in values):
                raise ValueError("Non-finite ephemeris value")

            x, y, z, vx, vy, vz = values

            records.append({
                "jd_tdb": jd_tdb,
                "calendar_date": calendar_date,
                "position_m": (
                    x * KM_TO_M,
                    y * KM_TO_M,
                    z * KM_TO_M,
                ),
                "velocity_m_s": (
                    vx * KM_TO_M,
                    vy * KM_TO_M,
                    vz * KM_TO_M,
                ),
            })

        except (ValueError, IndexError):
            continue

    if not records:
        raise ValueError("No valid ephemeris records found")

    return records


def fetch_ephemeris(
    target,
    start_time,
    stop_time,
    step_size="1 d",
    timeout=30,
):
    if not all(
        isinstance(value, str) and value.strip()
        for value in (target, start_time, stop_time, step_size)
    ):
        raise ValueError("Target and time parameters are required")

    parameters = {
        "format": "json",
        "COMMAND": f"'{target}'",
        "OBJ_DATA": "'YES'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'VECTORS'",
        "CENTER": "'500@10'",
        "START_TIME": f"'{start_time}'",
        "STOP_TIME": f"'{stop_time}'",
        "STEP_SIZE": f"'{step_size}'",
        "OUT_UNITS": "'KM-S'",
        "VEC_TABLE": "'2'",
        "CSV_FORMAT": "'YES'",
    }

    url = HORIZONS_URL + "?" + urlencode(parameters)

    try:
        with urlopen(url, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))

    except (HTTPError, URLError, TimeoutError) as error:
        raise RuntimeError(
            f"JPL Horizons request failed: {error}"
        ) from error

    if "error" in data:
        raise RuntimeError(data["error"])

    result = data.get("result", "")

    if not isinstance(result, str):
        raise RuntimeError("Unexpected Horizons response")

    return parse_ephemeris(result)

def interpolate_state(records, jd_tdb):
    if len(records) < 2:
        raise ValueError("At least two records are required")

    if not math.isfinite(jd_tdb):
        raise ValueError("Invalid Julian Date")

    if jd_tdb < records[0]["jd_tdb"]:
        raise ValueError("Date is before available ephemeris data")

    if jd_tdb > records[-1]["jd_tdb"]:
        raise ValueError("Date is after available ephemeris data")

    for left, right in zip(records, records[1:]):
        t0 = left["jd_tdb"]
        t1 = right["jd_tdb"]

        if t0 <= jd_tdb <= t1:
            if t1 <= t0:
                raise ValueError("Ephemeris dates must increase")

            fraction = (jd_tdb - t0) / (t1 - t0)

            position = tuple(
                a + fraction * (b - a)
                for a, b in zip(
                    left["position_m"],
                    right["position_m"],
                )
            )

            velocity = tuple(
                a + fraction * (b - a)
                for a, b in zip(
                    left["velocity_m_s"],
                    right["velocity_m_s"],
                )
            )

            return {
                "position_m": position,
                "velocity_m_s": velocity,
            }

    raise ValueError("Could not interpolate ephemeris")






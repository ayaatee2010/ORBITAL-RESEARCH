"""
ORBITAL-RESEARCH
JPL Horizons Ephemeris Engine

Retrieves, validates, and interpolates astronomical state vectors.
"""

import csv
import json
import math
from io import StringIO
from urllib.parse import urlencode
from urllib.request import Request, urlopen


HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"

KM_TO_M = 1000.0
SECONDS_PER_DAY = 86400.0


class EphemerisError(Exception):
    """Base exception for ephemeris operations."""


class EphemerisDataError(EphemerisError, ValueError):
    """Raised when ephemeris data is invalid."""


def _finite_number(value, name):
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise EphemerisDataError(f"Invalid numeric value: {name}")

    if not math.isfinite(number):
        raise EphemerisDataError(f"Non-finite value: {name}")

    return number


def _validate_vector(vector, name):
    if len(vector) != 3:
        raise EphemerisDataError(
            f"{name} must contain exactly 3 components"
        )

    result = tuple(
        _finite_number(value, name)
        for value in vector
    )

    return result


def parse_ephemeris(raw_result):
    """Parse JPL Horizons CSV vector output."""

    if not isinstance(raw_result, str):
        raise EphemerisDataError("Result must be text")

    if "$$SOE" not in raw_result or "$$EOE" not in raw_result:
        raise EphemerisDataError("Missing ephemeris data markers")

    section = raw_result.split("$$SOE", 1)[1].split("$$EOE", 1)[0]

    records = []

    for row in csv.reader(StringIO(section)):
        if len(row) < 8:
            continue

        try:
            jd = _finite_number(row[0].strip(), "Julian date")

            values = [
                _finite_number(value.strip(), "state vector")
                for value in row[2:8]
            ]

            x, y, z, vx, vy, vz = values

            record = {
                "jd_tdb": jd,
                "calendar_date": row[1].strip(),
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
            }

            records.append(record)

        except (ValueError, IndexError):
            continue

    if len(records) < 2:
        raise EphemerisDataError(
            "At least two valid ephemeris records are required"
        )

    records.sort(key=lambda record: record["jd_tdb"])

    for left, right in zip(records, records[1:]):
        if right["jd_tdb"] <= left["jd_tdb"]:
            raise EphemerisDataError(
                "Ephemeris dates must be strictly increasing"
            )

    return records


def validate_records(records):
    """Validate records before interpolation."""

    if len(records) < 2:
        raise EphemerisDataError("At least two records are required")

    validated = []

    previous_time = None

    for record in records:
        jd = _finite_number(record["jd_tdb"], "Julian date")

        position = _validate_vector(
            record["position_m"], "position"
        )

        velocity = _validate_vector(
            record["velocity_m_s"], "velocity"
        )

        if previous_time is not None and jd <= previous_time:
            raise EphemerisDataError(
                "Dates must be strictly increasing"
            )

        validated.append({
            "jd_tdb": jd,
            "position_m": position,
            "velocity_m_s": velocity,
        })

        previous_time = jd

    return validated


def interpolate_state(records, jd_tdb):
    """
    Cubic Hermite interpolation.

    Positions and velocities are interpolated together.
    Time is expressed in Julian days.
    """

    records = validate_records(records)

    jd_tdb = _finite_number(jd_tdb, "Requested Julian date")

    if jd_tdb < records[0]["jd_tdb"]:
        raise EphemerisDataError("Requested date is before available data")

    if jd_tdb > records[-1]["jd_tdb"]:
        raise EphemerisDataError("Requested date is after available data")

    for left, right in zip(records, records[1:]):

        t0 = left["jd_tdb"]
        t1 = right["jd_tdb"]

        if t0 <= jd_tdb <= t1:

            interval_days = t1 - t0
            interval_seconds = interval_days * SECONDS_PER_DAY

            u = (jd_tdb - t0) / interval_days

            h00 = 2*u**3 - 3*u**2 + 1
            h10 = u**3 - 2*u**2 + u
            h01 = -2*u**3 + 3*u**2
            h11 = u**3 - u**2

            position = []
            velocity = []

            for axis in range(3):

                p0 = left["position_m"][axis]
                p1 = right["position_m"][axis]

                v0 = left["velocity_m_s"][axis]
                v1 = right["velocity_m_s"][axis]

                p = (
                    h00*p0
                    + h10*interval_seconds*v0
                    + h01*p1
                    + h11*interval_seconds*v1
                )

                dh00 = 6*u**2 - 6*u
                dh10 = 3*u**2 - 4*u + 1
                dh01 = -6*u**2 + 6*u
                dh11 = 3*u**2 - 2*u

                v = (
                    dh00*p0
                    + dh10*interval_seconds*v0
                    + dh01*p1
                    + dh11*interval_seconds*v1
                ) / interval_seconds

                position.append(p)
                velocity.append(v)

            return {
                "position_m": tuple(position),
                "velocity_m_s": tuple(velocity),
            }

    raise EphemerisDataError("Interpolation interval not found")


def fetch_ephemeris(
    target,
    start_time,
    stop_time,
    step_size="1 d",
    timeout=30,
):
    """Download heliocentric state vectors from JPL Horizons."""

    if not target:
        raise ValueError("Target cannot be empty")

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

    request = Request(
        url,
        headers={"User-Agent": "ORBITAL-RESEARCH/1.0"}
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))

    except Exception as error:
        raise EphemerisError(
            f"JPL Horizons request failed: {error}"
        ) from error

    if "error" in payload:
        raise EphemerisError(str(payload["error"]))

    result = payload.get("result", "")

    if not result:
        raise EphemerisDataError("JPL returned no ephemeris data")

    return parse_ephemeris(result)

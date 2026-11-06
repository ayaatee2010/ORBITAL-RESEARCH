import json
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"


def fetch_ephemeris(
    target,
    start_time,
    stop_time,
    step_size="1 d",
    timeout=30,
):
    if not all(isinstance(value, str) and value.strip()
               for value in (target, start_time, stop_time, step_size)):
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
            f"Could not retrieve JPL Horizons data: {error}"
        ) from error

    if "error" in data:
        raise RuntimeError(data["error"])

    result = data.get("result", "")

    if "$$SOE" not in result or "$$EOE" not in result:
        raise RuntimeError("No ephemeris vectors found in response")

    return result

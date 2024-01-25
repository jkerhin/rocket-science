"""Take a TLE and interpolate it to ECEF position vector at time point(s) of interest

Requirements:
    1. Parse TLE into an object that Skyfield understands
    2. Convert from the TLE's reference frame into the ECEF reference frame
    3. Interpolate to / evaluate at the ECEF position at the time(s) of interest

Solution:
    1. No work at all, EarthSatellite takes TLE lines as its input
    2. Yep, instructions were super clear. Evaluate the EarthSatellite object at the time
        of interest, then do a coordinate conversion into ITRF (the formal ECEF fame that
        Skyfield uses). Then trivial to get the m / km / au / etc. accessors for position
    3. Yep, this was easy too. The Skyfield API is fantastic - accepting ranges to the
        Time() constructor? *chef's kiss*

This script is very file-oriented, and at this point it doesn't make sense to try and hook
up web API calls.
"""
import io
from datetime import datetime
from typing import Tuple, Generator

import click
from skyfield.api import load, EarthSatellite
from skyfield.framelib import itrs


def tle_3le_reader(
    hdl: io.TextIOBase,
) -> Generator[Tuple[str, str, str | None], None, None]:
    """Iterate through a 2-line (TLE) or 3-line (3LE) text file

    If the file is a 3LE, also return the satellite name, stripping the leading "0 " if
    it exists

    Yields:
        A tuple (line1, line2, sat_name) where line1 and line2 are the two lines of the
        TLE, and sat_name is either the name of the satellite (in a 3LE file) or None

    """
    line1, line2, sat_name = None, None, None
    while line := hdl.readline():
        first_char = line[0]
        if first_char not in {"1", "2"}:
            sat_name = line.strip("0 ").strip()
            continue
        if line.startswith("1 "):
            line1 = line.strip()
            continue
        if line.startswith("2 "):
            line2 = line.strip()
            yield line1, line2, sat_name
        # Reset after reading a TLE/3LE
        line1, line2, sat_name = None, None, None


@click.command()
@click.option("-f", "--file", required=True, type=click.File(encoding="utf8"))
@click.option(
    "-t", "--datetime-utc", "datetime_utc", required=True, type=click.DateTime()
)
@click.option("-d", "--duration-minutes", "duration_min", default=0, type=click.INT)
@click.option("-i", "--interval-seconds", "interval_sec", default=30, type=click.INT)
def main(file, datetime_utc: datetime, duration_min: int, interval_sec: int) -> None:
    # FIXME: Better handling of files with multiple satellites or multiple records for the
    #   same satellite
    line1, line2, sat_name = next(tle_3le_reader(file))

    ts = load.timescale()
    seconds_range = range(
        datetime_utc.second,
        (datetime_utc.second + (60 * duration_min) + 1),
        interval_sec,
    )

    # Skyfield `Time` constructor will build an array for you if you pass a range
    target_time = ts.utc(
        datetime_utc.year,
        datetime_utc.month,
        datetime_utc.day,
        datetime_utc.hour,
        datetime_utc.minute,
        seconds_range,
    )

    sat = EarthSatellite(line1, line2, ts=ts)
    geocentric = sat.at(target_time)

    x_m, y_m, z_m = geocentric.frame_xyz(itrs).m

    print(f"TLE Epoch: {sat.epoch.utc_strftime()}")
    print(f"Seconds past midnight on {datetime_utc:%Y-%m-%d}:")
    for tt, x, y, z in zip(target_time, x_m, y_m, z_m):
        midnight = tt.utc_datetime().replace(hour=0, minute=0, second=0, microsecond=0)
        sec_past_midnight = (tt.utc_datetime() - midnight).total_seconds()
        print(f"{sec_past_midnight} [{x}, {y}, {z}]")


if __name__ == "__main__":
    main()

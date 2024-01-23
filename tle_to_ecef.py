"""Goal: Take a TLE and interpolate it to ECEC position (and velocity?) vector at time
point(s) of interest

Requirements:
    1. Parse TLE into an object that Skyfield understands
    2. Convert from the TLE's reference frame into the ECEF reference frame
    3. Interpolate to / evaluate at the ECEF position at the time(s) of interest

Solution:
    1. No work at all, EarthSatellite takes TLE lines as its input
    2. Yep, instructions were super clear. Evaluate the EarthSatellite object at the time
        of interest, then do a coordinate conversion into ITRF (the formal ECEF fame that
        Skyfield uses). Then trivial to get the m / km / au / etc. accessors for position
    3. TODO, but expect this to be pretty simple. I'm guessing Skyfield has some kind of
        time series object, just need to find it.

TODO (maybe?):
    Hook in to Space-Track.org and make queries automatically

"""
from datetime import timezone

import click
from skyfield.api import load, EarthSatellite
from skyfield.framelib import itrs


@click.command()
@click.option("-f", "--file", required=True, type=click.File(encoding="utf8"))
@click.option("-t", "--datetime", "datetime_utc", required=True, type=click.DateTime())
def main(file, datetime_utc):
    # FIXME: Error handling. This is very brittle
    line1, line2 = file.read().splitlines()

    ts = load.timescale()
    target_time = ts.from_datetime(datetime_utc.replace(tzinfo=timezone.utc))

    sat = EarthSatellite(line1, line2, ts=ts)
    geocentric = sat.at(target_time)

    x_m, y_m, z_m = geocentric.frame_xyz(itrs).m
    print(f"TLE Epoch {sat.epoch.utc_strftime()}: [{x_m}, {y_m}, {z_m}]")


if __name__ == "__main__":
    main()

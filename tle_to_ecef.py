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

"""
import itertools

from skyfield.api import load, EarthSatellite
from skyfield.framelib import itrs


# For now, don't mess with any web requests, just use the data we already pulled
TEST_TLE_RAW = r"""1 25544U 98067A   24022.87893601  .00024790  00000-0  44442-3 0  9995
2 25544  51.6428 320.3213 0004960 119.4797 344.6223 15.49770630435861
1 25544U 98067A   24022.67711117  .00024600  00000-0  44125-3 0  9992
2 25544  51.6436 321.3220 0004878 117.8594 299.4871 15.49761122435833
1 25544U 98067A   24022.37051078  .00025408  00000-0  45565-3 0  9998
2 25544  51.6435 322.8411 0004875 117.1497  28.5107 15.49747298435787
1 25544U 98067A   24022.37051078  .00024539  00000-0  44042-3 0  9991
2 25544  51.6431 322.8396 0005033 117.7562  27.8997 15.49743990435785
1 25544U 98067A   24022.24140652  .00024460  00000-0  43914-3 0  9994
2 25544  51.6428 323.4802 0005134 117.8798  27.0182 15.49737190435765
1 25544U 98067A   24022.21547817  .00021802  00000-0  39246-3 0  9995
2 25544  51.6402 323.6135 0004839 117.3161 242.8321 15.49735823435761"""


def main():
    tle_lines = TEST_TLE_RAW.splitlines()

    ts = load.timescale()
    target_time = ts.utc(2024, 1, 22, 0, 0, 0)

    # NB: itertools.batched() was introduced in Python3.12
    for line1, line2 in itertools.batched(tle_lines, n=2):
        sat = EarthSatellite(line1, line2, "ISS (ZARYA)", ts)
        geocentric = sat.at(target_time)
        x_m, y_m, z_m = geocentric.frame_xyz(itrs).m
        print(f"TLE Epoch {sat.epoch.utc_strftime()}: [{x_m}, {y_m}, {z_m}]")


if __name__ == "__main__":
    main()

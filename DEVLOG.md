# Starting point

hey I owe you some info on the python package I'd recommend for working with TLEs and coordinate conversions from that reference frame to ECF. So here's the info:

The package is skyfield: Positions — Skyfield documentation (rhodesmill.org) https://rhodesmill.org/skyfield/positions.html

Positions should be able to be operated on vectorized and use this class: API Reference — Units — Skyfield documentation (rhodesmill.org) https://rhodesmill.org/skyfield/api-units.html#skyfield.units.Distance

What you really want is to call the frame_xyz(frame) function to convert to the frame you need: API Reference — Astronomical Positions — Skyfield documentation (rhodesmill.org) https://rhodesmill.org/skyfield/api-position.html#skyfield.positionlib.ICRF.frame_xyz

And then the reference frame you want to be passing to that function to get ECF is framelib.ITRF (ITRF = ECF, the T is Terrestrial, and the I is NOT inertial) API Reference — Reference Frames — Skyfield documentation (rhodesmill.org) https://rhodesmill.org/skyfield/api-framelib.html

And then finally, note that they have a good overview on how to get the position from a TLE: Earth Satellites — Skyfield documentation (rhodesmill.org) https://rhodesmill.org/skyfield/earth-satellites.html#generating-a-satellite-position

# ISS as a Proxy

ISS is as good of a space object as any to track 😊

SATCAT ID is 25544

# Approach

To start with, I'm going to focus on TLEs, because that's what I _know_ I'm going to
have access to. Ideally I'd be using the JSON or some other format, but for now lets
learn to use TLEs

# Sample ISS data

```
1 25544U 98067A   24022.87893601  .00024790  00000-0  44442-3 0  9995
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
2 25544  51.6402 323.6135 0004839 117.3161 242.8321 15.49735823435761
```

# Things learned along the way

TLEs have a short "shelf life". This isn't really surprising, but good to hear it
explicitly called out:

> Satellite elements go rapidly out of date. As explained below in Checking a TLE’s epoch, you will want to pay attention to the “epoch” — the date on which an element set is most accurate — of every TLE element set you use. Elements are only useful for a week or two on either side of the epoch date. For later dates, you will want to download a fresh set of elements. For earlier dates, you will want to pull an old TLE from the archives.

[Source](https://rhodesmill.org/skyfield/earth-satellites.html)

May be an interesting test to pick a "target date/time" in the middle of a set of TLEs,
and see how the position changes over time. I.e. if 20 days of TLEs, pick midnight on
Day 10 TLE and then calculate how far away the Day 0 / Day 20 interpolated positions are

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

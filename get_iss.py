"""Sample script to authenitcate and then grab a single TLE"""
import os

import httpx


URL_BASE = "https://www.space-track.org"


def get_httpx_session() -> httpx.Client:
    user = os.getenv("SPACETRACK_USER")
    if not (pass_ := os.getenv("SPACETRACK_PASS")):
        raise RuntimeError("Couldn't get password from SPACETRACK_PASS")
    ses = httpx.Client(follow_redirects=True, http2=True)
    r = ses.post(
        f"{URL_BASE}/ajaxauth/login", data={"identity": user, "password": pass_}
    )
    r.raise_for_status()
    return ses


def main():
    """This API is nuts; nested formats and queries/directives...

    Example from:
        https://www.space-track.org/documentation#api-sampleQueries

    NB: ISS NORAD / SATCAT ID is 25544

    """
    endpoint = "basicspacedata/query/class/gp_history/format/tle/NORAD_CAT_ID/25544/orderby/EPOCH desc/limit/10"
    ses = get_httpx_session()
    r = ses.get(f"{URL_BASE}/{endpoint}")
    r.raise_for_status()
    print(r.headers)
    print(r.text)


if __name__ == "__main__":
    main()

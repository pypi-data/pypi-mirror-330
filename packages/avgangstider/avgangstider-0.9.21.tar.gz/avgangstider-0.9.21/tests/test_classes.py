"""Tests for the classes module."""

import datetime

from freezegun import freeze_time

import avgangstider.classes


@freeze_time("2019-01-01T12:00:00+01:00")
def test_util() -> None:
    """Test the Departure class."""
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    departure = avgangstider.classes.Departure(
        line_id="RUT:Line:0",
        line_name="",
        destination="",
        platform="NSR:Quay:0",
        departure_datetime=now,
        bg_color="000000",
        fg_color="FFFFFF",
    )

    # Check the departure string for different timedelta's
    departure.departure_datetime = now + datetime.timedelta(seconds=59)
    assert departure.departure_string == "nå"

    departure.departure_datetime = now + datetime.timedelta(minutes=30)
    assert departure.departure_string == "30 min"

    departure.departure_datetime = now + datetime.timedelta(minutes=31)
    time_string = departure.departure_datetime.strftime("%H:%M")
    assert departure.departure_string == time_string

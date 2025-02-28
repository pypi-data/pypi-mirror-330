"""Tests for the entur_api module."""

import requests_mock
from freezegun import freeze_time

import avgangstider


def test_get_departures() -> None:  # noqa: D103
    # Test with an empty string as stop_id:
    departures = avgangstider.get_departures(stop_id="")
    assert departures == []

    # Test with an invalid stop_id:
    departures = avgangstider.get_departures(stop_id="InvalidStopId")
    assert departures == []

    # Test without specifying line_ids
    # At Godlia T, the only passing line is 3, and there is only two quays
    departures = avgangstider.get_departures(
        stop_id="NSR:StopPlace:5968", max_departures=10
    )
    assert len(departures) == 10
    for departure in departures:
        assert departure.line_name == "3"
        assert departure.platform in ("NSR:Quay:10948", "NSR:Quay:10949")

    # Test querying a specific line (bus 21 from Helsfyr)
    departures = avgangstider.get_departures(
        "NSR:StopPlace:59516", max_departures=10, line_ids=["RUT:Line:21"]
    )
    assert len(departures) == 10
    for departure in departures:
        assert departure.line_name == "21"

    # Test querying a specific platform (Godlia T, only towards Mortensrud)
    departures = avgangstider.get_departures(
        stop_id="NSR:StopPlace:5968", platforms=["NSR:Quay:10948"]
    )
    assert departures
    for departure in departures:
        assert departure.line_name == "3"
        assert departure.platform == "NSR:Quay:10948"
        assert "3  -> Mortensrud" in str(departure)


@freeze_time("2025-01-26T18:00:00+01:00")
def test_get_situations_mocked_1(mocked_situations: requests_mock.Mocker) -> None:  # noqa: ARG001
    """Test get_situations with mocked data."""
    situations = avgangstider.get_situations(line_ids=[])

    assert len(situations) == 2
    assert (
        situations[0].summary
        == "T-banen stopper ikke på Nationaltheatret i vestgående retning"
    )


@freeze_time("2025-01-27T22:00:00+01:00")
def test_get_situations_mocked_2(mocked_situations: requests_mock.Mocker) -> None:  # noqa: ARG001
    """Test get_situations with mocked data."""
    situations = avgangstider.get_situations(line_ids=[])

    assert len(situations) == 2
    assert situations[0].summary == "Linje 2: Endret kjøremønster på kveldstid"


def test_get_situations() -> None:  # noqa: D103
    # Test without specifying line_ids
    situations = avgangstider.get_situations(line_ids=[])
    assert situations == []

    # Test with an invalid line number
    situations = avgangstider.get_situations(line_ids=["RUT:Line:0"])
    assert situations == []

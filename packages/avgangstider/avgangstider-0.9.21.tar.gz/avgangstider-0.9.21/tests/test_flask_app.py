"""Tests for the Flask app."""

import requests_mock
from flask.testing import FlaskClient
from freezegun import freeze_time


def test_static(client: FlaskClient) -> None:  # noqa: D103
    response = client.get("/static/css/dinfont.css")
    assert response.status_code == 200
    assert b"font-face" in response.data


def test_app_without_stop_id(client: FlaskClient) -> None:  # noqa: D103
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Examples" in response.data


def test_app(client: FlaskClient) -> None:  # noqa: D103
    response = client.get("/", query_string={"stop_id": "NSR:StopPlace:58366"})
    assert response.status_code == 200
    assert b"DepartureTable" in response.data

    # Call again, but with a new stop_id
    response = client.get("/", query_string={"stop_id": "NSR:StopPlace:59872"})
    assert response.status_code == 200
    assert b"DepartureTable" in response.data


def test_departure_table(client: FlaskClient) -> None:  # noqa: D103
    # Get departures with an empty stop_id
    response = client.get("/departure_table", query_string={"stop_id": None})
    assert response.status_code == 200

    # Get departures with a valid stop_id
    response = client.get(
        "/departure_table", query_string={"stop_id": "NSR:StopPlace:58366"}
    )
    assert response.status_code == 200

    # Get departures with a valid stop_id and a line_id
    response = client.get(
        "/departure_table",
        query_string={"stop_id": "NSR:StopPlace:58366", "line_id": "RUT:Line:3"},
    )
    assert response.status_code == 200


def test_deviations(client: FlaskClient) -> None:  # noqa: D103
    # Try first without having got any departures
    # There should be no situations
    response = client.get(
        "/deviations", query_string={"stop_id": "NSR:StopPlace:58366"}
    )
    assert response.status_code == 200
    assert response.data == b""

    # First, get some departures
    client.get("/departure_table", query_string={"stop_id": "NSR:StopPlace:58366"})
    # Then get situations again
    response = client.get(
        "/deviations", query_string={"stop_id": "NSR:StopPlace:58366"}
    )
    assert response.status_code == 200


def test_deviations_with_line(client: FlaskClient) -> None:  # noqa: D103
    response = client.get(
        "/deviations",
        query_string={"stop_id": "NSR:StopPlace:58366", "line_id": "RUT:Line:3"},
    )
    assert response.status_code == 200


@freeze_time("2025-01-26T18:00:00+01:00")
def test_deviations_mocked(
    client: FlaskClient,
    mocked_situations: requests_mock.Mocker,  # noqa: ARG001
) -> None:
    """Test deviations endpoint with mocked data."""
    client.get("/departure_table", query_string={"stop_id": "NSR:StopPlace:58366"})

    response = client.get(
        "/deviations", query_string={"stop_id": "NSR:StopPlace:58366"}
    )
    assert response.status_code == 200
    assert (
        response.data.decode("utf-8")
        == "2: T-banen stopper ikke på Nationaltheatret i vestgående retning"
    )

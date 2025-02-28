"""Get departures and situations from the Entur API."""

import datetime

from loguru import logger

from avgangstider import Departure, Situation, entur_query


def get_departures(
    stop_id: str,
    line_ids: list[str] | None = None,
    platforms: list[str] | None = None,
    max_departures: int = 10,
) -> list[Departure]:
    """Query the Entur API and return a list of matching departures.

    Args:
        stop_id: The stop_id you want departures for
        line_ids: An optional list with line_ids
        platforms: An optional list with platform_ids
        max_departures: The maximum number of departures to query for

    Returns:
        A list of departures
    """
    if line_ids is None:
        line_ids = []

    # Get response from Entur API
    json = entur_query.departure_line_query_data(
        stop_id=stop_id, line_ids=line_ids, max_departures=max_departures
    )

    # Return an empty list if there is no valid data
    try:
        json["data"]["stopPlace"]["estimatedCalls"]
    except (TypeError, KeyError):
        return []

    departures: list[Departure] = []
    for journey in json["data"]["stopPlace"]["estimatedCalls"]:
        # Extract the elements we want from the response
        line_id = journey["serviceJourney"]["line"]["id"]
        line_name = journey["serviceJourney"]["line"]["publicCode"]
        bg_color = journey["serviceJourney"]["line"]["presentation"]["colour"]
        fg_color = journey["serviceJourney"]["line"]["presentation"]["textColour"]
        platform = journey["quay"]["id"]
        destination = journey["destinationDisplay"]["frontText"]
        departure_datetime = datetime.datetime.fromisoformat(
            journey["expectedDepartureTime"]
        )

        # Skip unwanted platforms
        if platforms and (platform not in platforms):
            continue

        # Add departure to the list
        departure = Departure(
            line_id=line_id,
            line_name=line_name,
            destination=destination,
            departure_datetime=departure_datetime,
            platform=platform,
            fg_color=fg_color,
            bg_color=bg_color,
        )
        departures.append(departure)

    return departures


def get_situations(line_ids: list[str], language: str = "no") -> list[Situation]:
    """Query the Entur API and return a list of relevant situations.

    Args:
        line_ids: A list of strings with line_ids
        language: A language string: 'en' or 'no'

    Returns:
        A list of relevant situations for that line
    """
    logger.debug(f"Getting situations for lines {line_ids}.")

    json = entur_query.situation_query_data(line_ids)

    # Return an empty list if there is no valid data
    try:
        json["data"]["lines"]
    except (TypeError, KeyError):
        return []

    situations: list[Situation] = []
    for line in json["data"]["lines"]:
        if not line:
            # Might be empty if line_id is non-existing
            continue

        # Extract some general information about the line
        line_id = line["id"]
        line_name = line["publicCode"]
        transport_mode = line["transportMode"]
        fg_color = line["presentation"]["textColour"]
        bg_color = line["presentation"]["colour"]

        for situation in line["situations"]:
            # Extract the fields we need from the response
            start_time = situation["validityPeriod"]["startTime"]
            end_time = situation["validityPeriod"]["endTime"]

            # Find start, end and current timestamp
            start_time = datetime.datetime.fromisoformat(start_time)
            end_time = datetime.datetime.fromisoformat(end_time)
            now = datetime.datetime.now(tz=start_time.tzinfo)

            # Add relevant situations to the list
            if start_time < now < end_time:
                for summary in situation["summary"]:
                    if summary["language"] == language:
                        situations.append(
                            Situation(
                                line_id=line_id,
                                line_name=line_name,
                                transport_mode=transport_mode,
                                fg_color=fg_color,
                                bg_color=bg_color,
                                summary=summary["value"],
                            )
                        )

    return sorted(situations)

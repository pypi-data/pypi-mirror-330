"""Query the Entur Journey Planner API for departures and situations."""

from typing import Any

import requests

from avgangstider.constants import API_URL

# For testing and debugging of queries, use this page:
# https://api.entur.io/graphql-explorer/journey-planner-v3


def departure_line_query_data(
    stop_id: str, line_ids: list[str], max_departures: int = 10
) -> dict[str, Any]:
    """Get GraphQL query data.

    Finding departures for a specific stop_id, and for specific line_ids.

    Args:
        stop_id: The stop_id you want departures for
        line_ids: A list of the lines you want departures for, can be empty
        max_departures: The maximum number of departures to ask for

    Returns:
        A GraphQL query string
    """
    query = """
query Departures($id: String!, $line_ids: [ID], $max_departures: Int) {
  stopPlace(
    id: $id
  ) {
    name
    estimatedCalls(
      numberOfDepartures: $max_departures,
      whiteListed: {
        lines: $line_ids
      }
    ) {
      expectedArrivalTime
      expectedDepartureTime
      quay {
        id
        description
      }
      destinationDisplay {
        frontText
      }
      serviceJourney {
        line {
          id
          publicCode
          presentation {
            colour
            textColour
          }
        }
      }
    }
  }
}
"""
    variables = {"id": stop_id, "line_ids": line_ids, "max_departures": max_departures}
    return journey_planner_api(query, variables).json()


def situation_query_data(line_ids: list[str]) -> dict[str, Any]:
    """Get GraphQL query data: Situations for a list of line_ids.

    Args:
        line_ids: A list of line_ids you want situations for

    Returns:
        A GraphQL query string
    """
    query = """
query Situations($line_ids: [ID]) {
  lines(
    ids: $line_ids
  ) {
    id
    publicCode
    transportMode
    presentation {
      textColour
      colour
    }
    situations {
      summary {
        value
        language
      }
      description {
        value
        language
      }
      advice {
        value
        language
      }
      validityPeriod {
        startTime
        endTime
      }
    }
  }
}
"""
    variables = {"line_ids": line_ids}
    return journey_planner_api(query, variables).json()


def journey_planner_api(query: str, variables: dict[str, Any]) -> requests.Response:
    """Query the Entur Journey Planner API.

    Args:
        query: A string with the GraphQL query
        variables: A dictionary with the variables for the query

    Returns:
        A requests response object
    """
    import socket

    headers = {"ET-Client-Name": f"avgangstider-{socket.gethostname()}"}
    response = requests.post(
        API_URL,
        headers=headers,
        json={"query": query, "variables": variables},
        timeout=5,
    )
    response.raise_for_status()

    return response

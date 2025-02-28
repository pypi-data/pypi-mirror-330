"""Package for fetching public transport departure times from Entur's API."""

import importlib.metadata

from avgangstider.classes import Departure, Situation
from avgangstider.entur_api import get_departures, get_situations
from avgangstider.flask_app import create_app

__all__ = ["Departure", "Situation", "create_app", "get_departures", "get_situations"]

__version__ = importlib.metadata.version(__package__)

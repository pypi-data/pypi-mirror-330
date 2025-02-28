"""Defines fixtures for the test suite."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import requests_mock
from flask import Flask

import avgangstider
from avgangstider.constants import API_URL


@pytest.fixture
def mocked_situations(requests_mock: requests_mock.Mocker) -> requests_mock.Mocker:
    """Mock the Entur Journey Planner API with the contents of situations.json."""
    file = Path(__file__).parent / "saved_responses" / "situations.json"
    data = json.loads(file.read_text())
    requests_mock.post(API_URL, json=data)
    return requests_mock


@pytest.fixture
def app() -> Flask:  # noqa: D103
    return avgangstider.create_app()

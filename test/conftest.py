"""Shared fixtures: one in-memory build of the repository, so tests read what the build writes without touching disk."""
import json
from typing import Any

import pytest

from build import Plan, plan_build
from config import ROOT


@pytest.fixture(scope="session")
def plan() -> Plan:
    return plan_build(ROOT)


@pytest.fixture(scope="session")
def site_text(plan: Plan) -> dict[str, str]:
    """Every text file the build would write to site/, by relative path."""
    return {name: data.decode() for name, data in plan.site.items() if not name.endswith(".png")}


@pytest.fixture
def cards_json(site_text: dict[str, str]) -> dict[str, Any]:
    data: dict[str, Any] = json.loads(site_text["cards.json"])
    return data

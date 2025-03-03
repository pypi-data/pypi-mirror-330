"""Tests for the oocone.Enocoo.get_area_ids() method."""

import datetime as dt

import pytest

from oocone import Auth, Enocoo
from oocone.model import Area
from tests import TIMEZONE
from tests.conftest import MockApiParams


@pytest.mark.asyncio
# @pytest.mark.parametrize("dataset", MOCK_API_DATASET_NAMES)
@pytest.mark.parametrize(
    ("dataset", "expected_areas"),
    [
        (
            "one_area",
            [
                Area(
                    name="H12W34",
                    id="123",
                    data_available_since=dt.date(2021, 1, 1),
                    data_available_until=dt.date(2022, 2, 2),
                )
            ],
        ),
        (
            "two_areas",
            [
                Area(
                    name="H12W34",
                    id="123",
                    data_available_since=dt.date(2021, 1, 1),
                    data_available_until=dt.date(2021, 1, 1),
                ),
                Area(
                    name="SP567 TNr:890",
                    id="124",
                    data_available_since=dt.date(2021, 1, 1),
                    data_available_until=dt.date(2021, 1, 1),
                ),
            ],
        ),
    ],
)
async def test_happy_path(
    dataset: str, expected_areas: list[Area], mock_auth: Auth, mock_api_params: MockApiParams
) -> None:
    """Check that enocoo.get_areas returns the areas as indicated in ownConsumption.php."""
    mock_api_params.dataset_name = dataset
    enocoo = Enocoo(mock_auth, TIMEZONE)

    areas = await enocoo.get_areas()
    assert areas == expected_areas

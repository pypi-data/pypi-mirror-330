"""Module containing the main API entry points for this module."""

from __future__ import annotations

import datetime as dt
import logging
import warnings
from typing import TYPE_CHECKING, Literal

from oocone import errors
from oocone._internal import (
    quirks,
    scrape_consumption,
    scrape_meter_table,
    scrape_photovoltaic,
    scrape_traffic_light,
)

if TYPE_CHECKING:
    from oocone.auth import Auth
    from oocone.model import (
        Area,
        Consumption,
        ConsumptionType,
        MeterStatus,
        PhotovoltaicSummary,
        TrafficLightStatus,
    )

ROUTE_LOGIN = "/signinForm.php?mode=ok"
BEAUTIFULSOUP_PARSER = "html.parser"

logger = logging.getLogger(__name__)


class Enocoo:
    """Provides access to the data accessible via the enocoo Web interface."""

    def __init__(self, auth: Auth, timezone: dt.tzinfo) -> None:
        """
        Initialize the API and store the auth so we can make requests.

        Parameters
        ----------
        auth
            Indicates how to contact the enocoo dashboard, including URL and credentials.
        timezone
            The timezone in which the building of the energy management system is located.

        """
        self.auth = auth
        self.timezone = timezone

    async def get_traffic_light_status(self) -> TrafficLightStatus:
        """Return the status of the energy traffic light."""
        return await scrape_traffic_light.get_traffic_light_status(self.auth)

    async def get_meter_table(
        self,
        date: dt.date | None = None,
        allow_previous_day_until: dt.time | None = None,
    ) -> list[MeterStatus]:
        """
        Return the status of all individual consumption meters available in the dashboard.

        Parameters
        ----------
        date
            The date for which meter data should be fetched.
            If left to None: the current day.
        allow_previous_day_until:
            If set, data from the previous day might be returned if the timestamp is at least the
            value of this parameter.

        """
        if date is None:
            date = dt.datetime.now(tz=self.timezone).date()

        meter_table = await scrape_meter_table.get_meter_table(
            date=date,
            timezone=self.timezone,
            auth=self.auth,
        )

        if not meter_table:
            day_before = date - dt.timedelta(days=1)
            meter_table_day_before = await scrape_meter_table.get_meter_table(
                date=day_before,
                timezone=self.timezone,
                auth=self.auth,
            )

            def status_is_relevant(status: MeterStatus) -> bool:
                relevant = False
                if status.timestamp.date() == date:
                    # status is from today -> relevant
                    relevant = True
                elif (
                    allow_previous_day_until is not None
                    and status.timestamp.time() >= allow_previous_day_until
                    and status.timestamp.date() == (date - dt.timedelta(days=1))
                ):
                    # status is declared relevant explicitly by user wishes
                    relevant = True
                return relevant

            meter_table = [s for s in meter_table_day_before if status_is_relevant(s)]
            logger.debug(
                "Found %s relevant meter statuses from the day before (%s), returning those...",
                len(meter_table),
                day_before,
            )

        return meter_table

    async def get_areas(self) -> list[Area]:
        """Get all available areas via the dashboard."""
        return await scrape_consumption.get_areas(auth=self.auth)

    async def get_individual_consumption(
        self,
        consumption_type: ConsumptionType,
        during: dt.date,
        interval: Literal["day", "month", "year"],
        area_id: str,
        compensate_off_by_one: bool | None = None,
    ) -> list[Consumption]:
        """Return individual consumption statistics for a given meter type."""
        if compensate_off_by_one is None:
            compensate_off_by_one = interval == "day"

        if compensate_off_by_one and interval != "day":
            warnings.warn(
                "Data points in the enocoo dashboard are off by one. Compensation for this is only"
                " available when fetching daily consumption statistics.",
                stacklevel=1,
            )
            compensate_off_by_one = False

        async def fetch_data(date: dt.date) -> list[Consumption]:
            return await self._get_individual_consumption_uncompensated(
                consumption_type=consumption_type, during=date, interval=interval, area_id=area_id
            )

        if compensate_off_by_one:
            result = await quirks.get_off_by_one_compensated_data(
                fetch_data=fetch_data,
                date=during,
                timezone=self.timezone,
            )
        else:
            result = await fetch_data(date=during)

        return result

    async def _get_individual_consumption_uncompensated(
        self,
        consumption_type: ConsumptionType,
        during: dt.date,
        interval: Literal["day", "month", "year"],
        area_id: str,
    ) -> list[Consumption]:
        match interval:
            case "day":
                return await scrape_consumption.get_daily_consumption(
                    consumption_type=consumption_type,
                    area_id=area_id,
                    date=during,
                    timezone=self.timezone,
                    auth=self.auth,
                )
            case "month":
                return await scrape_consumption.get_monthly_consumption(
                    consumption_type=consumption_type,
                    area_id=area_id,
                    date=during,
                    timezone=self.timezone,
                    auth=self.auth,
                )
            case "year":
                return await scrape_consumption.get_yearly_consumption(
                    consumption_type=consumption_type,
                    area_id=area_id,
                    year_number=during.year,
                    timezone=self.timezone,
                    auth=self.auth,
                )
            case _:
                msg = f'Illegal interval "{interval}"'
                raise errors.OoconeMisuse(msg)

    async def get_quarter_photovoltaic_data(
        self,
        during: dt.date,
        interval: Literal["day", "month"],
    ) -> list[PhotovoltaicSummary]:
        """Return photovoltaic data for the whole quarter."""
        match interval:
            case "day":
                return await scrape_photovoltaic.get_daily_photovoltaic_data(
                    date=during, timezone=self.timezone, auth=self.auth
                )
            case "month":
                return await scrape_photovoltaic.get_monthly_photovoltaic_data(
                    date=during, timezone=self.timezone, auth=self.auth
                )
            case _:
                msg = f'Illegal interval "{interval}"'
                raise errors.OoconeMisuse(msg)

from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

from hypothesis import given
from hypothesis.strategies import DataObject, data, datetimes, sampled_from, timezones
from pytest import mark, param, raises

from utilities.hypothesis import zoned_datetimes
from utilities.zoneinfo import (
    UTC,
    HongKong,
    Tokyo,
    USCentral,
    USEastern,
    _EnsureTimeZoneInvalidTZInfoError,
    _EnsureTimeZoneLocalDateTimeError,
    ensure_time_zone,
    get_time_zone_name,
)


class TestGetTimeZoneName:
    @given(data=data())
    @mark.parametrize(
        "time_zone",
        [
            param("Asia/Hong_Kong"),
            param("Asia/Tokyo"),
            param("US/Central"),
            param("US/Eastern"),
            param("UTC"),
        ],
    )
    def test_main(self, *, data: DataObject, time_zone: str) -> None:
        zone_info_or_str = data.draw(sampled_from([ZoneInfo(time_zone), time_zone]))
        result = get_time_zone_name(zone_info_or_str)
        assert result == time_zone


class TestEnsureZoneInfo:
    @given(data=data())
    @mark.parametrize(
        ("time_zone", "expected"),
        [
            param(HongKong, HongKong),
            param(Tokyo, Tokyo),
            param(USCentral, USCentral),
            param(USEastern, USEastern),
            param(UTC, UTC),
            param(dt.UTC, UTC),
        ],
    )
    def test_time_zone(
        self, *, data: DataObject, time_zone: ZoneInfo | dt.timezone, expected: ZoneInfo
    ) -> None:
        zone_info_or_str = data.draw(
            sampled_from([time_zone, get_time_zone_name(time_zone)])
        )
        result = ensure_time_zone(zone_info_or_str)
        assert result is expected

    @given(data=data(), time_zone=timezones())
    def test_zoned_datetime(self, *, data: DataObject, time_zone: ZoneInfo) -> None:
        datetime = data.draw(zoned_datetimes(time_zone=time_zone))
        result = ensure_time_zone(datetime)
        assert result is time_zone

    def test_error_invalid_tzinfo(self) -> None:
        time_zone = dt.timezone(dt.timedelta(hours=12))
        with raises(
            _EnsureTimeZoneInvalidTZInfoError, match="Unsupported time zone: .*"
        ):
            _ = ensure_time_zone(time_zone)

    @given(datetime=datetimes())
    def test_error_local_datetime(self, *, datetime: dt.datetime) -> None:
        with raises(_EnsureTimeZoneLocalDateTimeError, match="Local datetime: .*"):
            _ = ensure_time_zone(datetime)


class TestTimeZones:
    @mark.parametrize(
        "time_zone", [param(HongKong), param(Tokyo), param(USCentral), param(USEastern)]
    )
    def test_main(self, *, time_zone: ZoneInfo) -> None:
        assert isinstance(time_zone, ZoneInfo)

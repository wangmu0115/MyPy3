from datetime import datetime, timedelta, timezone
from functools import singledispatchmethod

# https://docs.python.org/3/library/datetime.html
DT_DEFAULT_FORMATS = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y%m%d_%H%M%S", "%Y%m%d_%H%M"]


class DatetimeParser:
    """A parser uesd to parse datetime string or timestamp to `datetime`.
    Supported datetime formats are defined by `formats` attribute.
    The attributes `tz_hours` and `tz_minutes` determine the timezone of the converted datetime.

    Attributes:
        formats: supported datetime formats
        tz_hours: timezone delta hours
        tz_minutes: timezone delta minutes
    """

    def __init__(self, formats: list[str] | None = None, tz_hours: int = 8, tz_minutes: int = 0):
        self.formats = formats or DT_DEFAULT_FORMATS
        self.tzinfo = timezone(timedelta(hours=tz_hours, minutes=tz_minutes))
        self.max_seconds = int(datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=self.tzinfo).timestamp())

    @singledispatchmethod
    def parse(self, dt: str | int | float, *args) -> datetime | None:
        """Parse datetime string or timestamp to `datetime`.
        If dt is `str`, parse by formats.
        If dt is `int` or `float`, parse by timestamp.
        Otherwise, return `None`.

        Raises:
            ValueError: If format mismatch or timestamp out of range.
        """

    @parse.register
    def _(self, dt_string: str, replace_tz: bool = True) -> datetime:
        for format in self.formats:
            try:
                dt = datetime.strptime(dt_string, format)
                break
            except ValueError:
                ...  # mismatch format
        if dt is None:
            raise ValueError(f"Unsupported datetime format: {dt_string}, expected formats: {self.formats}")
        return dt.replace(tzinfo=self.tzinfo) if replace_tz else dt

    @parse.register
    def _(self, timestamp: int | float, overflow_as_ms: bool = True) -> datetime:
        # 9999-12-31 23:59:59.999999+00:00 timestamp is 253402300800
        if timestamp >= self.max_seconds:  # as millisecond
            if overflow_as_ms:
                return datetime.fromtimestamp(timestamp / 1000, tz=self.tzinfo)
            else:
                raise ValueError(f"Timestamp({timestamp}) out of range, seconds must less than {self.max_seconds}.")
        else:
            return datetime.fromtimestamp(timestamp, tz=self.tzinfo)

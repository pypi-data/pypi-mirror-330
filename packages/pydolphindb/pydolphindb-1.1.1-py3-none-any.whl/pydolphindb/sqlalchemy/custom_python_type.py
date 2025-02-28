import pandas as pd

# Custom python type for DolphinDB data types


class Date:
    timestamp: pd.Timestamp

    def __init__(self, timestamp):
        if isinstance(timestamp, pd.Timestamp):
            self.timestamp = timestamp
        elif isinstance(timestamp, str) or isinstance(timestamp, int):
            self.timestamp = pd.Timestamp(timestamp)
        else:
            raise ValueError("Invalid type for Date")

    def __str__(self):
        return f"{self.timestamp.year:04d}.{self.timestamp.month:02d}.{self.timestamp.day:02d}"


class Month:
    timestamp: pd.Timestamp

    def __init__(self, timestamp):
        if isinstance(timestamp, pd.Timestamp):
            self.timestamp = timestamp
        elif isinstance(timestamp, str) or isinstance(timestamp, int):
            self.timestamp = pd.Timestamp(timestamp)
        else:
            raise ValueError("Invalid type for Month")

    def __str__(self):
        return f"{self.timestamp.year:04d}.{self.timestamp.month:02d}"


class Time:
    timestamp: pd.Timestamp

    def __init__(self, timestamp):
        if isinstance(timestamp, pd.Timestamp):
            self.timestamp = timestamp
        elif isinstance(timestamp, str) or isinstance(timestamp, int):
            self.timestamp = pd.Timestamp(timestamp)
        else:
            raise ValueError("Invalid type for Time")

    def __str__(self):
        return f"{self.timestamp.hour:02d}:{self.timestamp.minute:02d}:{self.timestamp.second:02d}.{self.timestamp.microsecond//1000:03}"


class Minute:
    timestamp: pd.Timestamp

    def __init__(self, timestamp):
        if isinstance(timestamp, pd.Timestamp):
            self.timestamp = timestamp
        elif isinstance(timestamp, str) or isinstance(timestamp, int):
            self.timestamp = pd.Timestamp(timestamp)
        else:
            raise ValueError("Invalid type for Minute")

    def __str__(self):
        return f"{self.timestamp.hour:02d}:{self.timestamp.minute:02d}"


class Second:
    timestamp: pd.Timestamp

    def __init__(self, timestamp):
        if isinstance(timestamp, pd.Timestamp):
            self.timestamp = timestamp
        elif isinstance(timestamp, str) or isinstance(timestamp, int):
            self.timestamp = pd.Timestamp(timestamp)
        else:
            raise ValueError("Invalid type for Second")

    def __str__(self):
        return f"{self.timestamp.hour:02d}:{self.timestamp.minute:02d}:{self.timestamp.second:02d}"


class DateTime:
    timestamp: pd.Timestamp

    def __init__(self, timestamp):
        if isinstance(timestamp, pd.Timestamp):
            self.timestamp = timestamp
        elif isinstance(timestamp, str) or isinstance(timestamp, int):
            self.timestamp = pd.Timestamp(timestamp)
        else:
            raise ValueError("Invalid type for DateTime")

    def __str__(self):
        return f"{self.timestamp.year:04d}.{self.timestamp.month:02d}.{self.timestamp.day:02d} {self.timestamp.hour:02d}:{self.timestamp.minute:02d}:{self.timestamp.second:02d}"


class Timestamp:
    timestamp: pd.Timestamp

    def __init__(self, timestamp):
        if isinstance(timestamp, pd.Timestamp):
            self.timestamp = timestamp
        elif isinstance(timestamp, str) or isinstance(timestamp, int):
            self.timestamp = pd.Timestamp(timestamp)
        else:
            raise ValueError("Invalid type for Timestamp")

    def __str__(self):
        return f"{self.timestamp.year:04d}.{self.timestamp.month:02d}.{self.timestamp.day:02d} {self.timestamp.hour:02d}:{self.timestamp.minute:02d}:{self.timestamp.second:02d}.{self.timestamp.microsecond//1000:03d}"


class NanoTime:
    timestamp: pd.Timestamp

    def __init__(self, timestamp):
        if isinstance(timestamp, pd.Timestamp):
            self.timestamp = timestamp
        elif isinstance(timestamp, int):
            self.timestamp = pd.Timestamp(timestamp)
        elif isinstance(timestamp, str):
            self.timestamp = pd.Timestamp(timestamp)
            # extract nanoseconds from the string
            # because pd.Timestamp("10:15:24.123456789") => 10:15:24.123456, nanosecond is 0
            # maybe it's a bug of pandas
            times = timestamp.split(".")
            if len(times) == 2 and len(times[1]) > 6:
                microsecond = int(times[1][:6].ljust(6, '0'))
                nanosecond = int(f"{times[1][6:].ljust(3, '0')}")
                self.timestamp = self.timestamp.replace(microsecond=microsecond, nanosecond=nanosecond)
        else:
            raise ValueError("Invalid type for NanoTime")

    def __str__(self):
        return f"{self.timestamp.hour:02d}:{self.timestamp.minute:02d}:{self.timestamp.second:02d}.{self.timestamp.microsecond:06d}{self.timestamp.nanosecond:03d}"


class NanoTimestamp:
    timestamp: pd.Timestamp

    def __init__(self, timestamp):
        if isinstance(timestamp, pd.Timestamp):
            self.timestamp = timestamp
        elif isinstance(timestamp, str) or isinstance(timestamp, int):
            self.timestamp = pd.Timestamp(timestamp)
        else:
            raise ValueError("Invalid type for NanoTimestamp")

    def __str__(self):
        return f"{self.timestamp.year:04d}.{self.timestamp.month:02d}.{self.timestamp.day:02d} {self.timestamp.hour:02d}:{self.timestamp.minute:02d}:{self.timestamp.second:02d}.{self.timestamp.microsecond:06d}{self.timestamp.nanosecond:03d}"


class DateHour:
    timestamp: pd.Timestamp

    def __init__(self, timestamp):
        if isinstance(timestamp, pd.Timestamp):
            self.timestamp = timestamp
        elif isinstance(timestamp, str) or isinstance(timestamp, int):
            self.timestamp = pd.Timestamp(timestamp)
        else:
            raise ValueError("Invalid type for DateHour")

    def __str__(self):
        return f"{self.timestamp.year:04d}.{self.timestamp.month:02d}.{self.timestamp.day:02d} {self.timestamp.hour:02d}"


class Int128:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"{self.value}"

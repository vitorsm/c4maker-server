from datetime import datetime

ISO_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def str_iso_to_date(str_date: str) -> datetime:
    return datetime.strptime(str_date, ISO_DATETIME_FORMAT)

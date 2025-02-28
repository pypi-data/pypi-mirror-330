from functools import partial
import datetime
import sys
from zoneinfo import ZoneInfo

if sys.version_info >= (3, 12):
    utcnow = partial(datetime.datetime.now, tz=datetime.UTC)
else:
    utcnow = partial(datetime.datetime.now, tz=ZoneInfo("UTC"))

if sys.version_info >= (3, 12):
    utcfromtimestamp = partial(datetime.datetime.fromtimestamp, tz=datetime.UTC)
else:
    utcfromtimestamp = partial(datetime.datetime.fromtimestamp, tz=ZoneInfo("UTC"))
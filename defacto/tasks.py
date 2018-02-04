from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime, timedelta
from stockapi.models import BuySell, OHLCV, Ticker
from defacto.models import SupplyDemand
import pandas as pd
import math

from defacto.concurrent_tasks.supplydemand import (
    calc_buysell_1,
    calc_buysell_2,
    calc_buysell_3,
    calc_buysell_4,
    calc_buysell_5,
)

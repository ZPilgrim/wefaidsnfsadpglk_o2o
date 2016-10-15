import datetime
USER_ID = 0
MERCHANT_ID = 1
COUPON_ID = 2
DISCOUNT_RATE = 3
DISTANCE = 4
DATE_RECEIVED = 5
DATE = 6
LABEL = 7

def _to_datetime(s):
    date = datetime.datetime.strptime(s, "%Y%m%d")
    return date

def date_diff(a,b):
    diff = _to_datetime(b)-_to_datetime(a)
    return diff.days
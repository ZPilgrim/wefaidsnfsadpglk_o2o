import pandas as pd
from common import *
from data import offline_data_train,offline_data_test
import datetime

def _to_datetime(s):
    date = datetime.datetime.strptime(s, "%Y%m%d")
    return date

def get_raw_train_sample():
    samples = []
    for record in offline_data_train.values:
        sample = {}
        if record[-1] != 'null' and record[2] == 'null':
            continue

        if record[-1] != 'null' and record[2] != 'null' and (_to_datetime(record[-1])-_to_datetime(record[-2])).days <= 15:
            sample[LABEL] = 1
        else:
            sample[LABEL] = 0
        sample[USER_ID] = record[0]
        sample[MERCHANT_ID] = record[1]
        sample[COUPON_ID] = record[2]
        sample[DISCOUNT_RATE] = record[3]
        sample[DISTANCE] = record[4]
        sample[DATE_RECEIVED] = record[5]
        sample[DATE] = record[6]
        samples.append(sample)
    return samples

def get_predict_sample():
    samples = []
    for record in offline_data_test.values:
        sample = {}
        sample[USER_ID] = record[0]
        sample[MERCHANT_ID] = record[1]
        sample[COUPON_ID] = record[2]
        sample[DISCOUNT_RATE] = record[3]
        sample[DISTANCE] = record[4]
        sample[DATE_RECEIVED] = record[5]
        samples.append(sample)
    return samples
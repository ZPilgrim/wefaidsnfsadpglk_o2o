# -*- coding: utf-8 -*-
import pandas as pd
from common import *

def _get_discount_rate_preference(data):
    table = data[['User_id','Discount_rate','Date']].groupby(['User_id','Discount_rate']).count().reset_index()
    ret = {}
    for value in table.values:
        if value[0] not in ret:
            ret[value[0]] = {}
        ret[value[0]][value[1]] = value[2]
    return ret

def _get_Merchant_id_preference(data):
    table = data[['User_id', 'Merchant_id', 'Date']].groupby(['User_id', 'Merchant_id']).count().reset_index()
    ret = {}
    for value in table.values:
        if value[0] not in ret:
            ret[value[0]] = {}
        ret[value[0]][value[1]] = value[2]
    return ret

def _get_Distance_id_preference(data):
    table = data[['User_id','Distance','Date']].groupby(['User_id','Distance']).count().reset_index()
    ret = {}
    for value in table.values:
        if value[0] not in ret:
            ret[value[0]] = {}
        ret[value[0]][value[1]] = value[2]
    return ret

def _get_lingquan_nouse(data):
    lingquan_nouse_data = data[(data.Coupon_id != "null") & (data.Date == 'null')]
    lingquan_data = data[(data.Coupon_id != "null")]
    table = lingquan_nouse_data[['User_id','Coupon_id']].groupby(['User_id']).count().reset_index()
    table2 = lingquan_data[['User_id','Coupon_id']].groupby(['User_id']).count().reset_index()
    tb_temp = pd.merge(table, table2, on='User_id')
    ret = {}
    for value in tb_temp.values:
        ret[value[0]] = float(value[1])/value[2]
    return ret

def _get_coupon_in_sum(data):
    coupon_buy_data = data[(data.Coupon_id != "null") & (data.Date != 'null')]
    buy_data = data[(data.Date != "null")]
    table = coupon_buy_data[['User_id', 'Coupon_id']].groupby(['User_id']).count().reset_index()
    table2 = buy_data[['User_id', 'Coupon_id']].groupby(['User_id']).count().reset_index()
    tb_temp = pd.merge(table, table2, on='User_id')
    ret = {}
    for value in tb_temp.values:
        ret[value[0]] = float(value[1]) / value[2]
    return ret

def _to_datetime(s):
    date = datetime.datetime.strptime(s, "%Y%m%d")
    return date

def _get_time_chazhi(data):
    coupon_buy_data = data[(data.Coupon_id != "null") & (data.Date != 'null')]
    table = coupon_buy_data[['User_id','Date_received','Date']].groupby(['User_id','Date_received','Date']).count().reset_index()
    ret = {}
    for value in table.values:
        value[1] = (_to_datetime(value[2])-_to_datetime(value[1])).days
        if(value[0] not in ret):
            ret[value[0]] = [0,0]
        ret[value[0]][1] += 1
        ret[value[0]][0] += float(ret[value[0]][0]*(ret[value[0]][1]-1) + value[1])/ret[value[0]][1]
    return ret


def head(data,n):
    for k,v in data.items():
        print k,v
        n -= 1
        if n <= 0:
            break

def getUserFeature(data):
    #利用data求用户特征
    user_ids = [i for i in data[['User_id']].groupby('User_id').count().index]
    data_positive = data[(data.Coupon_id != "null") & (data.Date != 'null')]
    data_positive = pd.DataFrame([i for i in data_positive.values if date_diff(i[DATE_RECEIVED], i[DATE]) <= 15])
    data_positive.columns = data.columns
    dis_rate_pre = _get_discount_rate_preference(data)
    dis_rate_pre2 = _get_discount_rate_preference(data_positive)
    merchant_pre = _get_Merchant_id_preference(data)
    merchant_pre2 = _get_Merchant_id_preference(data_positive)
    distance_pre = _get_Distance_id_preference(data)
    receive_nouse = _get_lingquan_nouse(data)
    coupon_inbuy = _get_coupon_in_sum(data)
    time_sub = _get_time_chazhi(data)
    ret = {}
    for user_id in user_ids:
        record = {}
        record['dis_rate_pre'] = dis_rate_pre.get(user_id,{})
        record['dis_rate_pre2'] = dis_rate_pre2.get(user_id,{})
        record['merchant_pre'] = merchant_pre.get(user_id,{})
        record['merchant_pre2'] = merchant_pre2.get(user_id,{})
        record['distance_pre'] = distance_pre.get(user_id,{})
        record['receive_nouse'] = receive_nouse.get(user_id,0)
        record['coupon_inbuy'] = coupon_inbuy.get(user_id, 0)
        temp = time_sub.get(user_id, [100,100])
        record['time_sub'] = temp[0]
        ret[user_id] = record
    return ret

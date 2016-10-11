import pandas as pd
from data import offline_data_train as data,offline_data_positive as data_positive

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



def head(data,n):
    for k,v in data.items():
        print k,v
        n -= 1
        if n <= 0:
            break




def getUserFeature():
    user_ids = [i for i in data[['User_id']].groupby('User_id').count().index]
    dis_rate_pre = _get_discount_rate_preference(data)
    dis_rate_pre2 = _get_discount_rate_preference(data_positive)
    merchant_pre = _get_Merchant_id_preference(data)
    merchant_pre2 = _get_Merchant_id_preference(data_positive)
    distance_pre = _get_Distance_id_preference(data)
    distance_pre2 = _get_Distance_id_preference(data)
    ret = {}
    for user_id in user_ids:
        record = {}
        record['dis_rate_pre'] = dis_rate_pre.get(user_id,{})
        record['dis_rate_pre2'] = dis_rate_pre2.get(user_id,{})
        record['merchant_pre'] = merchant_pre.get(user_id,{})
        record['merchant_pre2'] = merchant_pre2.get(user_id,{})
        record['distance_pre'] = distance_pre.get(user_id,{})
        record['dis_rate_pre2'] = distance_pre2.get(user_id,{})
        ret[user_id] = record
    return ret

#ret = getUserFeature()

#head(ret,5)
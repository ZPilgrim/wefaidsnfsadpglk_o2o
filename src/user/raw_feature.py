# -*- coding: utf-8 -*-
import user_feature
from common import *
from sample import get_raw_train_sample

def getSampleFeature(samples,data):
    #利用data求特征来为samples构造样本特征
    u_fea = user_feature.getUserFeature(data)
    X,Y = [],[]
    for sample in samples:
        features = []
        user_id = sample.get(USER_ID)
        merchant_id = sample.get(MERCHANT_ID)
        dis_rate = sample.get(DISCOUNT_RATE)
        distance = sample.get(DISTANCE)
        this_user_fea = u_fea.get(user_id,{})
        # features.append(this_user_fea.get('receive_nouse',0))
        # features.append(this_user_fea.get('coupon_inbuy', 0))
        # features.append(this_user_fea.get('time_sub', 0))
        # features.append(this_user_fea.get('dis_rate_pre',{}).get(dis_rate,0))
        # features.append(this_user_fea.get('dis_rate_pre2',{}).get(dis_rate,0))
        features.append(this_user_fea.get('merchant_pre',{}).get(merchant_id,0))
        features.append(this_user_fea.get('merchant_pre2',{}).get(merchant_id,0))
        # features.append(this_user_fea.get('distance_pre',{}).get(distance,0))
        # distance_pre = this_user_fea.get('distance_pre', {})
        # for i in range(11):
        #     if(str(i) in distance_pre):
        #         features.append(distance_pre[str(i)])
        #     else:
        #         features.append(0)
        # if ('null' in distance_pre):
        #     features.append(distance_pre['null'])
        # else:
        #     features.append(0)
        X.append(features)
        Y.append(sample.get(LABEL))
    return X,Y
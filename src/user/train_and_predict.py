import sample
import raw_feature
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from common import *
from sklearn.ensemble import GradientBoostingClassifier
from data import _6_data,_5_data,_4_data,_3_data,_2_data,_1_data

samples = sample.get_raw_train_sample()
train_samples = [i for i in samples if i.get(DATE_RECEIVED) < '20160701' and i.get(DATE_RECEIVED) >= '20160601']
X1,Y1 = raw_feature.getSampleFeature(train_samples,_5_data)
train_samples = [i for i in samples if i.get(DATE_RECEIVED) < '20160601' and i.get(DATE_RECEIVED) >= '20160501']
temp_X1,temp_Y1 = raw_feature.getSampleFeature(train_samples,_4_data)
X1 += temp_X1
Y1 += temp_Y1
train_samples = [i for i in samples if i.get(DATE_RECEIVED) < '20160501' and i.get(DATE_RECEIVED) >= '20160401']
temp_X1,temp_Y1 = raw_feature.getSampleFeature(train_samples,_3_data)
X1 += temp_X1
Y1 += temp_Y1
train_samples = [i for i in samples if i.get(DATE_RECEIVED) < '20160401' and i.get(DATE_RECEIVED) >= '20160301']
temp_X1,temp_Y1 = raw_feature.getSampleFeature(train_samples,_2_data)
X1 += temp_X1
Y1 += temp_Y1
train_samples = [i for i in samples if i.get(DATE_RECEIVED) < '20160301' and i.get(DATE_RECEIVED) >= '20160201']
temp_X1,temp_Y1 = raw_feature.getSampleFeature(train_samples,_1_data)
X1 += temp_X1
Y1 += temp_Y1

predict_samples = sample.get_predict_sample()
X2,Y2 = raw_feature.getSampleFeature(predict_samples,_6_data)


def test_clf():
    clf = RandomForestClassifier(n_estimators=10)
    clf = clf.fit(X1,Y1)
    pre = clf.predict_proba(X2)
    results = []
    for i in range(len(predict_samples)):
        t = predict_samples[i]
        results.append([t.get(USER_ID),t.get(COUPON_ID),t.get(DATE_RECEIVED),pre[i][1]])
    df = pd.DataFrame(results)
    df.to_csv('../../ccf_data/predic_distance.csv',index=False)


def test_gbdt():
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.05, max_depth=6, random_state=0).fit(X1, Y1)
    clf = clf.fit(X1,Y1)
    pre = clf.predict_proba(X2)
    results = []
    for i in range(len(predict_samples)):
        t = predict_samples[i]
        results.append([t.get(USER_ID),t.get(COUPON_ID),t.get(DATE_RECEIVED),pre[i][1]])
    df = pd.DataFrame(results)
    df.to_csv('../../ccf_data/predic_gbdt_diedai.csv',index=False)


test_gbdt()
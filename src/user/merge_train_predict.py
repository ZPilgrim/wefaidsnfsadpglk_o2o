import sample
import raw_feature
from data import coupon_feature_6,coupon_feature_7,merchant_feature_6,merchant_feature_7
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from common import *
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from data import _6_data,_5_data,_4_data,_3_data,_2_data,_1_data

train_samples = sample.get_raw_train_sample()

X1,Y1 = raw_feature.getSampleFeature(train_samples)

predict_samples = sample.get_predict_sample()
X2,Y2 = raw_feature.getSampleFeature(predict_samples)

def data_merge():
    count = 0
    # flag = 0
    while count < len(X1):
        for i in coupon_feature_6.values[count]:
            X1[count].append(i)
        for i in merchant_feature_6.values[count]:
            X1[count].append(i)
        count += 1
    # while count < len(X1):
    #     if (Y1[count] == 1):
    #         train_X1.append(X1[count])
    #         for i in coupon_feature_6.values[count]:
    #             train_X1[-1].append(i)
    #         for i in merchant_feature_6.values[count]:
    #             train_X1[-1].append(i)
    #         train_Y1.append(Y1[count])
    #         count += 1
    #     elif flag == 4:
    #         train_X1.append(X1[count])
    #         for i in coupon_feature_6.values[count]:
    #             train_X1[-1].append(i)
    #         for i in merchant_feature_6.values[count]:
    #             train_X1[-1].append(i)
    #         train_Y1.append(Y1[count])
    #         count += 1
    #         flag = 0
    #     else:
    #         flag = flag + 1
    #         count += 1

    count = 0
    while count < len(X2):
        for i in coupon_feature_7.values[count]:
            X2[count].append(i)
        for i in merchant_feature_7.values[count]:
            X2[count].append(i)
        count += 1

def test_lr():
    lr = LogisticRegression(C=1000.0, penalty='l1')
    lr = lr.fit(X1,Y1)
    pre = lr.predict_proba(X2)
    results = []
    for i in range(len(predict_samples)):
        t = predict_samples[i]
        results.append([t.get(USER_ID), t.get(COUPON_ID), t.get(DATE_RECEIVED), pre[i][1]])
    df = pd.DataFrame(results)
    df.to_csv('../../ccf_data/predic_5.csv', index=False)


def test_clf():
    clf = RandomForestClassifier(n_estimators=10)
    clf = clf.fit(X1,Y1)
    pre = clf.predict_proba(X2)
    results = []
    for i in range(len(predict_samples)):
        t = predict_samples[i]
        results.append([t.get(USER_ID),t.get(COUPON_ID),t.get(DATE_RECEIVED),pre[i][1]])
    df = pd.DataFrame(results)
    df.to_csv('../../ccf_data/predic_3.csv',index=False)

def test_gbdt():
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.05,max_depth = 6, random_state = 0).fit(X1, Y1)
    pre = clf.predict_proba(X2)
    results = []
    for i in range(len(predict_samples)):
        t = predict_samples[i]
        results.append([t.get(USER_ID), t.get(COUPON_ID), t.get(DATE_RECEIVED), pre[i][1]])
    df = pd.DataFrame(results)
    df.to_csv('../../ccf_data/predic_4.csv', index=False)

data_merge()
# test_clf()
# test_gbdt()
test_lr()
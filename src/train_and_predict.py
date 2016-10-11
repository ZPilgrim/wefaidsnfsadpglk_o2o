import sample
import raw_feature
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from common import *

train_samples = sample.get_raw_train_sample()
predict_samples = sample.get_predict_sample()
X1,Y1 = raw_feature.getSampleFeature(train_samples)
X2,Y2 = raw_feature.getSampleFeature(predict_samples)


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

test_clf()
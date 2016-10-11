
import sample
import raw_feature
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from common import *


samples = sample.get_raw_train_sample()
train_samples = [i for i in samples if i.get(DATE_RECEIVED) < '20160501']
#test_samples = [i for i in samples if i.get(DATE_RECEIVED) >= '20160601']
test_samples = []
test_samples_positive = []
test_samples_negative = []
for i in samples:
    if i.get(DATE_RECEIVED)>='20160501' and i.get(LABEL)==0:
        test_samples_negative.append(i)
    if i.get(DATE_RECEIVED) >= '20160501' and i.get(LABEL) == 1:
        test_samples_positive.append(i)
length = len(test_samples_positive)
test_samples = test_samples_positive + test_samples_negative[0:length]
X1,Y1 = raw_feature.getSampleFeature(train_samples)
X2,Y2 = raw_feature.getSampleFeature(test_samples)
# print test_samples,X2


def test_rf():
    rf = RandomForestClassifier(n_estimators=10)
    rf = rf.fit(X1,Y1)
    pre = rf.predict_proba(X2)
    pre = [i[1] for i in pre]
    print auc(Y2,pre)
    # fpr, tpr, thresholds = metrics.roc_curve(Y2, pre, pos_label=1)
    # print metrics.auc(fpr, tpr)
    # for i in range(10000):
    #     print (Y2[i],pre[i]),(Y2[-i],pre[-i])

def test_lr():
    lr = LogisticRegression(C=1000.0, penalty='l1')
    lr = lr.fit(X1,Y1)
    pre = lr.predict_proba(X2)
    pre = [i[1] for i in pre]
    fpr, tpr, thresholds = metrics.roc_curve(Y2, pre, pos_label=1)
    print metrics.auc(fpr, tpr)

def auc(Y,pre):
    res_dic = []
    count_negative = 0
    count_positive = 0
    for i in range(len(Y)):
        res_dic.append(([Y[i],pre[i]]))
        if(Y[i]==0):
            count_negative += 1
        else:
            count_positive += 1
    dict = sorted(res_dic, key=lambda d: d[1], reverse=True)
    auc_sum = 0.0
    jianshu = count_positive*(count_positive+1)/2
    chushu = count_positive*count_negative
    if(chushu==0):
        return 0.5
    sample_point_count = len(Y)
    for i in range(sample_point_count):
        if(Y[i]==1):
            auc_point = ((sample_point_count-i)-jianshu)/float(chushu)
            auc_sum += auc_point
    return auc_sum/sample_point_count

test_rf()
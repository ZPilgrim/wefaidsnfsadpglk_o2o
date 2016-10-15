import pandas as pd
from common import *
offline_data_train = pd.read_csv('../../ccf_data/ccf_offline_stage1_train.csv')
offline_data_test = pd.read_csv('../../ccf_data/ccf_offline_stage1_test_revised.csv')

def get_data(s1,s2):
    return offline_data_train[((offline_data_train.Date_received<s1)|(offline_data_train.Date<s1))& ((offline_data_train.Date_received>=s2)|(offline_data_train.Date>=s2))]

_1_data = get_data("20160201","20160101")
_2_data = get_data("20160301","20160201")
_3_data = get_data("20160401","20160301")
_4_data = get_data("20160501","20160401")
_5_data = get_data("20160601","20160501")
_6_data = get_data("20160701","20160601")
_12345_data = get_data("20160601","20160101")

coupon_feature_5 = pd.read_csv('../../ccf_data/coupon_feature5_zwm.csv')
coupon_feature_6 = pd.read_csv('../../ccf_data/coupon_feature6_zwm.csv')
coupon_feature_7 = pd.read_csv('../../ccf_data/coupon_feature7_zwm.csv')
coupon_feature_6form5 = pd.read_csv('../../ccf_data/coupon_feature_6from5_zwm.csv')


merchant_feature_6 = pd.read_csv('../../ccf_data/merchant_feature6_nyh.csv')
merchant_feature_7 = pd.read_csv('../../ccf_data/merchant_feature7_nyh.csv')
merchant_feature_5 = pd.read_csv('../../ccf_data/merchant_feature5_nyh.csv')
merchant_feature_6from5 = pd.read_csv('../../ccf_data/merchant_feature6from5_nyh.csv')
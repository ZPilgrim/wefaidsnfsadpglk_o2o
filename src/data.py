import pandas as pd

prefix = "/Users/zhangweimin/Documents/MyDocs/Contest/Ant/ccf_data/final/"

offline_data_train = pd.read_csv(prefix + 'ccf_offline_stage1_train.csv')
offline_data_positive = offline_data_train[(offline_data_train.Coupon_id != "null") & (offline_data_train.Date != 'null')]
offline_data_test = pd.read_csv(prefix + 'ccf_offline_stage1_test_revised.csv')

coupon_feature_5 = pd.read_csv('../../ccf_data/coupon_feature5_zwm.csv')
coupon_feature_6 = pd.read_csv('../../ccf_data/coupon_feature6_zwm.csv')
coupon_feature_7 = pd.read_csv('../../ccf_data/coupon_feature7_zwm.csv')
coupon_feature_6form5 = pd.read_csv('../../ccf_data/coupon_feature_6from5_zwm.csv')



xgb_train_file = prefix + "xgb_train_file.csv"
xgb_test_file = prefix + "xgb_test_file.csv"


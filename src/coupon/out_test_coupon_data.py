from cal_coupon_feature import *

if __name__ == "__main__" :
    
    cs_records = []
    cs = []
    pos = {} #key:id value:idx in cs
    cs_offline = []
    feature_data = []

    process_offline_date(offline_train_file, cs, cs_records, pos)
    process_online_data(online_train_file, cs, cs_records, pos)

    #process_sample_train_data(offline_train_file, cs, feature_data, pos)
    #process_sample_online_data(online_train_file, cs, feature_data, pos)

    process_test_data(test_file, cs, feature_data)

    log_info("dump features to file")
    csv_write_file(online_and_offline_test_file, feature_data)
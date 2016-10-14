
from src.utils.file_io import *
from src.coupon.coupon import *
from src.coupon.cal_coupon_feature import *
from test.test_parameters import *


# if __name__ == "__main__":
#
#     cs_records = []
#     cs = []
#     pos = {} #key:id value:idx in cs
#
#     offline_file = file(test_offline_file, 'rb')
#
#     init_cs(offline_file, offline_type, cs, cs_records, pos)
#
#     offline_file.close()
#
#     online_file = file(test_online_file, 'rb')
#     init_cs(online_file, online_type, cs, cs_records, pos )
#     online_file.close()
#
#     cs_data = []
#     for c in cs:
#         cs_data.append(c.to_tuple())
#
#     csv_write_file(test_out_file, cs_data)
#
#     cs_offline = []
#     cs_offline = copy.deepcopy(cs)
#     log_info("dump features to file, cs len:" + str(len(cs)))
#     feature_data = []
#     offline_file = file(test_offline_file, 'rb')
#     #cal_out_coupon_features(offline_file, feature_data, cs_offline, pos)
#     cal_out_coupon_features_classifed_by_type(offline_file, cs, feature_data)
#     offline_file.close()
#
#     #log_special_debug(str(feature_data))
#     csv_write_file(test_coupon_feature_out_file, feature_data)



if __name__ == "__main__":

    cs_records = []
    cs = []
    pos = {} #key:id value:idx in cs
    cs_offline = []
    feature_data = []

    process_offline_date(test_offline_file, cs, cs_records, pos)
    process_online_data(test_online_file, cs, cs_records, pos)

    process_train_data(test_offline_file, cs, feature_data, pos)

    #process_test_data(test_file, cs, feature_data)

    log_info("dump features to file")
    csv_write_file(coupon_feature_out_file, feature_data)
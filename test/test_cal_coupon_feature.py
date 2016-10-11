
from src.utils.file_io import *
from src.coupon.coupon import *
from src.coupon.cal_coupon_feature import *
from test.test_parameters import *


if __name__ == "__main__":

    cs_records = []
    cs = []
    pos = {} #key:id value:idx in cs

    offline_file = file(test_offline_file, 'rb')

    init_cs(offline_file, offline_type, cs, cs_records, pos)

    offline_file.close()

    online_file = file(test_online_file, 'rb')
    init_cs(online_file, online_type, cs, cs_records, pos )
    online_file.close()

    cs_data = []
    for c in cs:
        cs_data.append(c.to_tuple())

    csv_write_file(test_out_file, cs_data)
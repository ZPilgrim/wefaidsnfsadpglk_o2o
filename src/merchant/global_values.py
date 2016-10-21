# -*- coding: UTF-8 -*-

distance_level = 11
months_first_days = ['20160101', '20160201', '20160301', '20160401', '20160501', '20160601', '20160701']

# 商户特征默认取值
dist_user_portion_default = [0.0] * distance_level  # 距离为i档的用户的个数/该店总的用户的个数
dist_consume_portion_default = [0.0] * distance_level  # 距离为i档的消费记录的个数/该店总的消费记录的个数
# 上面两个特征只使用线下数据计算，但未分母去掉距离为null的记录，是否合适？
used_coupon_portion_default = 0.0  # 使用的优惠券的数量（额度）/所有商店使用的优惠券的数量(额度)
pi_avg_default = 0.0  # Pi=第I个月消费件数/第I月所有店消费记录个数
pi_var_default = 0.0
latest_pi_default = 0.0
gradient_avg_default = 0.0  # 梯度平均值，即近2个月销售额差值平均值
visit_frequency_without_coupon_default = 0.0  # 被访问次数/总的记录
default_values = dist_user_portion_default + dist_consume_portion_default + \
               [used_coupon_portion_default, pi_avg_default, pi_var_default, latest_pi_default,
                gradient_avg_default, visit_frequency_without_coupon_default]

# 数组下标含义定义
USER_ID = 0
MERCHANT_ID = 1
COUPON_ID = 2
DISCOUNT_RATE = 3
DISTANCE = 4
DATE_RECEIVED = 5
DATE = 6

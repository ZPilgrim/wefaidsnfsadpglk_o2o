# -*- coding: UTF-8 -*-


def compute_month_sales(data1, data2, total_months):
    month_sales = [0] * total_months
    for record in data1:
        if record[7] != "":
            if record[7] >= '20160101' and record[7] < '20160201':
                month_sales[0] += 1
            elif record[7] >= '20160201' and record[7] < '201603201':
                month_sales[1] += 1
            elif record[7] >= '20160301' and record[7] < '20160401':
                month_sales[2] += 1
            elif record[7] >= '20160401' and record[7] < '20160501':
                month_sales[3] += 1
            elif record[7] >= '20160501' and record[7] < '20160601':
                month_sales[4] += 1
            elif total_months == 6 and record[7] >= '20160601' and record[7] < '20160701':
                month_sales[total_months - 1] += 1
    for record in data2:
        if record[7] != "":
            if record[7] >= '20160101' and record[7] < '20160201':
                month_sales[0] += 1
            elif record[7] >= '20160201' and record[7] < '201603201':
                month_sales[1] += 1
            elif record[7] >= '20160301' and record[7] < '20160401':
                month_sales[2] += 1
            elif record[7] >= '20160401' and record[7] < '20160501':
                month_sales[3] += 1
            elif record[7] >= '20160501' and record[7] < '20160601':
                month_sales[4] += 1
            elif total_months == 6 and record[7] >= '20160601' and record[7] < '20160701':
                month_sales[total_months - 1] += 1
    return month_sales
# 可优化，用列表匹配，循环

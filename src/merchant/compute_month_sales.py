# -*- coding: UTF-8 -*-

from global_values import months_first_days, DATE


def compute_month_sales(data, start_month, end_month):
    month_sales = [0] * (end_month - start_month + 1)
    for record in data:
        if record[DATE] != "":
            for i in range(start_month - 1, end_month):
                if months_first_days[i] <= record[DATE] < months_first_days[i+1]:
                    month_sales[i - start_month + 1] += 1
    return month_sales

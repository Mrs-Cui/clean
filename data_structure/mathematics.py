#! /usr/bin/env python
# -*- coding:utf-8 -*-

import array
"""
    大数相乘
"""

def larger_number_multiply(first_num, second_num):
    array_list = array()



"""
    最大差值:
        有一个长为n的数组A，求满足0≤a≤b<n的A[b]-A[a]的最大值。
        给定数组A及它的大小n，请返回最大差值
        [10, 5], 2 return 0+
    思路:
        
"""

def max_value(array, n):
    min_value = array[0]
    max_value = 0
    for pos, atr in enumerate(array):
        if pos == 0:
            continue
        if atr < min_value:
            min_value = atr

        if atr - min_value > max_value:
            max_value = atr - min_value
    return max_value


"""
    给定两个数A、B（0，100000），求 A^B 中最后三位数是多少
"""
def mantissa(a, b):

    if b == 0:
        return 1
    if a <= 1 or b == 1:
        return a % 1000
    if b == 2:
        return a * a % 1000
    if b % 2 == 1:
        return mantissa(mantissa(a, b//2), 2) * a % 1000
    else:
        return mantissa(mantissa(a, b//2) % 1000, 2) % 1000


"""
给定一个整数数组 A，找到 min(B) 的总和，其中 B 的范围为 A 的每个（连续）子数组。

由于答案可能很大，因此返回答案模 10^9 + 7。

输入：[3,1,2,4]
输出：17
解释：
子数组为 [3]，[1]，[2]，[4]，[3,1]，[1,2]，[2,4]，[3,1,2]，[1,2,4]，[3,1,2,4]。 
最小值为 3，1，2，4，1，1，2，1，1，1，和为 17。

"""


def min_child_array(array):
    length = len(array)
    count = 0
    for i in range(length):
        count += array[i]
        min_value = array[i]
        for j in range(i+1, length):
            min_value = min(min_value, array[j])
            count += min_value
    return count

"""
编写一个 StockSpanner 类，它收集某些股票的每日报价，并返回该股票当日价格的跨度。
今天股票价格的跨度被定义为股票价格小于或等于今天价格的最大连续日数（从今天开始往回数，包括今天）。
例如，如果未来7天股票的价格是 [100, 80, 60, 70, 60, 75, 85]，那么股票跨度将是 [1, 1, 1, 2, 1, 4, 6]。

调用 StockSpanner.next(int price) 时，将有 1 <= price <= 10^5。
每个测试用例最多可以调用 10000 次 StockSpanner.next。
在所有测试用例中，最多调用 150000 次 StockSpanner.next。
此问题的总时间限制减少了 50%。
"""




def max_stock_span(array):

    length = len(array)










if __name__ == '__main__':
    print(min_child_array([3,1,2,4]))

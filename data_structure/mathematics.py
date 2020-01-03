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



if __name__ == '__main__':
    print(mantissa(11, 5))

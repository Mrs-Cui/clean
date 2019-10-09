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



if __name__ == '__main__':
    pass

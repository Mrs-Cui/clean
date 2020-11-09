#! /usr/bin/env python
# -*- coding:utf-8 -*-

import random

#  动态规划练习


def max_path():
    pass


"""
寺庙的柱子是由木头制成。每根柱子必须是一jie完整的木头而且不能是被连接得到的。
给出n段具有不同长度的木头。你的寺庙有m根高度严格相同的柱子。那么你寺庙最大高度是多少。(m根柱子的高度)
1<=n<=100000
1<=m<=100000
输入：m = 3, [2, 3, 4]
输出：2 
输入：m = 3, [2, 10]
输出：3
"""

def query_sort(array, start, end):
    if start > end:
        return
    tag = array[start]
    init_start, init_end = start, end
    while start < end:
        while start < end and array[end] >= tag:
            end -= 1
        array[start] = array[end]
        while start < end and array[start] < tag:
            start += 1
    array[end] = tag
    query_sort(array, init_start, start-1)
    query_sort(array, start + 1, init_end)

def count_max_height(m, trees):
    length = len(trees)
    query_sort(trees, 0, length-1)
    print(trees)
    if length - m >= 0:
        start, end = length - m, length - 1
    else:
        start, end = 0, length - 1
    position = list(range(start, end))
    position.reverse()
    max_height = 0
    for cut_num in range(1, m+1):
        count = 0
        height = trees[end] // cut_num
        if height < 1:
            break
        count += cut_num
        for pos in position:
            if trees[pos] // height >= 1:
                count += trees[pos] // height
                if count >= m:
                    max_height = height if height >= max_height else max_height
                    break
    return max_height


"""
在一个由 0 和 1 组成的二维矩阵内，找到只包含 1 的最大正方形，并返回其面积。
"""


def max_square_size(array):
    row = len(array)
    col = len(array[0])
    sizes = [[0] * col] * row
    for i in range(col):
        sizes[0][i] = array[0][i]
    for i in range(row):
        sizes[i][0] = array[i][0]
    max_length = 0
    for i, items in enumerate(array):
        if i == 0:
            continue
        for j, item in enumerate(items):
            if j == 0:
                continue
            if array[i][j] == 0:
                sizes[i][j] = 0
            else:
                sizes[i][j] = min(sizes[i-1][j-1], sizes[i-1][j], sizes[i][j-1]) + 1
        max_length = max(sizes[i][j], max_length)
    print(max_length * max_length)

"""
给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。
如果你最多只允许完成一笔交易（即买入和卖出一支股票），设计一个算法来计算你所能获取的最大利润。
"""

def max_profit(array):
    length = len(array)
    buy = -array[0]
    sell = 0
    for pos in range(1, length):
        buy = max(buy, -array[pos])
        sell = max(sell, array[pos] + buy)
    print(sell)

"""
给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。
设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。
注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。
"""

def max_profit_two(array):
    length = len(array)
    if length <= 1:
        return 0
    buy = -array[0]
    sell = 0
    for pos in range(1, length):
        sell = max(sell, array[pos] + buy)
        buy = max(buy, sell - array[pos])
        print(pos, sell, buy)
    print(sell)

"""
给定平面上 n 对不同的点，“回旋镖” 是由点表示的元组 (i, j, k) ，其中 i 和 j 之间的距离和 i 和 k 之间的距离相等（需要考虑元组的顺序）。
找到所有回旋镖的数量。你可以假设 n 最大为 500，所有点的坐标在闭区间 [-10000, 10000] 中。
"""



def boomerang(array):
    pass


def max_number_of_copy(numbers):
    """
        一个数分成几份，可以被 3 整除的最大份数。比如 12345 分成12 3 45 结果为3.
    """
    length = len(numbers)
    left, right = 0, 1
    result = [0, ]
    while right <= length:
        if int(numbers[left: right]) % 3 == 0:
            print(left, right)
            result.append(right)
            left = right
            right += 1
        else:
            right += 1
    else:
        if result[-1] != length:
            result = []
    print(result)



if __name__ == '__main__':
    # trees = [random.randint(1, 10) for i in range(3)]
    # print(count_max_height(4, trees))
    max_number_of_copy('12346')

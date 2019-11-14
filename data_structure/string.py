#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
    与字符串相关的算法
"""

import array

# KMP 算法

def kmp(pattern_array):
    length = len(pattern_array)
    next_array = array.array("h", range(length))
    front, back = -1, 0
    next_array[0] = -1
    while back < length - 1:
        if (front == -1 or pattern_array[front] == pattern_array[back]):
            front += 1
            back += 1
            if pattern_array[back] == pattern_array[back - 1]:
                next_array[back] = next_array[back - 1]
            else:
                next_array[back] = front
        else:
            front = next_array[front]
    return next_array.tolist()


def pattern(string, pattern_str):
    next_array = kmp(pattern_str)
    print(next_array)
    length = len(string)
    pattern_len = len(pattern_str)
    len_index, pattern_index = 0, 0
    while len_index < length and pattern_index < pattern_len:
        if string[len_index] == pattern_str[pattern_index] or pattern_index == -1:
            len_index += 1
            pattern_index += 1
        else:
            pattern_index = next_array[pattern_index]
        print(len_index, pattern_index)
    if pattern_index == pattern_len:
        return len_index - pattern_len
    else:
        return -1

# BM算法

def BM(string, pattern_str):
    length = len(string)
    pattern_len = len(pattern_str)
    len_index = 0
    pattern_index = list(range(pattern_len))
    pattern_index.reverse()

    while len_index < length:

        for pos in pattern_index:
            if pattern_index[pos] != string[len_index + pos]:
                # 坏字符原则
                if pos == pattern_len - 1:
                    temp_len = pattern_len - 1
                    while temp_len > 0:
                        if string[len_index + temp_len] == pattern_str[temp_len]:
                            break
                        else:
                            temp_len -= 1
                    len_index += temp_len
                # 好后缀原则
                else:
                    try:
                        index = pattern_str[:pos].index(pattern_str[pos])
                    except ValueError as e:
                        index = -1
                    if index != -1:
                        len_index += (pos + 1 - index)
                    else:
                        pass
                break

        if pos == 0:
            break


def max_len_subsequence(str_1, str_2):
    """
        最长公共子序列
    :param str_1:
    :param str_2:
    :return:
    """
    row, col = len(str_1), len(str_2)
    dp = []
    for i in range(row + 1):
        dp.append([0 for i in range(col + 1)])
    for i in range(row + 1):
        print(dp[i])
    print('*' * 10)
    for i in range(row):
        for j in range(col):
            if str_1[i] == str_2[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
    for i in range(row + 1):
        print(dp[i])
    return dp[row][col]


def max_len_substr(str_1, str_2):
    """
        最长公共子串
    :param str_1:
    :param str_2:
    :return:
    """
    row, col = len(str_1), len(str_2)
    dp = []
    for i in range(row + 1):
        dp.append([0 for i in range(col + 1)])
    for i in range(row + 1):
        print(dp[i])
    print('*' * 10)
    result = 0
    for i in range(row):
        for j in range(col):
            if str_1[i] == str_2[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = 0
            result = max(result, dp[i+1][j+1])
    for i in range(row + 1):
        print(dp[i])
    return dp[row][col]


def look_for_change(money, aim):
    """
        动态规划找零钱问题
    :param money:
    :param aim:
    :return:
    """
    dp = []
    if len(money) == 0 or aim == 0:
        return 0
    for i in range(len(money) + 1):
        dp.append([0 for i in range(aim + 1)])
    for i in range(len(money) + 1):
        dp[i][0] = 1 if i != 0 else 0

    for i in range(aim + 1):
        for j in range(aim + 1):
            if i != 0 and i == j * money[0]:
                dp[1][i] = 1
    for i in range(len(money) + 1):
        print(dp[i])

    for i in range(2, len(money) + 1):
        for j in range(1, aim+1):
            dp[i][j] = dp[i-1][j]
            if money[i-1] > j:
                continue
            for z in range(1, aim + 1):
                if money[i-1] * z <= j:
                    dp[i][j] += dp[i-1][j-money[i-1] * z]
                else:
                    break

    for i in range(len(money) + 1):
        print(dp[i])

"""
    现在给出一个数字序列，允许使用一种转换操作：
    选择任意两个相邻的数，然后从序列移除这两个数，并用这两个数字的和插入到这两个数之前的位置(只插入一个和)。
    思路:
        从最外层进行头尾比较，如果相等则进入内层，否则就进行操作(将小的放在前面，然后进行相邻数相加)。
"""


def back_to_text(arr):
    start_index, end_index = 0, len(arr) - 1
    count = 0
    while(start_index < end_index):
        if arr[start_index] == arr[end_index]:
            start_index += 1
            end_index -= 1
        else:
            if arr[start_index] > arr[end_index]:
                arr[start_index], arr[end_index] = arr[end_index], arr[start_index]
            arr[start_index] += arr[start_index + 1]
            del arr[start_index + 1]
            end_index -= 1
            count += 1
    return arr, count

"""
一种双核CPU的两个核能够同时的处理任务，现在有n个已知数据量的任务需要交给CPU处理，
假设已知CPU的每个核1秒可以处理1kb，每个核同时只能处理一项任务。
n个任务可以按照任意顺序放入CPU进行处理，现在需要设计一个方案让CPU处理完这批任务所需的时间最少，求这个最小的时间
"""


def max_execute_time(arr):

    sum = 0
    for pos, item in enumerate(arr):
        arr[pos] = item / 1024
        sum += arr[pos]
    half = sum / 2
    best_time = [0, ] * (half + 1)
    value = [i for i in range(half + 1)]
    value.reverse()
    for i in range(len(arr)):
        for j in value:
            if j < arr[i]:
                break
            best_time[j] = max(best_time[j], best_time[j-arr[i]] + arr[i])
    print((sum - best_time[-1]) * 1024)



if __name__ == '__main__':
    max_execute_time([3072, 3072, 7168, 3072, 1024])

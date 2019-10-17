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

if __name__ == '__main__':
    look_for_change([5, 2, 3, 4, 8], 8)

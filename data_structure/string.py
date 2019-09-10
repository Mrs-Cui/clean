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




if __name__ == '__main__':
    pass

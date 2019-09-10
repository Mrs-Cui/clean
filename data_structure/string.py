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
    

if __name__ == '__main__':
    main_string = 'ABCKAAAAABCDABDAKC'
    string = 'AAAAABCDABD'
    print pattern(main_string, string)


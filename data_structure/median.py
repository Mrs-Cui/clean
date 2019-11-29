#! /usr/bin/env python
# -*- coding:utf -*-

import random

# 给一个随机正整数数组，求所有子数组的最小值之和


def min_subset_sum(array):
    count = 0
    stack = []
    for pos, item in enumerate(array):

        if stack and array[stack[-1]] >= item:
            pass
        stack.append(pos)

    return count


if __name__ == '__main__':
    items = [random.randrange(1, 8) for i in range(4)]
    print(items)
    print(min_subset_sum(items))

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

"""
    如何对一个有序数组原地删除重复元素, 空间复杂度O(1), 时间复杂度O(n)
    方法: 采用快慢指针的方法.
"""

def delete_repeat_value(array):
    slow = 0
    fast = 1
    while fast < len(array):
        if array[slow] != array[fast]:
            slow += 1
            array[slow] = array[fast]
        fast += 1
        print(slow, fast)
    print(array)

"""
给定一个包含 n + 1 个整数的数组 nums，其数字都在 1 到 n 之间（包括 1 和 n），可知至少存在一个重复的整数。假设只有一个重复的整数，找出这个重复的数。
输入: [3,1,3,4,2]
输出: 3
不能更改原数组（假设数组是只读的）。
只能使用额外的 O(1) 的空间。
时间复杂度小于 O(n^2) 。
数组中只有一个重复的数字，但它可能不止重复出现一次。
解决方法:  按值二分法
"""

def find_repeat_value(array):
    start, end = 0, len(array) - 1
    while start < end:
        mid = (end - start) / 2 + start
        count = 0
        for item in array:
            if item <= mid:
                count += 1
        if count > mid:
            end = mid
        else:
            start = mid + 1

"""
快慢指针的解法:
public int findDuplicate(int[] nums) {        
    int fast = nums[nums[0]];
    int slow = nums[0];

    while (fast != slow) {
        fast = nums[nums[fast]];
        slow = nums[slow];
    }

    slow = 0;
    while (fast != slow) {
        fast = nums[fast];
        slow = nums[slow];
    }

    return slow;
}
"""

"""
给定一个未排序的整数数组，找出其中没有出现的最小的正整数。
输入: [7,8,9,11,12]
输出: 1
你的算法的时间复杂度应为O(n)，并且只能使用常数级别的空间。

"""


def find_min_num(array):
    length = len(array)
    if not array or length <= 0:
        return
    pos = 0
    while pos < length:
        if array[pos] < 0 or array[pos] > length or array[pos] == array[array[pos]-1]:
            pos += 1
            continue
        temp = array[array[pos]-1]
        array[array[pos]-1] = array[pos]
        array[pos] = temp
    for i in range(length):
        if array[i] != i+1:
            return i + 1
    return length + 1

"""
单调栈:  在普通的栈基础上多了一个特性, 栈内元素是有序的.
"""
if __name__ == '__main__':
    items = [random.randrange(1, 8) for i in range(4)]
    print(items)
    # print(min_subset_sum(items))
    # delete_repeat_value([1, 2, 2, 2, 3, 3, 4])
    print(find_min_num([12, 2, 4, 1, 3, 11, 8, 9]))

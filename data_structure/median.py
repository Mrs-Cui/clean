#! /usr/bin/env python
# -*- coding:utf-8 -*-

import random
import sys
# 给一个随机正整数数组，求所有子数组的最小值之和
reload(sys)
sys.setdefaultencoding('utf-8')
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

class Solution(object):
    def wordBreak(self, s, wordDict):
        """
        :type s: str
        :type wordDict: List[str]
        :rtype: bool
        """
        self.dict_tree = {}
        for word in wordDict:
            self.index = 0
            self.length = len(word)
            self.create_tree(word, self.dict_tree)
        self.index = 0
        init_index = []
        init_dict = self.dict_tree
        while self.index < len(s):
            if init_dict.get(s[self.index]):
                if self.index + 1 == len(s) and not init_dict[s[self.index]].flag:
                    if init_index:
                        self.index = init_index.pop() + 1
                        init_dict = self.dict_tree
                        continue

                if init_dict[s[self.index]].flag:
                    init_index.append(self.index)
                init_dict = init_dict[s[self.index]].data
                self.index += 1
            else:
                if init_index:
                    self.index = init_index.pop() + 1
                else:
                    return False
                init_dict = self.dict_tree
            print(self.index, init_index, init_dict)

        return True

    def create_tree(self, word, dict_tree):
        if self.index >= self.length:
            return dict()
        if dict_tree.get(word[self.index]):
            if self.index + 1 == self.length:
                dict_tree[word[self.index]].flag = True
            self.index += 1
            self.create_tree(word, dict_tree[word[self.index - 1]].data)
        else:
            if self.index + 1 == self.length:
                flag = True
            else:
                flag = False
            tree = Tree(flag)
            dict_tree[word[self.index]] = tree
            self.index += 1
            self.create_tree(word, dict_tree[word[self.index - 1]].data)


class Tree(object):
    def __init__(self, flag=False):
        self.data = {}
        self.flag = flag


class Solutions(object):
    def checkSubarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """
        if not nums or len(nums) == 1:
            return False
        length = len(nums)
        num = 0
        hash_map = {0: -1}
        for i in range(length):
            num += nums[i]
            if k != 0:
                num = num % k
            print('a',hash_map, i, nums[i], num)

            if hash_map.has_key(num):
                if i - hash_map[num] > 1:
                    return True
            else:
                hash_map[num] = i
            print(hash_map, i, nums[i], num)

        return False

import csv
import re
class HandleCsv(object):

    def __init__(self):
        self.data = []
        self.new_data = []
    def read(self):
        with open('/home/cui/文档/handle.txt', 'r') as f:
            reader = csv.reader(f,)
            for row in reader:
                self.data.append(row)

    def handle(self):
        self.data.pop(0)

        try:
            for data in self.data:
                print(data[0].encode('ISO-8859'))
                if not data:
                    continue
                pattern = re.search('(.*(?:,|\S*))([0-9-]*)(.*(?:,|\S*))', data[0])
                # if pattern:
                #     print(pattern.group(1))
        except Exception as e:
            print(data[0])
            raise e


class Solutions(object):
    def longestArithSeqLength(self, A):
        """
        :type A: List[int]
        :rtype: int
        """
        if not A or len(A) == 1:
            return 0
        length = len(A)
        dp = [dict(), ] * length
        result = float('-inf')
        for i in range(length):
            if i == 0:
                continue
            temp = dict()
            for j in range(length):
                if j >= i:
                    break
                if dp[j].get(A[i] - A[j]):
                    temp[A[i] - A[j]] = dp[j][A[i] - A[j]] + 1
                else:
                    temp[A[i] - A[j]] = 2
                result = max(result, temp[A[i] - A[j]])
            dp[i] = temp
        return result


if __name__ == '__main__':
    s = Solutions()
    print(s.longestArithSeqLength([20,1,15,3,10,5,8]))



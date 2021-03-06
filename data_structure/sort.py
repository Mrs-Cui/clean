#! /usr/bin/env python
# -*- coding:utf-8 -*-

import random

# 排序算法

# 堆排序

def heap_sort(start, end, items):
    mid = (start + end) / 2
    while mid > -1:
        index = 0
        if 2 * mid + 1 <= end and items[mid] < items[2 * mid + 1]:
            items[mid], items[2 * mid + 1] = items[2 * mid + 1], items[mid]
            index = 2 * mid + 1
        if 2 * mid + 2 <= end and items[mid] < items[2 * mid + 2]:
            items[mid], items[2 * mid + 2] = items[2 * mid + 2], items[mid]
            index = 2 * mid + 2
        if index != 0:
            wrap_sort(index, end, items)
        mid -= 1


def wrap_sort(index, end, items):
    if index >= end:
        return
    value = 0
    if 2 * index + 1 <= end and items[index] < items[2 * index + 1]:
        items[index], items[2 * index + 1] = items[2 * index + 1], items[index]
        value = 2 * index + 1
    if 2 * index + 2 <= end and items[index] < items[2 * index + 2]:
        items[index], items[2 * index + 2] = items[2 * index + 2], items[index]
        value = 2 * index + 2
    if value != 0:
        wrap_sort(value, end, items)

def new_warp_sort(index, end, items):
    if index < 0:
        return
    value = 0
    if 2 * index + 1 <= end and items[index] < items[2 * index + 1]:
        items[index], items[2 * index + 1] = items[2 * index + 1], items[index]
        value = 1
    if 2 * index + 2 <= end and items[index] < items[2 * index + 2]:
        items[index], items[2 * index + 2] = items[2 * index + 2], items[index]
        value = 1
    if value != 0:
        new_warp_sort((index - 1) / 2, end, items)

def heap_sort_main():
    items = [random.randrange(1, 30) for i in range(15)]
    print(items)
    heap_sort(0, len(items) - 1, items)
    print(items)
    indexs = range(len(items))
    indexs.reverse()
    for i in indexs:
        if i - 1 < 0:
            break
        items[0], items[i] = items[i], items[0]
        heap_sort(0, i - 1, items)
    print(items)

# 优先队列

def push_queue(item ,array):
    array.append(item)
    end = len(array) - 1
    index = end - 1
    new_warp_sort(index / 2, end, array)


def pop_queue(array):
    del array[0]
    new_warp_sort(0, len(array), array)


def priority_queue():
    items = [random.randrange(1, 30) for i in range(15)]
    heap_sort(0, len(items) - 1, items)
    push_queue(43, items)
    print(items)
    pop_queue(items)
    print(items)

# 跳跃表

class SkipNode(object):

    def __init__(self):
        self.key = None
        self.value = None
        self.child = [SkipNodeLevel(), ] * 32


class SkipNodeLevel(object):
    def __init__(self):
        self.skip_node = None
        self.level = None


class SkipNodeHead(object):

    def __init__(self):
        self.head = None
        self.tail = None
        self.level = None
        self.length = None


class SkipList(object):

    def __init__(self):
        self.skip_list = SkipNodeHead()


# 并查集

def and_check():

    def search_root(root, pre):
        son = root
        while root != pre[root]:
            root = pre[root]
        # 便于快捷查找
        while son != root:
            tmp = pre[son]
            pre[son] = root
            son = tmp

        return root

    def join(x, y, pre):
        root1 = search_root(x, pre)
        root2 = search_root(y, pre)
        if root1 != root2:
            pre[root2] = root1

    items = [i for i in range(20)]


"""
    给定一组 N 人（编号为 1, 2, ..., N）， 我们想把每个人分进任意大小的两组。
    每个人都可能不喜欢其他人，那么他们不应该属于同一组。
    形式上，如果 dislikes[i] = [a, b]，表示不允许将编号为 a 和 b 的人归入同一组。
    当可以用这种方法将每个人分进两组时，返回 true；否则返回 false。
"""

def like_group(array):
    people_queue = dict()

    def search(root, queue):
        son = root
        while root != queue.get(root, root):
            root = queue[root]
        while son != root:
            temp = queue.get(son, son)
            queue[temp] = root
            son = temp
        return root

    for people in array:
        parent_1 = search(people[0], people_queue)
        parent_2 = search(people[1], people_queue)
        if parent_1 != parent_2:
            people_queue[people[1]] = parent_1
    print(people_queue)


# 归并排序

def merge_split(start, end, nums):
    if start < end:
        middle = (end - start) / 2 + start
        left_nums = merge_split(start, middle, nums)
        right_nums = merge_split(middle+1, end, nums)
        return merge_sort(left_nums, right_nums)
    elif start == end:
        return [nums[start],]


def merge_sort(left_nums, right_nums):
    nums = []
    while left_nums or right_nums:
        if left_nums and right_nums:
            while left_nums and right_nums and left_nums[0] <= right_nums[0]:
                nums.append(left_nums.pop(0))
            while left_nums and right_nums and right_nums[0] < left_nums[0]:
                nums.append(right_nums.pop(0))
        elif left_nums:
            nums.extend(left_nums)
            left_nums = []
        elif right_nums:
            nums.extend(right_nums)
            right_nums = []
    return nums


def kmp(origin_str, pattern_str):
    next = kmp_next(pattern_str)
    print(next)
    i = j = 0
    pattern_length = len(pattern_str)
    origin_length = len(origin_str)
    while i < origin_length and j < pattern_length:
        if j == -1 or origin_str[i] == pattern_str[j]:
            i += 1
            j += 1
        else:
            j = next[j]
    print(i, j)
def kmp_next(pattern_str):
    length = len(pattern_str)
    next = [-1] * length
    i, j = 0, -1
    while i < length - 1:
        if j == -1 or pattern_str[i] == pattern_str[j]:
            i += 1
            j += 1
            next[i] = j
        else:
            j = next[j]
    return next


def is_pattern(pattern_str, original_str):
    pattern_len = len(pattern_str)
    original_len = len(original_str)
    pattern_start = original_start = 0
    flag = True
    while pattern_start < pattern_len:
        if original_start == original_len:
            break
        if pattern_str[pattern_start+1] not in ('*', '?'):
            if pattern_str[pattern_start] == '.':
                original_start += 1
                pattern_start += 1
            else:
                if pattern_str[pattern_start] == original_str[original_start]:
                    original_start += 1
                    pattern_start += 1
                else:
                    flag = False
                    break
        else:
            if pattern_str[pattern_start+1] == '*':
                if pattern_str[pattern_start+2] == '?':
                    pass
                else:
                    pass
            elif pattern_str[]:
                pass
    print(flag)

if __name__ == '__main__':
    array = [8, 9, 10, 4, 8, 7, 3, 0, -1, 7, 6, 5]
    print(merge_split(0, len(array) - 1, array))

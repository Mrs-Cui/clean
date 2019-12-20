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

if __name__ == '__main__':
    array = [[1,2],[1,3],[2,4]]
    like_group(array)

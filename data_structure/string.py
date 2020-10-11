#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
    与字符串相关的算法
"""

import array


# KMP 算法
import time


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
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j])
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
            result = max(result, dp[i + 1][j + 1])
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
        for j in range(1, aim + 1):
            dp[i][j] = dp[i - 1][j]
            if money[i - 1] > j:
                continue
            for z in range(1, aim + 1):
                if money[i - 1] * z <= j:
                    dp[i][j] += dp[i - 1][j - money[i - 1] * z]
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
    while (start_index < end_index):
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
            best_time[j] = max(best_time[j], best_time[j - arr[i]] + arr[i])
    print((sum - best_time[-1]) * 1024)


"""
    你面前有一栋从 1 到N共N层的楼，然后给你K个鸡蛋（K至少为 1）。现在确定这栋楼存在楼层0 <= F <= N，在这层楼将鸡蛋扔下去，
    鸡蛋恰好没摔碎（高于F的楼层都会碎，低于F的楼层都不会碎）。现在问你，最坏情况下，你至少要扔几次鸡蛋，才能确定这个楼层F呢？
"""


# def superEggDrop(K: int, start: int, end: int):
#     memo = dict()
#
#     def dp(K, start, end) -> int:
#         print(K, start, end)
#         # base case
#         if K == 1: return end - start
#         if start > end: return 0
#         # 避免重复计算
#         if (K, start) in memo:
#             return memo[(K, start)]
#
#         res = float('INF')
#         # 穷举所有可能的选择
#         # for i in range(1, N + 1):
#         i = (start + end) // 2
#         res = min(res,
#                   max(
#                       dp(K, i + 1, end),
#                       dp(K - 1, start, i - 1)
#                   ) + 1
#                   )
#         # 记入备忘录
#         memo[(K, start)] = res
#         return res
#
#     return dp(K, start, end)

class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        length = 0
        hash_map = {}
        for pos, item in enumerate(s, 1):
            if not hash_map.get(item):
                hash_map[item] = pos
            else:
                child_length = pos - hash_map[item]
                length = max(length, child_length)
                if child_length == 1:
                    if len(hash_map) != 1:
                        length = max(length, len(hash_map))
                    hash_map = {item: pos}
                else:
                    pass
        length = max(length, len(hash_map))
        return length




# 字符串匹配算法-> 正则表达式匹配

# input:  a -> [a-z] / ''
#         b　-> [a-z.*] / ''

# output: true/false


def regex_match(origin_str, pattern_str):
    pattern_len = len(pattern_str)
    origin_len = len(origin_str)
    i = j = 0
    pd = [[[-1, -1]for j in range(pattern_len)] for i in range(origin_len)]
    while i < pattern_len:
        if i == 0:
            if pattern_str[i] == '*':
                return False
            elif pattern_str[i] == '.':
                pd[i][j][0] = 0
            else:
                if pattern_str[i] != origin_str[j]:
                    return False
                else:
                    pd[i][j][0] = 0
            i += 1
            j += 1
            continue
        while j < origin_len:
            pass

        else:
            return True


class MinStack(object):

    def __init__(self):
        self.min = []
        self.stack = []

    def push(self, value):
        pos = 0
        if not self.min:
            self.min.append(value)
        else:
            for pos, item in enumerate(self.min):
                if item >= value:
                    self.min.insert(pos, value)
                    break
            else:
                pos = pos + 1
                self.min.insert(pos, value)
        self.stack.append((pos, value))

    def top(self):
        return self.stack[-1][1]

    def pop(self):
        pos, value = self.stack.pop(-1)
        self.min.pop(pos)

    def getMin(self):
        if self.min:
            return self.min[0]
        else:
            return None

class ListNode(object):
    def __init__(self, value, next=None):
        self.val = value
        self.next = next

class Chain(object):


    def addTwoNumbers(self, l1, l2):
        head = ListNode(0, None)
        head1 = head
        front = None
        while l1 or l2:
            num = carry = 0
            if l1:
                num += l1.val
                l1 = l1.next
            if l2:
                num += l2.val
                l2 = l2.next
            num = head1.val + num
            if num >= 10:
                carry = num / 10
                num = num % 10
                carry = int(carry)
            head1.val = num
            t = ListNode(carry, None)
            head1.next = t
            front = head1
            head1 = t
        else:
            if front.next.val == 0:
                front.next = None
            if front.val >= 10:
                node = ListNode(0, None)
                node.val = int(front.val / 10)
                front.val = int(front.val % 10)
                front.next = node
        while head:
            print(head.val)
            head = head.next
        return head

    def reverseList(self, head):
        if not head:
            return None
        else:
            new_head = self.reverseList(head.next)
            if not new_head:
                new_head = head
                new_head.tail = head
            else:
                new_tail = new_head.tail
                new_tail.next = head
                new_tail = new_tail.next
                new_tail.next = None
                new_head.tail = new_tail
            return new_head

    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        data_map = {}
        for list_node in lists:
            while list_node:
                if data_map.get(list_node.val):
                    tail = data_map[list_node.val]['tail']
                    tail.next = list_node
                    tail = tail.next
                    data_map[list_node.val]['tail'] = tail
                else:
                    data_map[list_node.val] = {}
                    data_map[list_node.val]['node'] = list_node
                    data_map[list_node.val]['tail'] = list_node
                    tail = list_node
                list_node = list_node.next
                tail.next = None
        values = list(data_map.keys())
        values.sort()
        head = None
        for value in values:
            if not head:
                head = data_map[value]['node']
                tail = data_map[value]['tail']
            else:
                tail.next = data_map[value]['node']
                tail = data_map[value]['tail']
        return head

    def get_mid(self, head):
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def merge_sort(self, first, second):
        head = head1 = None
        while first or second:
            mid = float('inf')
            if not head:
                if first.val <= second.val:
                    head = head1 = first
                    first = first.next
                else:
                    head = head1 = second
                    second = second.next
            else:
                if first and head1.val <= first.val:
                    mid = first.val
                    if not second:
                        head1.next = first
                        break
                if second and head1.val <= second.val:
                    if not first:
                        head1.next = second
                        break
                    if second.val < mid:
                        head1.next = second
                        head1 = head1.next
                        second = second.next
                        head1.next = None
                    else:
                        head1.next = first
                        head1 = head1.next
                        first = first.next
                        head1.next = None
        return head

    def sortList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if not head:
            return head
        mid = self.get_mid(head)
        if not mid or not mid.next:
            return mid
        first = head
        second = mid.next
        mid.next = None
        first = self.sortList(first)
        second = self.sortList(second)
        return self.merge_sort(first, second)

    def detectCycle(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

    def mergeTwoLists(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        head = head1 = None
        first, second = l1, l2
        while first or second:
            mid = float('inf')
            if not head:
                if not first and not second:
                    return None
                if not first:
                    return second
                if not second:
                    return first
                else:
                    if first and first.val <= second.val:
                        head = head1 = first
                        first = first.next
                    elif second and second.val:
                        head = head1 = second
                        second = second.next
                    head1.next = None
            else:
                if first and head1.val <= first.val:
                    mid = first.val
                    if not second:
                        head1.next = first
                        break
                if second and head1.val <= second.val:
                    if not first:
                        head1.next = second
                        break
                    if second.val < mid:
                        head1.next = second
                        head1 = head1.next
                        second = second.next
                        head1.next = None
                    else:
                        head1.next = first
                        head1 = head1.next
                        first = first.next
                        head1.next = None
        return head

    def lowestCommonAncestor(self, root, p, q):
        """
        :type root: TreeNode
        :type p: TreeNode
        :type q: TreeNode
        :rtype: TreeNode
        """
        root1 = root
        path_p = []
        path_q = []
        self.find_path(root1, p, path_p)
        self.find_path(root, q, path_q)
        path_p = {item: pos for pos, item in enumerate(path_p)}
        index = -1
        value = 0
        for item in path_q:
            if path_p.get(item) and path_p[item] >= index:
                index = path_p[item]
                value = item
        return TreeNode(value)


    def find_path(self, root, value, path):
        if not root:
            return False
        if root.val == value:
            return True
        path.append(root.val)
        flag = self.find_path(root.left, value, path)
        if flag:
            return flag
        flag = self.find_path(root.right, value, path)
        if flag:
            return flag
        else:
            path.pop(-1)
            return False

    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        length = 0
        hash_data = {}
        for pos, item in enumerate(s, 1):
            if not hash_data.get(item):
                hash_data[item] = pos
            else:
                child_length = pos - hash_data[item]
                if child_length == 1:
                    hash_len = len(hash_data)
                    if hash_len != 1:
                        length = max(length, hash_len)
                    hash_data = {item: pos}
                else:
                    length = max(length, len(hash_data))
                    pre_pos = hash_data[item]
                    remove_list = []
                    for key, value in hash_data.items():
                        if value < pre_pos:
                            remove_list.append(key)
                    for remove in remove_list:
                        hash_data.pop(remove)
                    hash_data[item] = pos
                    length = max(length, len(hash_data))
        length = max(length, len(hash_data))
        return length

    def checkInclusion(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """
        if len(s1) > len(s2):
            return False
        pattern_map = {}
        match_map = {}
        diff_map = {}
        new_start = start = end = 0
        for item in s1:
            end += 1
            pattern_map[item] = pattern_map.get(item, 0) + 1
        while new_start <= end - 1:
            match_map[s2[new_start]] = match_map.get(s2[new_start], 0) + 1
            new_start += 1
        if cmp(pattern_map, match_map) == 0:
            return True
        for key in match_map:
            if match_map[key] != pattern_map.get(key):
                diff_map[key] = True
        match_start = end
        while True:
            try:
                item = s2[match_start]
            except IndexError:
                return False
            match_map[item] = match_map.get(item, 0) + 1
            match_map[s2[start]] -= 1
            print(pattern_map, match_map, diff_map, match_start, start, item)
            if match_map[s2[start]] == 0:
                if diff_map.get(s2[start]):
                    del diff_map[s2[start]]
                del match_map[s2[start]]
            else:
                if match_map[s2[start]] == pattern_map.get(s2[start]):
                    if diff_map.get(s2[start]):
                        del diff_map[s2[start]]
                else:
                    diff_map[s2[start]] = True
            if match_map[item] != pattern_map.get(item):
                diff_map[item] = True
            else:
                if diff_map.get(item):
                    del diff_map[item]
            print(pattern_map, match_map, diff_map, match_start, start, item)
            if not diff_map:
                return True
            start += 1
            match_start += 1

    def multiply(self, num1, num2):
        """
        :type num1: str
        :type num2: str
        :rtype: str
        """
        length_1 = len(num1)
        length_2 = len(num2)
        result = [0] * (length_1 + length_2)
        num1 = num1[::-1]
        num2 = num2[::-1]
        if length_1 < length_2:
            num1, num2 = num2, num1
        for pos_1, item_1 in enumerate(num1, 1):
            for pos_2, item_2 in enumerate(num2, 0):
                value = int(item_1) * int(item_2)
                index = pos_2 + pos_1 - 1
                result[index] += value
                if result[index] >= 10:
                    self.handle_carry(index, result)
        result = ''.join([str(i) for i in result])
        result = result.rstrip('0')
        if not result:
            return '0'
        return result[::-1]

    def handle_carry(self, index, result):
        temp = result[index]
        result[index] = temp % 10
        result[index + 1] += temp / 10
        if result[index + 1] >= 10:
            self.handle_carry(index + 1, result)

    def simplifyPath(self, path):
        """
        :type path: str
        :rtype: str
        """
        stack = []
        dot_num = 0
        length = 0
        for item in path:
            print(stack, item, dot_num)
            if not stack:
                stack.append(item)
                length += 1
            else:
                if item == '.':
                    if stack[-1] == '/':
                        dot_num += 1
                        stack.append(item)
                        length += 1
                    elif stack[-1] == '.':
                        if dot_num != 0:
                            dot_num += 1
                            stack.append(item)
                            length += 1
                    elif stack[-1] != '.' and stack[-1] != '/':
                        stack[-1] += item
                elif item == '/':
                    if dot_num == 2:
                        while dot_num > 0:
                            stack.pop(-1)
                            length -= 1
                            dot_num -= 1
                        if length > 1:
                            if stack[-1] != '/':
                                stack.pop(-1)
                                length -= 1
                            else:
                                stack.pop(-1)
                                stack.pop(-1)
                                length -= 2
                        dot_num = 0
                    elif dot_num == 1:
                        stack.pop(-1)
                        length -= 1
                        dot_num = 0
                    elif dot_num == 0:
                        if stack[-1] != '/':
                            stack.append(item)
                            length += 1
                    else:
                        _ = []
                        while dot_num > 0:
                            _.append(stack.pop(-1))
                            length -= 1
                            dot_num -= 1
                        stack.append(''.join(_))
                        stack.append(item)
                        length += 2
                else:
                    if stack[-1] != '/':
                        if dot_num != 0:
                            _ = []
                            while dot_num > 0:
                                _.append(stack.pop(-1))
                                length -= 1
                                dot_num -= 1
                            _.append(item)
                            stack.append(''.join(_))
                            length += 1
                        else:
                            stack[-1] += item
                    else:
                        stack.append(item)
                        length += 1
        else:
            if dot_num == 2:
                while dot_num > 0:
                    stack.pop(-1)
                    length -= 1
                    dot_num -= 1
                if length > 1:
                    if stack[-1] != '/':
                        stack.pop(-1)
                        length -= 1
                    else:
                        stack.pop(-1)
                        stack.pop(-1)
                        length -= 2
            elif dot_num == 1:
                stack.pop(-1)
                length -= 1
        if length != 1 and stack[-1] == '/':
            stack.pop(-1)
        return ''.join(stack)

    def _restoreIpAddress(self, segment, s, ip_address, path):
        print(segment, s, ip_address, path)
        if segment < 0:
            return
        if segment == 0 and not s:
            path.append(ip_address)
        for pos, item in enumerate(s, 1):
            if not self.is_num(s[:pos]):
                break
            self._restoreIpAddress(segment-1, s[pos:], ip_address + '.' + s[:pos], path)

    def restoreIpAddresses(self, s):
        """
        :type s: str
        :rtype: List[str]
        """
        path = []
        if len(s) > 12 or len(s) < 4 or not s:
            return path
        for pos, item in enumerate(s, 1):
            if not self.is_num(s[:pos]):
                break
            self._restoreIpAddress(3, s[pos:], s[:pos], path)
        return path

    def is_num(self, num):
        if int(num) >=0 and int(num) <= 255 and str(int(num)) == num:
            return True
        return False

    def threeSum(self, nums):
        results = []
        nums.sort()
        length = len(nums)
        for pos, num in enumerate(nums):
            if pos > 0 and nums[pos] == nums[pos-1]:
                continue
            target = -num
            start, end = pos + 1, length - 1
            while start < end:
                if nums[start] + nums[end] == target:
                    results.append((num, nums[start], nums[end]))
                    while start < end and nums[start] == nums[start + 1]:
                        start += 1
                    while start < end and nums[end] == nums[end - 1]:
                        end -= 1
                    start += 1
                    end -= 1
                elif nums[start] + nums[end] < target:
                    start += 1
                elif nums[start] + nums[end] > target:
                    end -= 1
        return results

    def maxAreaOfIsland(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        max_size = 0
        row_len = len(grid)
        col_len = len(grid[0])
        for i, row in enumerate(grid):
            for j, item in enumerate(row):
                if grid[i][j]:
                    size = self.search(grid, i, j, row_len, col_len)
                    max_size = max(size, max_size)
        return max_size

    def search(self, grid, i, j, row_len, col_len):
        if i>=0 and i < row_len and j>=0 and j < col_len and grid[i][j] == 1:
            grid[i][j] = 0
            num = 1 + self.search(grid, i-1, j, row_len, col_len) + self.search(grid, i+1, j, row_len, col_len) +\
            self.search(grid, i, j-1, row_len, col_len) + self.search(grid, i, j+1, row_len, col_len)
            return num
        else:
            return 0

    def findKthLargest(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        target_list = nums[:k]
        target_list.sort()
        start, end = 0, k-1
        length = len(nums)
        while k < length:
            if nums[k] > target_list[start]:
                if nums[k] >= target_list[end]:
                    target_list.append(nums[k])
                else:
                    for pos, item in enumerate(target_list):
                        if nums[k] <= item:
                            break
                    target_list.insert(pos, nums[k])
                start += 1
                end += 1
            k += 1
        return target_list[start]

    def findLengthOfLCIS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        max_length = 0
        count = 0
        for pos, num in enumerate(nums):
            if pos == 0:
                count += 1
            else:
                if nums[pos] > nums[pos-1]:
                    count += 1
                else:
                    max_length = max(max_length, count)
                    count = 1
        max_length = max(max_length, count)
        return max_length

    def longestConsecutive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        map_data = {}
        max_length = 0
        for num in nums:
            if not map_data.get(num):
                map_data[num] = 1
                if map_data.get(num - 1):
                    map_data[num] += map_data[num - 1]
                if map_data.get(num + 1):
                    map_data[num] += map_data[num + 1]
                target = num - 1
                while map_data.get(target):
                    map_data[target] = map_data[num]
                    target -= 1
                target = num + 1
                while map_data.get(target):
                    map_data[target] = map_data[num]
                    target += 1
            else:
                pass
            # print(map_data, num)
            max_length = max(max_length, map_data[num])
        return max_length

    def findCircleNum(self, M):
        """
        :type M: List[List[int]]
        :rtype: int
        """
        if not M:
            return 0
        friend_map = {}
        for pos, item in enumerate(M[0]):
            friend_map[pos] = pos
            if M[0][pos]:
                friend_map[pos] = 0
        for i, item in enumerate(M):
            if i == 0:
                continue
            for j, _ in enumerate(item):
                if M[i][j] and i != j:
                    root = self.merge_friend(friend_map, j)
                    root_1 = self.merge_friend(friend_map, i)
                    for key, value in friend_map.items():
                        if value == root_1:
                            friend_map[key] = root
        head = []
        for key, value in friend_map.items():
            head.append(value)
        return len(set(head))


    def merge_friend(self, friend, i):
        head = i
        while head != friend[head]:
            head = friend[head]
        return head

    def merge(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        """

        intervals = sorted(intervals, key=lambda x: x[0])
        start, end = 1, len(intervals)
        while start < end:
            if intervals[start][0] <= intervals[start-1][1]:
                if intervals[start][1] > intervals[start-1][1]:
                    intervals[start-1][1] = intervals[start][1]
                intervals.pop(start)
                end -= 1
            elif intervals[start][0] > intervals[start-1][1]:
                start += 1
        return intervals

    def getPermutation(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """
        data = [i+1 for i in range(n)]
        def handle(n, k, data):
            step = num = 1
            if n == 0:
                return str(data[0])
            while step <= n:
                num *= step
                step += 1
            if k % num == 0:
                start = k / num - 1
            else:
                if k == num:
                    start = k / num -1
                else:
                    start = k / num
            pos = k % num
            result = str(data.pop(start))
            # print(n, k, start, pos, data, num)
            result += handle(n-1, pos, data)
            return result
        result = handle(n-1, k, data)
        return result

    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        end = len(height) - 1
        start = 0
        left_height = right_height = 0
        size = 0
        while start <= end:
            if left_height <= right_height:
                left_height = max(height[start], left_height)
                size += left_height - height[start]
                start += 1

            if right_height < left_height:
                right_height = max(height[end], right_height)
                size += right_height - height[end]
                end -= 1
        return size

    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        """
            0: 买，　1: 卖，　2: 啥也不干
        """
        sell = 0
        for pos, price in enumerate(prices):
            if pos == 0:
                continue
            if prices[pos] > prices[pos-1]:
                sell += prices[pos] - prices[pos-1]
        return sell

    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        dp = [0] * len(nums)
        max_value = float('-inf')
        for pos, item in enumerate(nums):
            if pos == 0:
                dp[pos] = item
            else:
                if item > item + dp[pos-1]:
                    dp[pos] = item
                else:
                    dp[pos] = item + dp[pos-1]
            max_value = max(dp[pos], max_value)
        return max_value

    def makeGood(self, s):
        """
        :type s: str
        :rtype: str
        """
        start, end = 0, len(s) - 1
        s = list(s)
        while start < end:
            pass

class TreeNode(object):

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class LineNode(object):

    def __init__(self, val, next):
        self.val = val
        self.next = next

class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.cache = {}
        self.current_capacity = 0
        self.stack = []
        self.stack_len = 0
        self.head = ListNode(-1)
        self.tail = self.head

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if self.cache.get(key):
            pass
        return -1

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if self.current_capacity < self.capacity:
            if self.cache.get(key):
                pass
            else:
                pass
            self.current_capacity += 1
        else:
            pass


def getResult(n, m):
    if m < 0 or n < 0:
        return 0
    if (m == 1 and n == 0) or (n == 1 and m == 0):
        return 1
    return getResult(n, m - 1) + getResult(n - 1, m)


def build_head(nums, pos, length):
    left_pos = 2 * pos + 1
    right_pos = 2 * pos + 2
    index = 0
    if left_pos < length and nums[pos] < nums[left_pos]:
        nums[pos], nums[left_pos] = nums[left_pos], nums[pos]
        index = left_pos
    if right_pos <length and nums[pos] < nums[right_pos]:
        nums[pos], nums[right_pos] = nums[right_pos], nums[pos]
        index = right_pos
    if index != 0:
        build_head(nums, index, length)



if __name__ == '__main__':
    # while True:
    #     try:
    #         n, k = (int(i) for i in raw_input().split(' '))
    #         nums = [int(i) for i in raw_input().split(' ')]
    #     except EOFError as e:
    #         break
    #     k_small = nums[:k]
    #     middle = k / 2
    #     while middle >= 0:
    #         build_head(k_small, middle, k)
    #         middle -= 1
    #     length = k
    #     while k < n:
    #         if nums[k] < k_small[0]:
    #             k_small[0] = nums[k]
    #             build_head(k_small, 0, length)
    #         k += 1
    #     end = length - 1
    #     while end > 0:
    #         k_small[0], k_small[end] = k_small[end], k_small[0]
    #         build_head(k_small, 0, end - 1)
    #         end -= 1
    #     print(' '.join([str(i) for i in k_small]))

    # while True:
    #     try:
    #         password_str = raw_input()
    #     except EOFError as e:
    #         break
    #     flag = [False, ] * 4
    #     length = 0
    #     count = 0
    #     repeat_flag = False
    #     hash_map = {}
    #     for pos, item in enumerate(password_str):
    #         length += 1
    #         if item >= 'a' and item <= 'z':
    #             flag[0] = True
    #         elif item >='A' and item <= 'Z':
    #             flag[1] = True
    #         elif item >= '0' and item <= '9':
    #             flag[2] = True
    #         else:
    #             flag[3] = True
    #         hash_map.setdefault(item, [])
    #         if hash_map.get(item):
    #             for index in hash_map[item]:
    #                 try:
    #                     if [password_str[index], password_str[index+1], password_str[index+2]] == [
    #                         password_str[pos], password_str[pos+1], password_str[pos+2]
    #                     ]:
    #                         repeat_flag = True
    #                         break
    #                 except IndexError as e:
    #                     break
    #             hash_map[item].append(pos)
    #         else:
    #             hash_map[item].append(pos)
    #     tmp = 0
    #     for i in flag:
    #         if i:
    #             tmp += 1
    #     if length > 8 and not repeat_flag and tmp >= 3:
    #         print('OK')
    #     else:
    #         print('NG')
    numbers_str = raw_input()
    int_str, dot_str = numbers_str.split('.')
    cn_numbers = ['', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖', '拾']
    small_carry = ['', '拾', '佰', '仟']
    big_carry = ['万', '亿']
    int_list = []
    int_str = int_str[::-1]
    int_list.append('元')
    have_zero = False
    zero_index = -1
    for pos, item in enumerate(list(int_str)):
        if pos % 4 == 0 and pos % 8 != 0 and pos != 0:
            if int_list[-1] in ['万', '亿']:
                int_list.pop(-1)
            int_list.append('万')
        elif pos % 8 == 0 and pos != 0:
            if int_list[-1] in ['万', '亿']:
                int_list.pop(-1)
            int_list.append('亿')
        if item == '0':
            if int_list[-1] != '零':
                if int_list[-1] not in ['万', '亿']:
                    int_list.append('零')
            continue
        int_list.append(small_carry[pos % 4])
        int_list.append(cn_numbers[int(item)])
    if dot_str == '00':
        dot_str = '整'
    else:
        _ = []
        for pos, i in enumerate(list(dot_str)):
            if pos == 0:
                _.extend([cn_numbers[int(dot_str[0])], '角'])
            elif pos == 1:
                _.extend([cn_numbers[int(dot_str[1])], '分'])
        dot_str = ''.join(_)
    print ''.join(['人民币',''.join(int_list[::-1]),dot_str])
    # n = int(input())
    # m = int(input())
    #
    #
    # def getResult(n, m):
    #     n, m = n + 1, m + 1
    #     dp = [0 for i in range(m)]
    #     dp[0] = 1
    #     for row, _ in enumerate(range(n)):
    #         for col, _ in enumerate(range(m)):
    #             if col == 0:
    #                 continue
    #             dp[col] += dp[col - 1]
    #     return dp[m - 1]
    #
    #
    # print(getResult(n, m))

    from copy import deepcopy

    n, m = [int(i) for i in input().split(' ')]
    nums = []
    for i in range(n):
        nums.append([int(i) for i in input().split(' ')])
    path = []

    def find_path(i, j, nums, child_path=None):
        global path
        global n
        global m
        if 0 <= i < n and 0 <= j < m:
            if nums[i][j] == 0:
                child_path.append((int(i), int(j)))
                if i == n - 1 and j == m - 1:
                    path.append(child_path)
                else:
                    if (i - 1, j) not in child_path:
                        find_path(i - 1, j, nums, deepcopy(child_path))
                    if (i + 1, j) not in child_path:
                        find_path(i + 1, j, nums, deepcopy(child_path))
                    if (i, j - 1) not in child_path:
                        find_path(i, j - 1, nums, deepcopy(child_path))
                    if (i, j + 1) not in child_path:
                        find_path(i, j + 1, nums, deepcopy(child_path))

    find_path(0, 0, nums, [])
    length = 0
    result = []
    for pos, i in enumerate(path):
        if pos == 0:
            length = len(i)
            result = i
        else:
            tmp = len(i)
            if tmp < length:
                length = tmp
                result = i
    print('aaaaaaa')
    for i in result:
        print('({0}, {1})'.format(*i))



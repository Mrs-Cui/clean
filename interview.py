# /usr/bin/env python
#-*-coding:utf-8-*-

def sort(nums):
    length = len(nums)
    for i in range(length-1):
        for j in range(i, length):
            if nums[i] > nums[j]:
                nums[i], nums[j] = nums[j], nums[i]

    map = {
        1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'
    }
    big_nums = ['', '十', '百', '千']
    nums = [i for i in nums if i != 0]
    end = len(nums) - 1
    start = 0
    result = ''
    while end >= 0:
        result += map[nums[start]] + big_nums[end]
        end -= 1
        start += 1
    print(result)








class Test(object):

    def __init__(self):
        pass

    @property
    def current(self):
        return self


def find(arr, target, start, end):
    middle = (end - start) / 2 + start
    if start > end:
        return
    if arr[middle] == target:
        return arr[middle]
    elif arr[middle] > target:
        return find(arr, target, start, middle)
    elif arr[middle] < target:
        return find(arr, target, middle + 1, end)

def kongge(arr):
    target = ''
    for pos, item in enumerate(arr):
        if pos == 0:
            target += item
        else:
            if arr[pos] == ' ':
                if arr[pos-1] == ' ':
                    continue
                else:
                    target += item
            else:
                target += item





import os
def ping(ip):
    ip_list = ip.split('.')
    if len(ip_list) == 4:
        for item in ip_list:
            if int(item) >= 0 and int(item) <= 255:
                continue
            else:
                return
        popen = os.popen('ping {0} -c 5'.format(ip))
        print(popen._proc.stdout.readlines(11))



#崔希艺
# 17865922913
def maxLength(array_str):

    length = len(array_str)
    flag = 0
    start = 0
    max_length = 0
    while start < length:
        index = 0
        if array_str[start] in array_str[flag:start]:
            index = array_str[flag:start].find(array_str[start])
            max_length = max(max_length, start - (index + flag))
            flag = index + flag + 1
        else:
            max_length = (start - flag) + 1
        print(array_str[start], index, max_length, flag)
        start += 1
    return max_length



























if __name__ == '__main__':
    print(maxLength('abccccbbcddfggg'))


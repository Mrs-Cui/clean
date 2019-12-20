#! /usr/bin/env python
# -*- coding:utf-8 -*-

# 汉诺塔


def han_no_ta(a, b, c, n):
    if n == 1:
        print('from {0}, with help {1}, to {2}, {3}'.format(a, b, c, n))
    else:
        han_no_ta(a, c, b, n-1)
        print('from {0}, with help {1}, to {2}, {3}'.format(a, b, c, n))
        han_no_ta(b, a, c, n-1)

def recursive(n):
    han_no_ta('A', 'B', 'C', n)


# 尾递归


# 给出一个n * m 矩阵, 找出从左下角到右上角最短路径的值

def min_path():
    pass

if __name__ == '__main__':
    recursive(8)

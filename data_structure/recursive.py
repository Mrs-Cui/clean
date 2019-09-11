#! /usr/bin/env python
# -*- coding:utf-8 -*-

# 汉诺塔


def han_no_ta(a, b, c, n):
    if n == 1:
        print 'from {0}, with help {1}, to {2}, {3}'.format(a, b, c, n)
    else:
        han_no_ta(a, c, b, n-1)
        print 'from {0}, with help {1}, to {2}, {3}'.format(a, b, c, n)
        han_no_ta(b, a, c, n-1)

def recursive(n):
    han_no_ta('A', 'B', 'C', n)


# 尾递归

if __name__ == '__main__':
    recursive(8)
#! /usr/bin/env python
# -*- coding:utf-8 -*-

# hash 解决冲突的方法:
"""
1. 开放寻址法:
    H0 = (H(key) + di) / m
    线性探测: di = 1, 2, 3 .... m-1
    平方探测: di = 1*2, -(1*2), 2*2, -(2*2) ... -(m-1)*2
    随机探测: di 是一组随机数
2. 链地址法.
3. 建立公共溢出区: 将哈希表分为基本表和溢出表两部分，凡是和基本表发生冲突的元素，一律填入溢出表
4. 再哈希法:  多个哈希函数.
"""

# 布隆过滤器
"""
布隆过滤器原理
    如果想判断一个元素是不是在一个集合里，一般想到的是将集合中所有元素保存起来，然后通过比较确定。
    链表、树、散列表（又叫哈希表，Hash table等等数据结构都是这种思路。但是随着集合中元素的增加，我们需要的存储空间越来越大。同时检索速度也越来越慢。
    Bloom Filter 是一种空间效率很高的随机数据结构，Bloom filter 可以看做是对 bit-map 的扩展, 它的原理是：
    当一个元素被加入集合时，通过 K 个 Hash 函数将这个元素映射成一个位阵列（Bit array）中的 K 个点，把它们置为 1。
    检索时，我们只要看看这些点是不是都是 1 就（大约）知道集合中有没有它了：

        如果这些点有任何一个 0，则被检索元素一定不在；
        如果都是 1，则被检索元素很可能在。
优点:
    它的优点是空间效率和查询时间都远远超过一般的算法，布隆过滤器存储空间和插入 / 查询时间都是常数O(k)。
    另外, 散列函数相互之间没有关系，方便由硬件并行实现。布隆过滤器不需要存储元素本身，在某些对保密要求非常严格的场合有优势。
缺点:
    但是布隆过滤器的缺点和优点一样明显。误算率是其中之一。随着存入的元素数量增加，误算率随之增加。但是如果元素数量太少，则使用散列表足矣
"""

if __name__ == '__main__':
    pass

#! /usr/bin/env python
# -*- coding:utf-8 -*-


# 树
"""
    二叉树节点计算:
        每层最大的节点数量: 2^(n-1)
        二叉树的节点数量: N = n0 + n1 + n2
        对于任意二叉树满足: n0 = n2 + 1
        二叉树深度: k = log2^N + 1
"""

#  已知 树的前序和中序, 创建二叉树

"""
    例:  前序遍历: GDAFEMHZ
        中序遍历: ADEFGHMZ
    例:
    中序遍历:   ADEFGHMZ
    后序遍历:   AEFDHZMG
"""



class Tree(object):

    def __init__(self, data=None):
        self.data = data
        self.lchild = None
        self.rchild = None
        self.ltag = 1
        self.rtag = 1

class Index(object):
    def __init__(self, pos):
        self.pos = pos

def create_tree(front_str, mid_str, index, flag):
    root = Tree(front_str[index.pos])
    length = len(mid_str)

    if length == 1:
        return root
    mid_index = mid_str.index(front_str[index.pos])
    left_mid = mid_str[0:mid_index]
    right_mid = mid_str[mid_index + 1: length]
    if left_mid:
        index.pos += 1
        root.lchild = create_tree(front_str, left_mid, index, 'left')
    if right_mid:
        index.pos += 1
        root.rchild = create_tree(front_str, right_mid, index, 'right')
    return root

def tree_prefix(front_str, middle_str):
    index = Index(0)

    root = create_tree(front_str, middle_str, index, 'root')
    return root


def front_tree(root):
    if not root:
        return
    front_tree(root.lchild)
    front_tree(root.rchild)
    print root.data

# 线索二叉树
"""
    线索二叉树: 对一个二叉树进行中序遍历就能得到 一个节点的前驱和后继节点。 线索二叉树就是在进行中序
    遍历时记录下这种前驱和后继的关系, 等到再次遍历时能提高效率。
"""

def mid_tree(root, pre):

    if root:
        mid_tree(root.lchild, pre)
        print root.data,   pre.data if pre else None

        if not root.lchild:
            root.lchild = pre
            root.ltag = 0
        if pre and not pre.rchild:
            pre.rtag = 0
            pre.rchild = root
        pre = root
        mid_tree(root.rchild, pre)
    return pre
if __name__ == '__main__':
    front_str = 'GDAFEMHZ'
    mid_str = 'ADEFGHMZ'
    root = tree_prefix(front_str, mid_str)
    mid_tree(root, None)
    print root.lchild.lchild.data
    print root.lchild.lchild.rchild
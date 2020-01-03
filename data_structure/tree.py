#! /usr/bin/env python
# -*- coding:utf-8 -*-

import random
import array

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
    print(root.data)

# 线索二叉树
"""
    线索二叉树: 对一个二叉树进行中序遍历就能得到 一个节点的前驱和后继节点。 线索二叉树就是在进行中序
    遍历时记录下这种前驱和后继的关系, 等到再次遍历时能提高效率。
"""
# python对象传值是引用，但是 a = b, 是赋值会申请新的内存空间。
def mid_tree(root, pre):

    if root:
        mid_tree(root.lchild, pre)
        print(root.data,   pre[0].data if pre[0] else None, 'first')

        if not root.lchild:
            root.lchild = pre[0]
            root.ltag = 0
        if pre[0] and not pre[0].rchild:
            pre[0].rtag = 0
            pre[0].rchild = root
        pre[0] = root
        mid_tree(root.rchild, pre)
    return pre


# 赫夫曼树
"""
    定义: 当用 n 个结点（都做叶子结点且都有各自的权值）试图构建一棵树时，如果构建的这棵树的带权路径长度最小，
    称这棵树为“最优二叉树”，有时也叫“赫夫曼树”或者“哈夫曼树”。
    遵循的原则: 权重越大的结点离树根越近。
    建树过程：
        1. 在 n 个权值中选出两个最小的权值，对应的两个结点组成一个新的二叉树，且新二叉树的根结点的权值为左右孩子权值的和,
        2. 在原有的 n 个权值中删除那两个最小的权值，同时将新的权值加入到 n–2 个权值的行列中,
        3. 重复 1 和 2 ，直到所以的结点构建成了一棵二叉树为止。
"""

def find_pos(trees, root, left, right):
    mid = (right - left) / 2 + left
    if left > right:
        return left
    if trees[mid].data == root.data:
        pos = mid + 1
    elif trees[mid].data > root.data:
        pos = find_pos(trees, root, left, mid - 1)
    else:
        pos = find_pos(trees, root, mid + 1, right)
    return pos

def huffman_tree(trees, root):
    if not trees:
        return root
    lchild, rchild = trees.pop(0), trees.pop(0)
    root = Tree(lchild.data + rchild.data)
    root.lchild, root.rchild = lchild, rchild
    if trees:
        pos = find_pos(trees, root, 0, len(trees) - 1)
        print(pos, root.data)
        trees.insert(pos, root)
    root = huffman_tree(trees, root)
    return root

"""
    线段树: 求区间和问题
"""


def line_segment_tree(root ,arr, left, right, line_segment):
    if left == right:
        line_segment[root][1] = arr[left]
        line_segment[root][0] = left
        line_segment[root][2] = right
    else:
        mid = (left + right) / 2
        line_segment_tree(2 * root + 1, arr, left, mid, line_segment)
        line_segment_tree(2 * root + 2, arr, mid + 1, right, line_segment)
        line_segment[root][1] = sum([line_segment[2 * root + 1][1], line_segment[2 * root + 2][1]])
        line_segment[root][0] = line_segment[2 * root + 1][0]
        line_segment[root][2] = line_segment[2 * root + 2][2]



def push_down(root, line_segment):
    if (line_segment[root][3]):
        line_segment[2 * root + 1][3] += line_segment[root][3]
        line_segment[2 * root + 2][3] += line_segment[root][3]
        # line_segment[2 * root + 1][1] += line_segment[root][3] * (line_segment[2 * root + 1][2] - line_segment[2 * root + 1][0] + 1)
        # line_segment[2 * root + 2][1] += line_segment[root][3] * (line_segment[2 * root + 2][2] - line_segment[2 * root + 2][0] + 1)
        line_segment[root][3] = 0


def update(root, left, right, add, line_segment):
    """
        目标的更新区间为[left,right]
        显然如果没交集就不管他。
       如果二者区间有交集我们再详细处理
       如果当前查找的区间是我们目标区间的其中一个子区间，自然直接返回即可。
    """
    if left > line_segment[root][2] or right < line_segment[root][0]:
        return
    elif left <= line_segment[root][0] and line_segment[root][2] <= right:
        line_segment[root][3] += add
        line_segment[root][1] += add * (line_segment[root][2] - line_segment[root][0] + 1)
        return
    push_down(root, line_segment)
    mid = (line_segment[root][0] + line_segment[root][2]) / 2
    if right <= mid:
        update(root * 2 + 1, left, right, add, line_segment)
    elif mid + 1 <= left:
        update(root * 2 + 2, left, right, add, line_segment)
    else:
        update(root * 2 + 1, left, mid, add, line_segment)
        update(root * 2 + 2, mid + 1, right, add, line_segment)

    line_segment[root][1] = line_segment[2 * root + 1][1] + line_segment[2 * root + 2][1]


def query_line_segment(root, left, right, line_segment):
    left_value = right_value = 0

    if left > line_segment[root][2] or right < line_segment[root][0]:
        return 0
    elif left <= line_segment[root][0] and line_segment[root][2] <= right:
        return line_segment[root][1]
    mid = (line_segment[root][0] + line_segment[root][2]) / 2
    if right <= mid:
        left_value = query_line_segment(root * 2 + 1, left, right, line_segment)
    elif mid + 1 <= left:
        right_value = query_line_segment(root * 2 + 2, left, right, line_segment)
    else:
        left_value = query_line_segment(root * 2 + 1, left, mid, line_segment)
        right_value = query_line_segment(root * 2 + 2, mid + 1, right, line_segment)

    print(root, left, right, line_segment[root][0], line_segment[root][2], left_value, right_value)

    return left_value + right_value







"""
    平衡二叉树:
"""
class BalanceTree(object):

    def __init__(self, data):
        self.lchild = None
        self.rchild = None
        self.data = data
        self.height = 1


def height(root):
    if not root:
        return 0
    else:
        return root.height

def lrchild(root):
    child = root.lchild
    root.lchild = rrchild(child)
    return llchild(root)


def llchild(root):

    child = root.lchild
    root.lchild = child.rchild
    child.rchild = root
    root.height = max(height(root.lchild), height(root.rchild)) + 1
    child.height = max(height(child.lchild), height(child.rchild)) + 1
    return child

def rlchild(root):
    child = root.rchild
    root.rchild = llchild(child)
    return rrchild(root)

def rrchild(root):
    child = root.rchild
    root.rchild = child.lchild
    child.lchild = root
    root.height = max(height(root.lchild), height(root.rchild)) + 1
    child.height = max(height(child.lchild), height(child.rchild)) + 1

    return child


def balance_tree(node, root):
    if not root:
        root = BalanceTree(node)
    else:
        if node <= root.data:
            root.lchild = balance_tree(node, root.lchild)
        else:
            root.rchild = balance_tree(node, root.rchild)

        if height(root.lchild) - height(root.rchild) >= 2:
            if node <= root.data:
                root = llchild(root)
            else:
                root = lrchild(root)
        elif height(root.rchild) - height(root.lchild) >= 2:
            if node <= root.data:
                root = rlchild(root)
            else:
                root = rrchild(root)
    print(root.data, node)
    return root


"""
知道先序和中序,建立二叉树
"""


def rebuild_tree(adv_array, mid_array, start, end, root):
    if start > end:
        return None
    pos = mid_array.find(adv_array[root.pos])
    print(start, end, pos, root.pos)

    tree = Tree(mid_array[pos])
    root.pos += 1
    tree.lchild = rebuild_tree(adv_array, mid_array, start, pos-1, root)
    tree.rchild = rebuild_tree(adv_array, mid_array, pos+1, end, root)

    return tree

"""
    最小生成树
"""

if __name__ == '__main__':
    front_str = 'GDAFEMHZ'
    mid_str = 'ADEFGHMZ'
    index = Index(0)
    root = rebuild_tree(front_str, mid_str, 0, len(front_str)-1, index)
    print(root.lchild.data, root.rchild.data)
    # mid_tree(root, [None, ])
    nodes = random.sample(range(1, 20), 15)
    # trees = []
    # root = None
    # for node in nodes:
    #     trees.append(Tree(node))
    # trees = sorted(trees, key=lambda tree: tree.data, reverse=False)
    #
    # root = huffman_tree(trees, root)
    # print root.data, root.lchild.data, root.rchild.data


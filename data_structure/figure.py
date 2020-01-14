#! /usr/bin/env python
# -*- coding:utf-8 -*-


"""
    最小生成树
"""

"""
    普利姆算法:
        首先先任意选出一个节点作为开始节点. 找出开始节点到其他节点最小距离,
        将该点记录下来. 设置两个集合 U, V.U集合存放找到最短距离的节点,
        V集合存放未找到最短距离的节点. 
"""


def mini_span_tree(weight_map):
    nodes = [key for key in weight_map.keys()]
    weights = dict()
    finish_nodes = []
    finish_nodes.append(nodes.pop(0))
    while nodes:
        min_weight = float('inf')
        for finish_node in finish_nodes:
            for node in nodes:
                if weight_map[finish_node].get(node, float('inf')) < min_weight:
                    min_node = node
                    min_weight = weight_map[finish_node][node]
        else:
            finish_nodes.append(min_node)
            weights[min_node] = min_weight
            nodes.remove(min_node)
    print(weights, finish_nodes)


"""
    Kruskal算法:
"""
"""
    对所有权边排序, 每次选取最小边, 直到完成最小生成树. n-1条边中不能有回路.
"""


def mini_span_tree_2(weight_map):
    weight = []
    for key, value in weight_map.items():
        for node, weight_value in value.items():
            weight.append((key, node, weight_value))
    weights = sorted(weight, key=lambda item: item[2], reverse=False)
    length = len(weight_map)
    union_node = {}
    weight = []

    def search_node(node):
        child = node
        while node != union_node.get(node, node):
            node = union_node[node]
        while child != node:
            temp = union_node[child]
            union_node[child] = node
            child = temp
        return node

    def join(node1, node2):
        parent1 = search_node(node1)
        parent2 = search_node(node2)
        if parent1 != parent2:
            union_node[parent2] = parent1
        return parent1 == parent2

    while weights:
        nodes = weights.pop(0)
        if not join(nodes[0], nodes[1]):
            weight.append(nodes)
    print(weight)


"""
    图的存储方式-> 十字链表
"""

class Figure(object):
    start_node = None
    end_node = None
    head_link = None
    tail_link = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class CrossLinkNode(object):
    weight = None
    first_in = None
    first_out = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def figure_cache(weight_map):
    figure_map = {}
    for key, value in weight_map.items():
        figure_map[key] = CrossLinkNode(first_in=Figure(), first_out=Figure())

    for start_node, end_nodes in weight_map.items():

        for end_node, weight in end_nodes.items():

            node = Figure(start_node=start_node, end_node=end_node)
            node.head_link = figure_map[end_node].first_in
            node.tail_link = figure_map[start_node].first_out

            figure_map[end_node].first_in = node
            figure_map[start_node].first_out = node
    return figure_map


"""
    最短路径
"""


if __name__ == '__main__':
    weight_map = {
        'A': {
            'B': 6,
            'C': 3
        },
        'B': {
            'C': 4,
            'D': 2,
            'F': 3,
        },
        'C': {
            'B': 4,
            'F': 7,
            'E': 8
        },
        'D': {
            'B': 2,
            'F': 6
        },
        'E': {
            'C': 8,
            'F': 7
        },
        'F': {
            'B': 3,
            'C': 7,
            'D': 6,
            'E': 7
        }
    }
    mini_span_tree(weight_map)
    mini_span_tree_2(weight_map)
    import fcntl
    fcntl.fcntl()

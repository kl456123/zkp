# -*- coding: utf-8 -*-

from hashlib import sha256
from math import log2, ceil

from field import FieldElement

class MerkleTree(object):

    def __init__(self, data):
        assert isinstance(data, list)
        assert len(data) > 0, 'Cannot construct an empty Merkle Tree.'
        num_leaves = 2**ceil(log2(len(data)))
        self.data = data + [FieldElement.zero()] * (num_leaves-len(data))
        self.height = int(log2(num_leaves))
        self.root = self.build_tree()

    def get_authentication_path(self, leaf_id):
        assert 0<=leaf_id < len(data)
        node_id = leaf_id + len(data)
        cur = self.root
        decommitment = []

        for bit in bin(node_id)[3:]:
            cur, auth = self.facts[cur]
            if bit == '1':
                auth, cur = cur, auth
            decommitment.append(auth)
        return decommitment

    def build_tree():
        return self.recursive_build_tree(1)

    def recursive_build_tree(node_id):
        if node_id>=len(self.data):
            id_in_data = node_id - len(self.data)
            leaf_data = self.data[id_in_data]
            h = sha256(h.encode()).hexdigest()
            self.facts[h] = leaf_data
            return h
        else:
            left_node = self.recursive_build_tree(2*node_id)
            right_node = self.recursive_build_tree(2*node_id+1)
            h = sha256((left_node+right_node).encode()).hexdigest()
            self.facts[h] = (left_node, right_node)
            return h


def verify_decommitment(leaf_id, leaf_data, decommitment, root):
    leaf_num = 2 ** len(decommitment)
    node_id = leaf_id + leaf_num
    cur = sha256(str(leaf_data).encode()).hexdigest()
    for bit, auth in zip(bin(node_id)[3:][::-1], decommitment[::-1]):
        if bit == '0':
            h = cur + auth
        else:
            h = auth + cur
        cur = sha256(h.encode()).hexdigest()
    return cur == root

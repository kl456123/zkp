# -*- coding: utf-8 -*-

import random
import hashlib
from math import log2, ceil

def hash_string(s):
    return hashlib.sha256(s.encode()).hexdigest()

# side_obfuscator and shift used for confusion
def get_witness(problem, assignment):
    sum = 0
    mx = 0
    witness = []
    side_obfuscator = 1 - 2 * random.randint(0, 1)
    assert len(problem) == len(assignment)
    for num, side in zip(problem, assignment):
        assert side == 1 or side == -1
        sum+= side * num * side_obfuscator
        witness += [sum]
        mx = max(mx, num)

    assert sum == 0
    shift = random.randint(0, mx)
    witness = [ x + shift for x in witness]
    return witness



class ZKMerkleTree(object):
    def __init__(self, data):
        self.data = data
        # extend data
        next_pow_of_2 = int(2**ceil(log2(len(data))))
        self.data.extend([0]* (next_pow_of_2-len(data)))

        rand_list = [random.randint(0, 1<<32) for x in self.data]
        self.data = [x for tup in zip(self.data, rand_list) for x in tup]

        self.tree = ["" for x in self.data] + [hash_string(str(x)) for x in self.data]
        for i in range(len(self.data)-1, 0, -1):
            self.tree[i] = hash_string(self.tree[2*i] + self.tree[2*i+1])


    def get_root(self):
        return self.tree[1]

    def get_val_and_path(self, id):
        id = id * 2
        val = self.data[id]
        auth_path = []
        id = id + len(self.data)
        while id > 1:
            auth_path.append(self.tree[id^1])
            id = id//2
        return val, auth_path


def verify_zk_merkle_path(root, data_size, value_id, value, path):
    cur = hash_string(str(value))
    tree_node_id = value_id*2 + int(2**ceil(log2(data_size*2)))
    for sibling in path:
        assert tree_node_id > 1
        if tree_node_id%2==0:
            cur = hash_string(cur+sibling)
        else:
            cur = hash_string(sibling+cur)
        tree_node_id = tree_node_id//2
    assert tree_node_id == 1
    return root == cur

def get_proof(problem, assignment, num_queries):
    proof = []
    randomness_seed = problem[:]
    for i in range(num_queries):
        witness = get_witness(problem, assignment)
        tree = ZKMerkleTree(witness)
        random.seed(str(randomness_seed))
        query_idx = random.randint(0, len(problem))
        # 1. merkle root
        query_and_response = [tree.get_root()]
        # 2. query idx
        query_and_response.extend([query_idx])
        # 3. cur proof
        query_and_response.extend(tree.get_val_and_path(query_idx))
        # 4. sibling proof
        query_and_response.extend(tree.get_val_and_path((query_idx+1)%len(witness)))

        # collect all queries
        proof.append(query_and_response)

        randomness_seed.append(query_and_response)
    return proof

def verify_proof(problem, proof):
    proof_checks_out = True
    randomness_seed = problem[:]
    for query in proof:
        random.seed(str(randomness_seed))
        query_idx = random.randint(0, len(problem))
        merkle_root = query[0]
        # query idx
        proof_checks_out&= query_idx==query[1]

        # test witness properies
        if query_idx < len(problem):
            proof_checks_out &= abs(query[2]- query[4]) == abs(problem[query_idx])
        else:
            # the first one and the last one
            proof_checks_out &= query[2]==query[4]

        # auth path
        proof_checks_out&= verify_zk_merkle_path(merkle_root, len(problem) + 1, query_idx, query[2], query[3])
        proof_checks_out&= verify_zk_merkle_path(merkle_root, len(problem) + 1, (query_idx+1)%(len(problem)+1), query[4], query[5])
        randomness_seed.append(query)

def test(q):
    problem = [1, 2, 3, 6, 6, 6, 12]
    assignment = [1, 1, 1, -1, -1, -1, 1]
    proof = get_proof(problem, assignment, q)

    print(proof)
    return verify_proof(problem, proof)

if __name__=='__main__':
    test(4)

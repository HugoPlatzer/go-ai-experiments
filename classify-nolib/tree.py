#!/usr/bin/python3

from random import random, choice


class Tree():
  def __init__(self, in_size, tree):
    self.in_size = in_size
    self.edge_size = int(in_size**0.5)
    self.tree = tree
    
  def compute(self, d_in, tree=None):
    if tree is None:
      tree = self.tree
    op_params = [self.compute(d_in, subtree) for subtree in tree[1:]]
    return self.compute_op(d_in, tree[0], op_params)
  
  def compute_op(self, d_in, op, params):
    inA = params[0] if len(params) > 0 else None
    inB = params[1] if len(params) > 1 else None
    if op == "add":
      return [inA[i] + inB[i] for i in range(self.in_size)]
    elif op == "sub":
      return [inA[i] - inB[i] for i in range(self.in_size)]
    elif op == "mul":
      return [inA[i] * inB[i] for i in range(self.in_size)]
    elif op == "thr":
      return [max(0, inA[i]) for i in range(self.in_size)]
    elif op == "sl":
      return [(inA[i + 1] if (i % self.edge_size < (self.edge_size - 1)) else 0) for i in range(self.in_size)]
    elif op == "sr":
      return [(inA[i - 1] if (i % self.edge_size > 0) else 0) for i in range(self.in_size)]
    elif op == "su":
      return [(inA[i + self.edge_size] if (i // self.edge_size < (self.edge_size - 1)) else 0) for i in range(self.in_size)]
    elif op == "sd":
      return [(inA[i - self.edge_size] if (i // self.edge_size > 0) else 0) for i in range(self.in_size)]
    elif op == "in":
      return d_in
    elif op == "0":
      return [0] * self.in_size
    elif op == "1":
      return [1] * self.in_size
    else:
      raise ValueError()


def gen_classifier(tree):
  def tree_eval(testcase):
    d_out = tree.compute(testcase)
    return [(0 if v < 0.5 else 1) for v in d_out]
  
  return (lambda testcase : tree_eval(testcase))


def children_per_op(op):
  if op == "add":
    return 2
  elif op == "sub":
    return 2
  elif op == "mul":
    return 2
  elif op == "thr":
    return 1
  elif op == "sl":
    return 1
  elif op == "sr":
    return 1
  elif op == "su":
    return 1
  elif op == "sd":
    return 1
  elif op == "in":
    return 0
  elif op == "0":
    return 0
  elif op == "1":
    return 0
  else:
    raise ValueError()


def build_random_tree(rem_depth=20):
  p_2, p_1, p_0 = 0.4, 0.3, 0.34
  op_pool_2 = ["add", "sub", "mul"]
  op_pool_1 = ["thr", "sl", "sr", "su", "sd", "sl", "sr", "su", "sd"]
  op_pool_0 = ["in", "0", "1"]
  if rem_depth > 0:
    x = random()
    if x < p_2:
      op = choice(op_pool_2)
    elif x < p_2 + p_1:
      op = choice(op_pool_1)
    else:
      op = choice(op_pool_0)
  else:
    op = choice(op_pool_0)
  tree = [op]
  for i in range(children_per_op(op)):
    tree.append(build_random_tree(rem_depth-1))
  return tree


def test():
  t = build_random_tree()
  tr = Tree(25, t)
  print(tr.compute([0] * 25))


#test()

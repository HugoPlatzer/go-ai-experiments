#!/usr/bin/python3

from random import random, randint
from math import tanh

class NN():
  def __init__(self, in_size, tiles, activation="relu", initializer="zero"):
    activations = {"linear" : (lambda x : x),
                   "relu" : (lambda x : max(x, 0.0)),
                   "tanh" : tanh}
    initializers = {"zero" : (lambda : 0.0),
                    "random" : (lambda : random() - 0.5)}
    self.in_size = in_size
    self.edge_size = int(self.in_size**0.5)
    self.tiles = tiles
    self.compute_offsets()
    self.weights = [initializers[initializer]() for i in range(self.num_weights)]
    self.activation = activations[activation]
  
  def compute_offsets(self):
    self.num_weights = 0
    self.bias_ranges = []
    self.mul_ranges = []
    for i in range(len(self.tiles)):
      bias_size = self.in_size
      mul_size = (self.tiles[i] * 2 + 1)**2 * self.in_size
      self.bias_ranges.append((self.num_weights, self.num_weights + bias_size))
      self.num_weights += bias_size
      self.mul_ranges.append((self.num_weights, self.num_weights + mul_size))
      self.num_weights += mul_size
  
  def compute(self, d_in):
    for i in range(len(self.tiles)):
      bias_range = self.bias_ranges[i]
      mul_range = self.mul_ranges[i]
      mul_weights = self.weights[mul_range[0]:mul_range[1]]
      tile_size = self.tiles[i]
      d_out = self.weights[bias_range[0]:bias_range[1]]
      for p in range(len(d_in)):
        row, col = p // self.edge_size, p % self.edge_size
        for i in range(2 * tile_size + 1):
          for j in range(2 * tile_size + 1):
            orow = row - tile_size + i
            ocol = col - tile_size + j
            if orow < 0 or orow >= self.edge_size or ocol < 0 or ocol >= self.edge_size:
              continue
            op = orow * self.edge_size + ocol
            weight = mul_weights[i * tile_size + j]
            d_out[op] += weight * d_in[p]
      d_out = [self.activation(v) for v in d_out]
      d_in = d_out
    return d_in
  
  def clone(self):
    cloned = NN(self.in_size, self.tiles)
    cloned.weights = self.weights[:]
    cloned.activation = self.activation
    return cloned
  
  def mutate(self, n, k):
    for i in range(n):
      p = randint(0, len(self.weights) - 1)
      v = (random() - 0.5) * k
      self.weights[p] += v


def test_nn():
  net = NN(25, [3, 1], initializer="random", activation="linear")
  print(len(net.weights))
  d_in = [float(x) for x in range(25)]
  print(net.compute(d_in))


def gen_classifier(nn):
  def nn_eval(testcase):
    d_out = nn.compute(testcase)
    #return [(0 if v < 0.5 else 1) for v in d_out]
    return d_out
  
  return (lambda testcase : nn_eval(testcase))

def mutated(nn, n=100, k=1.0):
  clone = nn.clone()
  clone.mutate(n, k)
  return clone

#test_nn()

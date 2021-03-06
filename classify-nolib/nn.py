#!/usr/bin/python3

from random import random, randint
from math import tanh

class NN():
  def __init__(self, sizes, activation="relu", initializer="zero"):
    activations = {"linear" : (lambda x : x),
                   "relu" : (lambda x : max(x, 0.0)),
                   "tanh" : tanh}
    initializers = {"zero" : (lambda : 0.0),
                    "random" : (lambda : random() - 0.5)}
    self.sizes = sizes
    self.compute_offsets()
    self.weights = [initializers[initializer]() for i in range(self.num_weights)]
    self.activation = activations[activation]
  
  def compute_offsets(self):
    self.num_weights = 0
    self.bias_ranges = []
    self.mul_ranges = []
    for i in range(1, len(self.sizes)):
      size_now, size_before = self.sizes[i], self.sizes[i - 1]
      bias_size = size_now
      mul_size = size_now * size_before
      self.bias_ranges.append((self.num_weights, self.num_weights + bias_size))
      self.num_weights += bias_size
      self.mul_ranges.append((self.num_weights, self.num_weights + mul_size))
      self.num_weights += mul_size
  
  def compute(self, d_in):
    for i in range(1, len(self.sizes)):
      bias_range = self.bias_ranges[i - 1]
      mul_range = self.mul_ranges[i - 1]
      mul_weights = self.weights[mul_range[0]:mul_range[1]]
      d_out = self.weights[bias_range[0]:bias_range[1]]
      for i in range(len(d_out)):
        for j in range(len(d_in)):
          d_out[i] += d_in[j] * mul_weights[i * len(d_in) + j]
      d_out = [self.activation(v) for v in d_out]
      d_in = d_out
    return d_in
  
  def clone(self):
    cloned = NN(self.sizes)
    cloned.weights = self.weights[:]
    cloned.activation = self.activation
    return cloned
  
  def mutate(self, n, k):
    for i in range(n):
      p = randint(0, len(self.weights) - 1)
      v = (random() - 0.5) * k
      self.weights[p] += v


def test_nn():
  nn = NN([2, 2, 1])
  nn.weights = [0, -1, 1, 1, 1, 1, 0, 1, -2]
  print(nn.weights)
  print(nn.bias_ranges)
  print(nn.mul_ranges)
  print(nn.compute([0.0, 0.0]))
  print(nn.compute([0.0, 1.0]))
  print(nn.compute([1.0, 0.0]))
  print(nn.compute([1.0, 1.0]))


def gen_classifier(nn):
  def nn_eval(testcase):
    d_out = nn.compute(testcase)
    return d_out
  
  return (lambda testcase : nn_eval(testcase))

def mutated(nn, n=100, k=1.0):
  clone = nn.clone()
  clone.mutate(n, k)
  return clone

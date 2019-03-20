#!/usr/bin/python3

from random import random, randint

class NN():
  def __init__(self, sizes, activation="relu", initializer="zero"):
    activations = {"linear" : (lambda x : x),
                   "relu" : (lambda x : max(x, 0.0))}
    initializers = {"zero" : (lambda : 0.0)}
    self.sizes = sizes
    self.compute_offsets()
    self.weights = [initializers[initializer]() for i in range(self.num_weights)]
    self.activation = activations[activation]
  
  def compute_offsets(self):
    self.num_weights = 0
    self.ranges_bias = []
    self.ranges_mul = []
    for i in range(1, len(self.sizes)):
      size_now, size_before = self.sizes[i], self.sizes[i - 1]
      bias_size = size_now
      mul_size = size_now * size_before
      self.ranges_bias.append((self.num_weights, self.num_weights + bias_size))
      self.num_weights += bias_size
      self.ranges_mul.append((self.num_weights, self.num_weights + mul_size))
      self.num_weights += mul_size
  
  def compute(self, d_in):
    for i in range(1, len(self.sizes)):
      bias_range = self.bias_ranges[i - 1]
      mul_range = self.mul_ranges[i - 1]
      d_out = 
  
  def clone(self):
    cloned = NN(sizes, self.activation)
    cloned.weights = self.weights[:]
    return cloned
  
  def mutate(self, n, k):
    for i in range(n):
      p = randint(0, len(self.weights) - 1)
      v = (random() - 0.5) * k
      self.weights[p] += v


nn = NN([4, 2])
print(nn.weights)
print(nn.ranges_bias)
print(nn.ranges_mul)

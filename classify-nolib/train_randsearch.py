#!/usr/bin/python3

import test, nn_tiled as nn, tree

def train_randsearch(generator, evaluator, generations=10000, verbose=0):
  base = generator()
  score = evaluator(base)
  if verbose >= 1:
    print("base score={}".format(score))
    print(base)
  for i in range(1, generations + 1):
    candidate = generator()
    candidate_score = evaluator(candidate)
    if candidate_score > score:
      base = candidate
      score = candidate_score
      if verbose >= 1:
        print("gen {} score={}".format(i, score))
        print(base)
  return classifier


def test_train_nn():
  testcases = test.create_testcases(5, 1000)
  dummy_score = test.test_classifier(test.dummy_classifier, testcases)
  print("dummy_score = {}".format(dummy_score))
  generator = lambda : nn.NN(25, [1], initializer="random", activation = "relu")
  evaluator = lambda net : test.test_classifier_soft(nn.gen_classifier(net), testcases)
  train_randsearch(generator, evaluator, verbose=1)


def test_train_tree():
  testcases = test.create_testcases(5, 1000)
  dummy_score = test.test_classifier_soft(test.dummy_classifier, testcases)
  print("dummy_score = {}".format(dummy_score))
  generator = lambda : tree.build_random_tree()
  evaluator = lambda t : test.test_classifier_soft(tree.gen_classifier(tree.Tree(25, t)), testcases)
  train_randsearch(generator, evaluator, verbose=1)

test_train_nn()

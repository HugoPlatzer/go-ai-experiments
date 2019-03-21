#!/usr/bin/python3

import test, nn, nn_tiled, pickle

def train_mutate(base, evaluator, evaluator_test, gen_classifier,
                 mutator, generations=10000000, verbose=0):
  classifier = gen_classifier(base)
  score = evaluator(classifier)
  if verbose >= 1:
    score_test = evaluator_test(classifier)
    print("base score={} score_t={}".format(score, score_test))
  for i in range(1, generations + 1):
    candidate = mutator(base)
    candidate_classifier = gen_classifier(candidate)
    candidate_score = evaluator(candidate_classifier)
    if candidate_score > score:
      base = candidate
      classifier = candidate_classifier
      score = candidate_score
      with open("obj", "wb") as f:
        pickle.dump(base, f)
      if verbose >= 1:
        score_test = evaluator_test(classifier)
        print("gen {} score={} score_t={}".format(i, score, score_test))
  return base


def test_train():
  traincases = test.create_testcases(5, 10000)
  testcases = test.create_testcases(5, 1000)
  dummy_score_soft = test.test_classifier_soft(test.dummy_classifier, testcases)
  dummy_score = test.test_classifier(test.dummy_classifier, testcases)
  print("dummy_score_soft={} dummy_score = {}".format(dummy_score_soft, dummy_score))
  try:
    with open("obj", "rb") as f:
      base = pickle.load(f)
  except Exception:
    base = nn_tiled.NN(25, [1] * 5, initializer="random", activation="tanh")
  #base = nn.NN([25, 25], initializer="random", activation="tanh")
  evaluator = lambda classifier : test.test_classifier_soft(classifier, traincases)
  evaluator_test = lambda classifier : test.test_classifier(classifier, testcases)
  gen_classifier = nn.gen_classifier
  mutator = lambda net : nn.mutated(net, 10, 1.0)
  train_mutate(base, evaluator, evaluator_test, gen_classifier, mutator, verbose=1)

test_train()

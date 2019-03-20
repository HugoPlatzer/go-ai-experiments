#!/usr/bin/python3

from random import choice

def test_classifier(classifier, testcases):
  results = [classifier(tc[0]) for tc in testcases]
  num_correct = sum(1 for i in range(len(results)) if results[i] == testcases[i][1])
  return num_correct / float(len(testcases))


def dummy_classifier(b):
  return [0] * len(b)


def test_dummy_classifier():
  testcases = create_testcases(5, 1000)
  print_board(testcases[0][0])
  print_board(testcases[0][1])
  score = test_classifier(dummy_classifier, testcases)
  print(score)


def create_testcases(boardsize, n):
  return [create_testcase(boardsize) for i in range(n)]


def create_testcase(boardsize):
  s = [-1] * 5 + [1] * 5 + [0] * 1 
  b = [choice(s) for i in range(boardsize**2)]
  o = identify_nolib(b)
  return (b, o)


def identify_nolib(b):
  return [identify_nolib_point(b, i) for i in range(len(b))]


def identify_nolib_point(b, p):
  if b[p] == 0:
    return 0
  size = int(len(b)**0.5)
  point = (p // size, p % size)
  visited = set([point])
  stack = [point]
  while len(stack) > 0:
    point = stack.pop()
    candidates = [(point[0] - 1, point[1]), (point[0] + 1, point[1]),
                  (point[0], point[1] - 1), (point[0], point[1] + 1)]
    candidates = [c for c in candidates if (0 <= c[0] < size and
                                            0 <= c[1] < size)]
    cand_points = [(c[0] * size + c[1]) for c in candidates]
    for i in range(len(candidates)):
      if b[cand_points[i]] == 0:
        return 0
      if b[cand_points[i]] == b[p] and candidates[i] not in visited:
        stack.append(candidates[i])
        visited.add(point)
  return 1


def print_board(b):
  mapping = {-1 : "0", 0 : ".", 1 : "X"}
  size = int(len(b)**0.5)
  print()
  for i in range(size):
    print("".join(mapping[b[p]] for p in range(i * size, (i + 1) * size)))
  print()


test_dummy_classifier()

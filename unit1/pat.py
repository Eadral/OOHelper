import os
from sympy import Symbol, sin, cos, simplify
import sys
from unit1.utils import *
from time import time

x = Symbol("x")


def pat(input, output, mainClass, package):
    start = time()
    os.system('call run.cmd "{}" {}{}'.format(input, package, mainClass))
    end = time()
    duration = end - start
    # print(duration, input)
    if duration > 0.9:
        sys.stderr.write("\nWarning: TLE {} at {}\n".format(duration, input))
    test_output_path = os.path.join("temp", "output.txt")
    compare(output, test_output_path)


def compare(target_path, subject_path):
    target = open(target_path).readlines()
    subject = open(subject_path).readlines()
    if len(subject) == 0:
        raise RuntimeError("WA in {} \n\t No output".format(target_path))
    while target[-1] == "\n":
        del target[-1]
    while subject[-1] == "\n":
        del subject[-1]
    target = target[:1]
    subject = subject[:1]
    n_lines = min(len(target), len(subject))
    for i in range(n_lines):
        if not equal(target_path.split(".")[0] + ".in", target[i].rstrip(), subject[i].rstrip()):
            raise RuntimeError("WA in {} \n\t Line {} : except {} while found {}"
                               .format(target_path, i, target[i], subject[i]))
    if len(target) > len(subject):
        raise RuntimeError(
            "WA in {} \n\t EOF: except {} while found NOTHING".format(target_path, target[len(subject) + 1]))
    if len(target) < len(subject):
        raise RuntimeError(
            "WA in {} \n\t EOF: except NOTHING while found {}".format(target_path, subject[len(target) + 1]))

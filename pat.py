import os
from sympy import Symbol

x = Symbol("x")

def pat(input, output, mainClass):
    os.system('call run.cmd "{}" {}'.format(input, mainClass))

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
    n_lines = min(len(target), len(subject))
    for i in range(n_lines):
        if not equal(target[i].rstrip(), subject[i].rstrip()):
            raise RuntimeError("WA in {} \n\t Line {} : except {} while found {}"
                               .format(target_path, i, target[i], subject[i]))
    if len(target) > len(subject):
        raise RuntimeError(
            "WA in {} \n\t EOF: except {} while found NOTHING".format(target_path, target[len(subject) + 1]))
    if len(target) < len(subject):
        raise RuntimeError(
            "WA in {} \n\t EOF: except NOTHING while found {}".format(target_path, subject[len(target) + 1]))

def equal(target, subject):

    return target == subject or eval("{} == {}".format(target, subject))


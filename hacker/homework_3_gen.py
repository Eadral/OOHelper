from utils import *
import random
import subprocess
import os
from sympy import Symbol, sin, cos, diff, trigsimp
import progressbar
import time
from hacker.generate import generator

x = Symbol("x")

n_term = 3
n_factor = 3
range_expo = 10
range_coeff = 10

TIMES = 1000


def hack(project_dir, none=None, main="Main", package="", main_path="."):
    precompile(project_dir, main, main_path)
    # print("Testing... Please wait.")
    with progressbar.ProgressBar(max_value=TIMES) as bar:
        for i in range(TIMES):
            corr, expr, subj = auto_test(main, package)
            if not corr:
                raise RuntimeError("Err: {}\n {}".format(expr.replace(" ", ""), subj))
            bar.update(i)


def auto_test(mainClass, package):
    positive = True
    if random.random() < 0.5:
        # expr = gen_positive(random.randint(1, n_term))
        expr = generator()
    else:
        expr = gen_negative(random.randint(1, n_term))
        positive = False
    open("temp\\input.txt", "w").writelines(expr)
    os.system('call run.cmd "{}" {}{}'.format("input.txt", package, mainClass))
    subj = open("temp\\output.txt").readlines()[0]
    return test("temp\\input.txt", expr, subj, positive), expr, subj


def gen_term_positive(n=n_factor):
    term = ""
    if n >= 2 and random.random() < 0.4:
        term += "{}".format(random.choice(["-", "+"]))
        n -= 1
    terms = []
    for i in range(n):
        terms.append("{}".format(gen_factor()))
    term += "*".join(terms)
    return term


def gen_positive(n=n_term):
    expr = ""
    for i in range(n):
        expr += "{}{}".format(
            random.choice(["-", "+"]),
            gen_term_positive(random.randrange(1, n_factor))
        )
    return expr


global n_defect


def try_defect(defect, normal):
    global n_defect
    if n_defect == 0:
        return normal
    if random.random() < 0.1:
        n_defect -= 1
        return defect


def gen_negative(n=n_term):
    global n_defect
    n_defect = 1
    expr = ""
    for i in range(n):
        expr += "{}{}".format(
            random.choice(["-", "+"]),
            gen_term_negative(random.randrange(1, n_factor))
        )
    if n_defect > 0:
        expr += random.choice(["@", "\f", "\v"])
    return expr


def gen_term_negative(n=n_factor):
    global n_defect
    term = ""
    if n >= 2 and random.random() < 0.4:
        term += "{}".format(random.choice(["-", "+"]))
        n -= 1
    terms = []
    for i in range(n):
        terms.append("{}".format(gen_factor()))
    term += "*".join(terms)
    return term

global times
times = 0
def gen_factor():
    global times
    if times <= 3 and random.random() < 0.5:
        times += 1
        inside_factor = gen_factor()
        inside_expr = gen_positive()
    else:
        inside_factor = "x"
        inside_expr = "(x)"

    return random.choice([
        "{}".format(random_range(range_coeff)),
        "x^{}".format(random_range(range_expo)),
        "sin({})^{}".format(inside_factor, random_range(range_expo)),
        "cos({})^{}".format(inside_factor, random_range(range_expo)),
        "({})".format(inside_expr),
    ])


def test(name, expr, subject, positive=True):
    if positive:
        expr = expr.replace("^", "**")
        target = diff(eval(expr), x)
        target = str(target).replace("**", "^")
    else:
        target = "WRONG FORMAT!"
    return equal(name, target, subject, check_length=False)


if __name__ == "__main__":
    print(gen_positive())

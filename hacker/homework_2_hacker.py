from utils import *
import random
import subprocess
import os
from sympy import Symbol, sin, cos, diff
import progressbar
x = Symbol("x")

n_term = 10
n_factor = 10
range_expo = 5
range_coeff = 10


def hack(project_dir, none=None, main="Main", package=""):
    precompile(project_dir, main)
    # print("Testing... Please wait.")
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    i = 0
    while True:
        corr, expr, subj = auto_test(main, package)
        if not corr:
            raise RuntimeError("Err: {}\n {}".format(expr.replace(" ", ""), subj))
        bar.update(i)
        i += 1


def auto_test(mainClass, package):
    expr = gen(random.randint(1, n_term))
    open("temp\\input.txt", "w").writelines(expr)
    os.system('call run.cmd "{}" {}{}'.format("input.txt", package, mainClass))
    subj = open("temp\\output.txt").readlines()[0]
    return test(expr, subj), expr, subj


def gen_term(n=n_factor):
    term = ""
    if n >= 2 and random.random() < 0.4:
        term += "{}".format(random.choice(["-", "+"]))
        n -= 1
    terms = []
    for i in range(n):
        terms.append("{}".format(random.choice([
            "x^{}".format(random_range(range_expo)),
            "sin(x)^{}".format(random_range(range_expo)),
            "cos(x)^{}".format(random_range(range_expo)),
            "{}".format(random_range(range_coeff)),
        ])))
    term += "*".join(terms)
    return term



def gen(n=n_term):
    expr = ""
    for i in range(n):
        expr += "{}{}".format(
            random.choice(["-", "+"]),
            gen_term(random.randrange(1, n_factor))
        )
    return expr


def test(expr, subject):
    expr = expr.replace("^", "**")
    target = diff(eval(expr), x)
    target = str(target).replace("**", "^")
    return equal(target, subject, check_length=False)


if __name__ == "__main__":
    # print(gen_term())
    # print(split("7488*x^-97+1302*x^-94-4320*x^-81+6144*x^-65-3416*x^-62+48*x^7-75*x^14+864*x^15+960*x^39+4420*x^64+952*x^67"))
    # hack(r"C:\Study\OO\homework\oo_course_2019_16191051_homework_1", "Main", "")
    # hack(r"C:\Study\OO\others\homework_1\ly", "Executive", "math.qiudao.")
    # hack(r"C:\Study\OO\others\homework_1\hjw", main="WorkBegin", package="work.")
    hack(r"C:\Study\OO\homework\oo_course_2019_16191051_homework_2", [], "Main", "")


    # hack(r"C:\Study\OO\others\homework_1\Saber", [], "Main")
    # hack(r"C:\Study\OO\others\homework_1\Lancer", ["long_expo", "stack_overflow"], "Main")  # unhack
    # hack(r"C:\Study\OO\others\homework_1\Archer", ["special_space"], "PolyCal")
    # hack(r"C:\Study\OO\others\homework_1\Rider", [], "Main")
    # hack(r"C:\Study\OO\others\homework_1\Caster", ["auto_0"], "Main") # checked
    # hack(r"C:\Study\OO\others\homework_1\Assassin", [], "Solution")
    # hack(r"C:\Study\OO\others\homework_1\Alterego", ["sign_first"], "PolyBuild")

from utils import *
import random
import subprocess
import os

n_term = 2000
range_expo = 100
len_coeff = 100


def hack(project_dir, main="Main"):
    precompile(project_dir, main)
    while True:
        corr, expr, subj = auto_test()
        if corr:
            print("Pass: {}, {}".format(expr, subj))
        else:
            raise RuntimeError("Err: {}, {}".format(expr, subj))


def auto_test():
    expr = gen(n_term)
    open("temp\\input.txt", "w").writelines(expr)
    os.system('call run.cmd "{}"'.format("input.txt"))
    subj = split(open("temp\\output.txt").readlines()[0])
    return test(expr, subj), expr, subj


def gen_term():
    if random.random() < 0.2:
        return " {} {} ".format(random.choice(["-", "+"]), random_bigint(len_coeff))
    else:
        return " {} {} x {} ".format(random.choice(["-", "+"]),
                                     random.choice([" {} * ".format(random_bigint(len_coeff)), "+", "-", " "]),
                                     random.choice([" ^ {} ".format(random.randint(-range_expo, range_expo)), " "]),
                                     )


def gen(n=10):
    expr = gen_term()[2:]
    for i in range(n):
        expr += gen_term()
    return expr





def test(expr, subject):
    open("test.wl", "w").writelines("Print[Dt[{}, x] == {}]".format(expr, subject))
    os.system("wolframscript -file test.wl > test_out.txt")
    return open("test_out.txt").readlines()[0] == "True\n"


if __name__ == "__main__":
    # print(gen_term())
    # print(split("7488*x^-97+1302*x^-94-4320*x^-81+6144*x^-65-3416*x^-62+48*x^7-75*x^14+864*x^15+960*x^39+4420*x^64+952*x^67"))
    hack(r"C:\Study\OO\homework\homework_1")

import os
import random


def get_paths_recursively(folder):
    paths = []
    files = os.listdir(folder)
    for file in files:
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            paths += get_paths_recursively(path)
        else:
            paths.append(path)
    return paths


def random_bigint(len=100):
    return random.randint(-10 ** len + 1, 10 ** len - 1)


def random_int():
    return random.randint(-2 ** 32, 2 ** 32 - 1)


def random_space():
    return ' ' * random.randint(0, 10)



def precompile(project_dir, main):
    class_path = os.path.join("temp", "{}.class".format(main))
    if os.path.exists(class_path):
        os.remove(class_path)
    output_path = os.path.join("temp", "output.txt")
    if os.path.exists(output_path):
        os.remove(output_path)
    src_path = os.path.join(project_dir, "src", "{}.java".format(main))
    compile_source(src_path)


def compile_source(src):
    os.system('javac "{}"  -cp "{}" -d {}'.format(src, os.path.join(src, ".."), "temp\\"))


def split(expr):
    return "".join(list(map(lambda x: " {} ".format(x) if x in ["*", "x", "^", "+", "-"] else x, expr)))


if __name__ == "__main__":
    print(split("-x-9*x-x+-3+-3*x^-4+-x^2-5*x^0+-4*x+-x+-x^1+-x+-8*x^5+8*x^-4--x^-5--8*x--x+-x^-4-7*x^5+-x+0*x^-1-x-3++x^0-9*x^0+5+x+-2+x+-5*x^3+x^-5--x^2+-1*x^-4+-6*x^-3++x^-1--x-1+-4+5+x+-x^0++x^4-2-+x+6*x^0-1-+x^-5--7*x++x-6++x--8*x^-3+9*x^5--x^5-+x--1*x+5*x+x^3+-x+2++x^-4+6*x+5-7*x^1+x+7-x^-4+-4*x^1-+x^1+x++x^5++x+-x+-x^5--9*x-x^-5+8*x^1+-x^-4-+x^5+6-x+x^1-+x^-2-x-3*x^2+-7--x^5++x-x--6*x^-5+-2*x-+x++x--x^-5-x+x-+x^-1++x^-1-x--x-+x++x^4--5*x^3+-1*x-+x-2*x-2*x^-5+7*x^-1-+x^2-8*x^1+2--x^4--8--6-6*x++x-5*x^-1-8+-x^5-6*x^-1-+x^-5--x--x^1++x^3-x^-3--5*x+4--x^-4+x^-3+-9*x-+x^-1+-1*x+0--5-4--9--x-7-3-x^4+-2*x^1+2*x+-x^-3+-6+x+-5-7-+x^3-+x^-4+6*x^0-x+x^3--x^-1+-x^2+1*x^0++x+x^-4+9*x^3+x^-2-x-x--1*x^1+-6+x^-2+3*x-+x-x-+x+x++x+-x^-1-x^1+x-x-9*x++x-x-2--x^5+5*x^4--x-+x++x^-4-5*x^1--7*x+-x^1-6-+x^5+x^3+5*x+-1*x^-2-x++x-7+2--x^3-+x^1+-x--7-+x^4--3*x+x^0"))
    print(split("4*x^-2-16*x^-5-3*x^-4-20*x^-6-6-10*x+39*x^2+24*x^3-30*x^4"))

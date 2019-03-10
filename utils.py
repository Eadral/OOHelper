import os
import random
from sympy import Symbol, sin, cos, simplify
import sys
x = Symbol("x")

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
    src_path = os.path.join(project_dir, "src")
    compile_source(src_path)


def compile_source(src):
    # src_path = os.path.join(project_dir, "src", "*.java")
    here = os.getcwd()
    os.chdir(src)
    cmd = 'javac -encoding UTF-8 *.java -d {}'.format(os.path.join(here, "temp"))
    print(cmd)
    os.system(cmd)
    os.chdir(here)


def split(expr):
    return "".join(list(map(lambda x: " {} ".format(x) if x in ["*", "x", "^", "+", "-"] else x, expr)))


def equal(target, subject):
    if target == subject:
        return True
    try:
        target = target.replace(" ", "")
        if eval("simplify({}) == simplify({})".format(target.replace("^", "**"), subject.replace("^", "**"))) is True:
            if len(subject) > len(target):
                sys.stderr.write("\nWarning: Equal but longer!! \n\t{}\n\t{}\n".format(target, subject))
            return True
    except:
        return False
    return False


if __name__ == "__main__":
    print(split("4*x^-2-16*x^-5-3*x^-4-20*x^-6-6-10*x+39*x^2+24*x^3-30*x^4"))

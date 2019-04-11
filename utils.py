import os
import random
import shutil
import sys
import re


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


def datacheck(test_data_in):
    # print("\033[1;33mDatacheck unavailable now.\033[0m")
    # return 65535, 65535
    result = os.popen(r"{} -i {}".format(os.path.join("test_data", "datacheck.exe"), test_data_in))
    output = result.read()
    basetime = re.search(r'base time is (\d+)', output, re.M)
    maxtime = re.search(r'max time is (\d+)', output, re.M)
    if basetime is None:
        print("\033[1;31mIllegal input: {}\033[0m".format(test_data_in))
        return 0, 0
    return int(basetime.group(1)), int(maxtime.group(1))


def precompile(project_dir, main, main_path, jar):
    if os.path.exists("temp"):
        shutil.rmtree("temp")
        os.mkdir("temp")
    class_path = os.path.join("temp", "{}.class".format(main))
    if os.path.exists(class_path):
        os.remove(class_path)
    output_path = os.path.join("temp", "output.txt")
    if os.path.exists(output_path):
        os.remove(output_path)
    src_path = os.path.join(project_dir, "src")
    compile_source(src_path, main_path, jar)


def compile_source(src, main_path=".", jar=".;"):
    # src_path = os.path.join(project_dir, "src", "*.java")
    here = os.getcwd()
    os.chdir(src)
    cmd = 'javac -encoding UTF-8 {} -d {} -cp {}'.format(os.path.join(main_path, "*.java"), os.path.join(here, "temp"),
                                                         jar)
    print(cmd)
    os.system(cmd)
    os.chdir(here)

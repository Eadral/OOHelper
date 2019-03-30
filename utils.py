import os
import random
import sys

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


def precompile(project_dir, main, main_path, jar):
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
    cmd = 'javac -encoding UTF-8 {} -d {} -cp {}'.format(os.path.join(main_path, "*.java"), os.path.join(here, "temp"), jar)
    print(cmd)
    os.system(cmd)
    os.chdir(here)


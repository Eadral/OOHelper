import os
from config import Config
from utils import *
from pat import pat


def test(project_dir):
    class_path = os.path.join("temp", "Main.class")
    if os.path.exists(class_path):
        os.remove(class_path)
    output_path = os.path.join("temp", "output.txt")
    if os.path.exists(output_path):
        os.remove(output_path)

    src_path = os.path.join(project_dir, "src", "Main.java")
    compile_source(src_path)
    test_data_folder = os.path.join(project_dir, "test_data")
    test_data_paths = get_paths_recursively(test_data_folder)
    test_data_in_paths = list(filter(lambda path: path.split('.')[-1] == "in", test_data_paths))
    for test_data_in in test_data_in_paths:
        test_data_out = test_data_in.split('.')[0] + ".out"
        pat(test_data_in, test_data_out)

    print("AC {}/{}".format(len(test_data_in_paths), len(test_data_in_paths)))


def compile_source(src):
    os.system('javac "{}" -d {}'.format(src, "temp\\"))


if __name__ == "__main__":
    test(r"C:\Study\OO\pre\A+B Problem I")
    test(r"C:\Study\OO\pre\A+B Problem II")
    test(r"C:\Study\OO\pre\A+B Problem III")
    test(r"C:\Study\OO\pre\A+B Problem IV")

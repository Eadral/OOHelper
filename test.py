from utils import *
from pat import pat
from utils import precompile
# import progressbar
import time


def test(jar, test_data_folder, project_dir, ignores=None, main="Main", package="", main_path="."):
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if ignores is None:
        ignores = []

    precompile(project_dir, main, main_path, jar)
    # print("Testing... Please wait.")
    # test_data_folder = os.path.join(project_dir, "test_data")
    test_data_paths = get_paths_recursively(test_data_folder)
    test_data_in_paths = list(filter(lambda path: path.split('.')[-1] == "in", test_data_paths))
    pass_num = 0

    for i, test_data_in in enumerate(test_data_in_paths):
        if test_data_in.split("\\")[-1].split(".")[0] in ignores:
            continue
        pat(test_data_in, package + main, jar)
        pass_num += 1



    print("AC {}/{}".format(pass_num, len(test_data_in_paths)))



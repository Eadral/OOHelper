from utils import *
from pat import pat
from utils import precompile
import progressbar
import time


def test(test_data_folder, project_dir, ignores=None, main="Main", package="", main_path="."):
    if ignores is None:
        ignores = []

    precompile(project_dir, main, main_path)
    # print("Testing... Please wait.")
    # test_data_folder = os.path.join(project_dir, "test_data")
    test_data_paths = get_paths_recursively(test_data_folder)
    test_data_in_paths = list(filter(lambda path: path.split('.')[-1] == "in", test_data_paths))
    pass_num = 0
    with progressbar.ProgressBar(max_value=len(test_data_in_paths)) as bar:
        for i, test_data_in in enumerate(test_data_in_paths):
            print(test_data_in)
            if test_data_in.split("\\")[-1].split(".")[0] in ignores:
                continue
            test_data_out = test_data_in.split('.')[0] + ".out"
            pat(test_data_in, test_data_out, main, package)
            pass_num += 1
            bar.update(i)

    # print("AC {}/{}".format(pass_num, len(test_data_in_paths)))

from utils import *
from pat import pat
from utils import precompile
# import progressbar
import time
from concurrent.futures import ThreadPoolExecutor

failed = []
def test(timeout, jar, test_data_folder, project_dir, ignores=None, main="Main", package="", main_path="."):
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

    with ThreadPoolExecutor(5) as executor:
        for i, test_data_in in enumerate(test_data_in_paths):
            if test_data_in.split("\\")[-1].split(".")[0] in ignores:
                continue
            # executor.submit(pat_thread, test_data_in, package + main, jar)

            if pat(test_data_in, package + main, jar, timeout):
                pass_num += 1
                print("Passed: {}".format(test_data_in))


    print("AC {}/{}".format(pass_num, len(test_data_in_paths)))

    # print(failed)

# def pat_thread(test_data_in, class_path, jar):
#     global failed
#     result = pat(test_data_in, class_path, jar)
#     if not result:
#         failed.append(test_data_in)

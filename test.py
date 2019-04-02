from utils import *
from pat import pat
from utils import precompile
# import progressbar
import time
from concurrent.futures import ThreadPoolExecutor, wait

failed = []
pass_num = 0


def test_single(n_thread, times, jar, test_file, project_dir, ignores=None, main="Main", package="", main_path="."):
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if ignores is None:
        ignores = []

    precompile(project_dir, main, main_path, jar)
    # print("Testing... Please wait.")
    # test_data_folder = os.path.join(project_dir, "test_data")

    p_list = []
    with ThreadPoolExecutor(n_thread) as executor:
        for i in range(times):
            child = executor.submit(pat_thread, test_file, package + main, jar)
            p_list.append(child)
            # if pat(test_data_in, package + main, jar, timeout):
            #     pass_num += 1
            #     print("Passed: {}".format(test_data_in))
    wait(p_list)
    # for p in p_list:
    #     print(p.done())
    #
    time.sleep(0.01)
    global pass_num

    if len(failed) != 0:
        print("\033[1;33mAC {}/{}\033[0m".format(pass_num, times))
        print("\033[1;31mFailed:", failed)
    else:
        print("\033[1;32mAC {}/{}\033[0m".format(pass_num, times))


def test(n_thread, jar, test_data_folder, project_dir, ignores=None, main="Main", package="", main_path="."):
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if ignores is None:
        ignores = []

    precompile(project_dir, main, main_path, jar)
    # print("Testing... Please wait.")
    # test_data_folder = os.path.join(project_dir, "test_data")
    test_data_paths = get_paths_recursively(test_data_folder)
    test_data_in_paths = list(filter(lambda path: path.split('.')[-1] == "in", test_data_paths))

    p_list = []
    with ThreadPoolExecutor(n_thread) as executor:
        for i, test_data_in in enumerate(test_data_in_paths):
            if test_data_in.split("\\")[-1].split(".")[0] in ignores:
                continue
            child = executor.submit(pat_thread, test_data_in, package + main, jar)
            p_list.append(child)
            # if pat(test_data_in, package + main, jar, timeout):
            #     pass_num += 1
            #     print("Passed: {}".format(test_data_in))
    wait(p_list)
    # for p in p_list:
    #     print(p.done())
    #
    time.sleep(0.01)
    global pass_num

    if len(failed) != 0:
        print("\033[1;33mAC {}/{}\033[0m".format(pass_num, len(test_data_in_paths)))
        print("\033[1;31mFailed:", failed)
    else:
        print("\033[1;32mAC {}/{}\033[0m".format(pass_num, len(test_data_in_paths)))


def pat_thread(test_data_in, class_path, jar):
    global failed
    global pass_num
    print("\033[1;37mTesting: {}\033[0m".format(test_data_in))
    result = pat(test_data_in, class_path, jar)
    if result is True:
        pass_num += 1
    else:
        failed.append(test_data_in)



# from test import test, test_single
# import sys
# from macro import *
#
# if __name__ == "__main__":
#     jar = ";".join([
#         r".",
#         r"temp",
#         r"C:\Study\OO\homework\unit2\elevator-input-hw1-1.3-jar-with-dependencies.jar",
#         r"C:\Study\OO\homework\unit2\timable-output-1.0-raw-jar-with-dependencies.jar",
#     ])
#     n_thread = 64  # thread number of evaluator
#     test_data = r"test_data"
#
#     # test_single(n_thread, 1, jar, r"test_data\auto\auto_15541782574642398.in", r"C:\Study\OO\homework\unit2\oo_course_2019_16191051_homework_5", [], "Main", "", ".")
#     test(n_thread, jar, test_data, r"C:\Study\OO\homework\unit2\oo_course_2019_16191051_homework_5", [], "Main", "", ".")
#
#

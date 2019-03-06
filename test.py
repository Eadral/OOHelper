from utils import *
from pat import pat
from utils import precompile


def test(test_data_folder, project_dir, ignores=None, main="Main", package=""):
    if ignores is None:
        ignores = []

    precompile(project_dir, main)

    # test_data_folder = os.path.join(project_dir, "test_data")
    test_data_paths = get_paths_recursively(test_data_folder)
    test_data_in_paths = list(filter(lambda path: path.split('.')[-1] == "in", test_data_paths))
    pass_num = 0
    for test_data_in in test_data_in_paths:
        if test_data_in.split("\\")[-1].split(".")[0] in ignores:
            continue
        test_data_out = test_data_in.split('.')[0] + ".out"
        pat(test_data_in, test_data_out, main, package)
        pass_num += 1

    print("AC {}/{}".format(pass_num, len(test_data_in_paths)))


if __name__ == "__main__":
    # test(r"C:\Study\OO\others\homework_1\ly", [], "Executive", "math.qiudao.")
    # test(r"C:\Study\OO\others\homework_1\hjw", ignores=[], main="WorkBegin", package="work.")
    # test(r"C:\Study\OO\homework\oo_course_2019_16191051_homework_1", [], "Main")

    # test(r"C:\Study\OO\others\homework_1\Saber", [], "Main")
    # test(r"C:\Study\OO\others\homework_1\Lancer", ["long_expo", "stack_overflow"], "Main")
    # test(r"C:\Study\OO\others\homework_1\Archer", ["special_space"], "PolyCal")
    # test(r"C:\Study\OO\others\homework_1\Rider", [], "Main")
    # test(r"C:\Study\OO\others\homework_1\Caster", [], "Main")
    # test(r"C:\Study\OO\others\homework_1\Assassin", [], "Solution")
    test(r"C:\Study\OO\homework\oo_course_2019_16191051_homework_1\test_data", r"C:\Study\OO\others\homework_1\Alterego", ["sign_first"], "PolyBuild")



from test import test
import sys
from macro import *

if __name__ == "__main__":
    jar = ";".join([
        r".",
        r"temp",
        r"C:\Study\OO\homework\unit2\elevator-input-hw1-1.3-jar-with-dependencies.jar",
        r"C:\Study\OO\homework\unit2\timable-output-1.0-raw-jar-with-dependencies.jar",
    ])
    n_thread = 32  # thread number of evaluator
    test_data = r"test_data"


    test(n_thread, jar, test_data, r"C:\Study\OO\homework\unit2\oo_course_2019_16191051_homework_5", [], "Main", "", ".")



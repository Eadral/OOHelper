from test import test
import sys

if __name__ == "__main__":
    test_data = r"C:\Develop\PyCharm\OOHelper\test_data"
    jar = r".;C:\Study\OO\homework\unit2\elevator-input-hw1-1.3-jar-with-dependencies.jar;C:\Study\OO\homework\unit2\timable-output-1.0-raw-jar-with-dependencies.jar "
    timeout = 30  # 200

    test(timeout, jar, test_data, r"C:\Study\OO\homework\unit2\oo_course_2019_16191051_homework_5", [], "Main", "", "")



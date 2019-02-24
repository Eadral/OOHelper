import os
import random

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

def random_bigint():
    return random.randint(-10**100+1, 10**100-1)

def random_int():
    return random.randint(-2**32, 2**32-1)

def random_space():
    return ' ' * random.randint(0, 10)


# test
if __name__ == "__main__":
    print(get_paths_recursively(r"C:\Study\OO\pre\A+B Problem I\test_data"))

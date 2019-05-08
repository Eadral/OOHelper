import random
from copy import copy
import os

random_int_poll = [2147483647, -2147483648, 2147483646, -2147483647, -1, 0, 1]
for i in range(240):
    random_int_poll.append(random.randint(-2147483648, 2147483647))

global n
n = 1
ID_RANGE = n
LENGTH = 200


def get_id():
    global n
    return random.randint(1, n)


def get_node():
    return random.choice(random_int_poll)


def get_path():
    return random.choice(path_poll)


def new_path():
    path = ""
    for i in range(LENGTH):
        path += "{} ".format(get_node())
    path_poll.append(path)


path_poll = []
for i in range(1):
    new_path()


def path_add():
    global n
    n += 1
    cmd = "PATH_ADD "
    new_path()
    cmd += get_path()
    return cmd


def path_remove():
    cmd = "PATH_REMOVE "
    cmd += get_path()
    return cmd


def path_remove_by_id():
    return "PATH_REMOVE_BY_ID {}".format(get_id())


def path_get_id():
    cmd = "PATH_GET_ID "
    cmd += get_path()
    return cmd


def path_get_by_id():
    return "PATH_GET_BY_ID {}".format(get_id())


def path_count():
    return "PATH_COUNT"


def path_size():
    return "PATH_SIZE {}".format(get_id())


def path_distinct_node_count():
    return "PATH_DISTINCT_NODE_COUNT {}".format(get_id())


def contains_path():
    cmd = "CONTAINS_PATH "
    cmd += get_path()
    return cmd


def contains_path_id():
    return "CONTAINS_PATH_ID {}".format(get_id())


def distinct_node_count():
    return "DISTINCT_NODE_COUNT"


def compare_paths():
    return "COMPARE_PATHS {} {}".format(get_id(), get_id())


def path_contains_node():
    return "PATH_CONTAINS_NODE {} {}".format(get_id(), get_node())


def contains_node():
    return "CONTAINS_NODE {}".format(get_node())


def contains_edge():
    return "CONTAINS_EDGE {} {}".format(get_node(), get_node())


def is_node_connected():
    return "IS_NODE_CONNECTED {} {}".format(get_node(), get_node())


def shortest_path_length():
    return "SHORTEST_PATH_LENGTH {} {}".format(get_node(), get_node())


def rnd(n):
    return random.randint(1, n)


MAX_LINEAR = 500
MAX_MOD = 20

global n_linear, n_mod
n_linear = 0
n_mod = 0

if __name__ == "__main__":
    # os.chdir("C:/Develop/PyCharm/OOHelper/")

    test = []
    cmd_list = []
    cmd_list += rnd(4) * [path_add]
    cmd_list += rnd(1) * [path_remove]
    cmd_list += rnd(3) * [path_remove_by_id]
    cmd_list += rnd(1) * [path_get_id]
    cmd_list += rnd(1) * [path_get_by_id]
    cmd_list += rnd(1) * [path_count]
    cmd_list += rnd(1) * [path_size]
    cmd_list += rnd(1) * [path_distinct_node_count]
    cmd_list += rnd(1) * [contains_path]
    cmd_list += rnd(1) * [contains_path_id]
    cmd_list += rnd(10) * [distinct_node_count]
    cmd_list += rnd(10) * [compare_paths]
    cmd_list += rnd(1) * [path_contains_node]
    cmd_list += rnd(1) * [contains_node]
    cmd_list += rnd(1) * [contains_edge]
    cmd_list += rnd(10) * [is_node_connected]
    cmd_list += rnd(10) * [shortest_path_length]

    for i in range(7000):
        pick = cmd_list[random.randint(0, len(cmd_list) - 1)]

        linear_cmd = [path_add, path_remove, path_remove_by_id, path_get_id, path_get_by_id, contains_path, compare_paths]
        if pick in linear_cmd:
            n_linear += 1
            if n_linear >= MAX_LINEAR:
                new_list = []
                for cmd in cmd_list:
                    if cmd not in linear_cmd:
                        new_list.append(cmd)
                cmd_list = new_list

        mod_cmd = [path_add, path_remove, path_remove_by_id]
        if pick in mod_cmd:
            n_mod += 1
            if n_mod >= MAX_MOD:
                new_list = []
                for cmd in cmd_list:
                    if cmd not in mod_cmd:
                        new_list.append(cmd)
                cmd_list = new_list

        test.append(pick())

    open(r"test.in", "w").writelines(["\n".join(test), '\n'])

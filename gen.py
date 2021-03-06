import random
from config import *
import time
import os
from utils import datacheck
import threading

id_now = 0
available_level = [-3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

def get_next_id():
    global id_now
    id_now += 1
    return id_now


def gen_level(diff=-1):
    level = random.choice(available_level)
    while level == diff:
        level = random.choice(available_level)
    return level


def request(time, id_, from_, to):
    return "[{:.1f}]{}-FROM-{}-TO-{}\n".format(float(time), id_, from_, to)


def gen_batch(time, n):
    batch = []
    for i in range(n):
        level_from = gen_level()
        level_to = gen_level(level_from)
        batch.append(request(time, get_next_id(), level_from, level_to))
    return batch


def save(filename, lines):
    open(filename, "w").writelines(lines)
    # check = datacheck(filename)
    # if check[0] == 0:
    #     os.remove(filename)
    #     return
    print("Generated: {} ".format(filename))


def autoname():
    return "auto_{}.in".format("".join(str(time.time()).split('.')))


def gen(n_batch, batch_size, time_interval=1.0):
    global id_now
    assert n_batch * batch_size <= cfg.MAX_REQUEST
    time = 0.0
    requests = []
    for i in range(n_batch):
        assert time < cfg.MAX_TIME
        requests += gen_batch(time, batch_size)
        time += time_interval * random.random()
    return requests


def random_range(range):
    return random.random() * range + 1 - range




# if __name__ == "__main__":
#     id_now = 0
#     gen_path = os.path.join("test_data", "auto")
#     # print(gen(n_batch=5, batch_size=6, time_interval=30))
#     # exit(0)
#     if not os.path.exists(gen_path):
#         os.mkdir(gen_path)
#
#     n = 512
#     for i in range(n):
#         save(os.path.join(gen_path, autoname()), gen(n_batch=40, batch_size=1, time_interval=2.0))
#     # gen(n_batch=40, batch_size=1, time_interval=0.1)



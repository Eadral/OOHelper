import random
from macro import *
import time
import os

id_now = 1

def get_next_id():
    global id_now
    id_now += 1
    return id_now

def gen_level(diff=-1, mi=MIN_LEVEL, ma=MAX_LEVEL):
    level = random.randint(mi, ma)
    while level == diff:
        level = random.randint(mi, ma)
    return level


def request(time, id_, from_, to):
    return "[{}]{}-FROM-{}-TO-{}\n".format(float(time), id_, from_, to)

def gen_batch(time, n):
    batch = []
    for i in range(n):
        level_from = gen_level()
        level_to = gen_level(level_from)
        batch.append(request(time, get_next_id(), level_from, level_to))
    return batch

def save(filename, lines):
    open(filename, "w").writelines(lines)

def autoname():
    return "auto_{}.in".format("".join(str(time.time()).split('.')))

def gen(n_batch, batch_size, time_interval=1):
    assert n_batch * batch_size <= MAX_REQUEST
    time = 0
    requests = []
    for i in range(n_batch):
        assert time < MAX_TIME
        requests += gen_batch(time, batch_size)
        time += time_interval
    return requests

if __name__ == "__main__":
    gen_path = r"test_data\auto"
    for i in range(5):
        save(os.path.join(gen_path, autoname()), gen(n_batch=3, batch_size=5, time_interval=1))





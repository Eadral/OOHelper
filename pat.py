import os
import sys
from time import time
import re
import subprocess
import os
import time
import threading
import threading
import time
import inspect
import ctypes
import signal
from macro import *

def pat(test_data_in, class_path, jar):
    start = time.time()
    inputfile = open(test_data_in).readlines()

    input = parseInput(inputfile)
    outputfile = callProgram(r"java -cp {} {}".format(jar, class_path), inputfile, TIME_LIMIT - start)
    output = parseOutput(outputfile)
    end = time.time()

    return checkAll(input, output) and end - start < TIME_LIMIT


def checkAll(input, output):
    return check_1_1(input, output) \
           and check_1_2(input, output) \
           and check_1_3(input, output) \
           and check_1_4(input, output) \
           and check_2(input, output)


def parseInput(inputfile):
    personRequests = []
    for line in inputfile:
        result = re.search(r'\[(.*)\](\d+)-FROM-(\d+)-TO-(\d+)', line.strip(), re.M | re.I)
        personRequests.append(result.groups())
    return personRequests


def run(p, output):
    while True:
        line = p.stdout.readline()
        if not line:
            break
        #         print(line)
        output.append(line.decode().strip())


def callProgram(cmd, inputFile, timeout=200):
#     os.chdir("temp")
#     print(inputFile)
    output = []
    p = subprocess.Popen(cmd,
                         shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    w = threading.Thread(target=run, args=(p, output,))
    last_time = 0
    for line in inputFile:
        result = re.search(r'\[(.*)\](.*)', line.strip(), re.M | re.I)
        sleeptime = result.group(1)
        inputLine = result.group(2)
        #     print(sleeptime)
        time.sleep(float(sleeptime) - last_time)
        last_time = float(sleeptime)
        write_str = inputLine + '\r\n'
        #         print(write_str)
        p.stdin.write(write_str.encode("UTF-8"))
        p.stdin.flush()
        time.sleep(1)
    w.start()
    p.stdin.close()
    if p.wait(timeout) != 0:
        return []
#     os.chdir("..")
#     print(output)
    return output


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def parseOutput(inputfile):
    sequence = []
    IN = []
    OUT = []
    OPEN = []
    CLOSE = []
    for line in inputfile:
        result = re.search(r'\[(.*)\]IN-(\d+)-(\d+)', line.strip(), re.M | re.I)
        if result is not None:
            sequence.append(["IN", result.groups()])
            IN.append(result.groups())
            continue
        result = re.search(r'\[(.*)\]OUT-(\d+)-(\d+)', line.strip(), re.M | re.I)
        if result is not None:
            sequence.append(["OUT", result.groups()])
            OUT.append(result.groups())
            continue
        result = re.search(r'\[(.*)\]OPEN-(\d+)', line.strip(), re.M | re.I)
        if result is not None:
            sequence.append(["OPEN", result.groups()])
            OPEN.append(result.groups())
            continue
        result = re.search(r'\[(.*)\]CLOSE-(\d+)', line.strip(), re.M | re.I)
        if result is not None:
            sequence.append(["CLOSE", result.groups()])
            CLOSE.append(result.groups())
            continue
    return sequence


def check_1_1(input, output):
    sequence = output
    time = []
    level = []
    for mesType, mes in sequence:
        time.append(float(mes[0]))
        if mesType == "IN" or mesType == "OUT":
            level.append(int(mes[2]))
        else:
            level.append(int(mes[1]))
    assert len(time) == len(level)
    for i in range(len(time) - 1):
        if not (time[i + 1] - time[i] > abs(level[i + 1] - level[i]) * 0.5 - 0.001):
            return False
    return True


def check_1_2(intput, output):
    sequence = output
    length = len(sequence)
    for i, (mesType, mes) in enumerate(sequence):
        if mesType == "OPEN" and i != 0:
            if not (float(sequence[i + 1][1][0]) - float(sequence[i][1][0]) > 0.25 - 0.001):
                print(sequence[i + 1], sequence[i])
                return False
        if mesType == "CLOSE" and i != length - 1:
            if not (float(sequence[i][1][0]) - float(sequence[i - 1][1][0]) > 0.25 - 0.001):
                print(sequence[i], sequence[i - 1])
                return False
    return True


def getLevel(sequence):
    mesType, mes = sequence
    if mesType == "OPEN" or mesType == "CLOSE":
        return int(mes[1])
    else:
        return int(mes[2])


def getTime(sequence):
    return float(sequence[1][0])


def getId(sequence):
    mesType, mes = sequence
    assert mesType == "IN" or mesType == "OUT"
    return int(mes[1])


def check_1_3(input, output):
    sequence = output
    isClosed = True
    for i, (mesType, mes) in enumerate(sequence):
        if i != 1 and not isClosed and (getLevel(sequence[i - 1]) != getLevel(sequence[i])):
            print(sequence[i - 1], sequence[i])
            return False

        if mesType == "OPEN":
            isClosed = False
        if mesType == "CLOSE":
            isClosed = True
    return True


def check_1_4(input, output):
    sequence = output
    isOpen = False
    for i, (mesType, mes) in enumerate(sequence):
        if not isOpen and (mesType == "IN" or mesType == "OUT"):
            return False
        if mesType == "OPEN":
            isOpen = True
        if mesType == "CLOSE":
            isOpen = False
    if isOpen == True:
        return False
    return True


def check_2(input, output):
    id_now = {}
    id_to = {}
    id_set = []
    ele = set()
    for time, id_, from_, to in input:
        id_now[int(id_)] = int(from_)
        id_to[int(id_)] = int(to)
        id_set.append(int(id_))
    #     print(id_now)
    sequence = output
    for i, (mesType, mes) in enumerate(sequence):
        #         print(sequence[i])
        if mesType == "IN":
            thisID = getId(sequence[i])
            del id_now[thisID]
            if thisID in ele:
                return False
            ele.add(thisID)
        if mesType == "OUT":
            thisID = getId(sequence[i])
            ele.remove(thisID)
            id_now[thisID] = getLevel(sequence[i])
    if len(ele) > 0:
        return False
    for id_ in id_set:
        if id_now[int(id_)] != id_to[int(id_)]:
            return False
    return True

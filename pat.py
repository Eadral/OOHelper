import re
import subprocess
import threading
import time
# from time import time

from config import *
from utils import *


def pat(test_data_in, class_path, jar, prt=False):
    inputfile = open(test_data_in).readlines()
    # print("@@@", test_data_in)
    basetime, maxtime = datacheck(test_data_in)
    # input = parseInput(inputfile)
    # print("@@@", input)
    start = time.time()
    outputfile = callProgram(r"java -Xmx128m -cp {} {}".format(jar, class_path), inputfile)
    end = time.time()
    passed_time = end - start

    # output = parseOutput(outputfile)
    if prt:
        for line in outputfile:
            print(line)
        # A, B, C = parseOutputABC(outputfile)
        # print("Elevator A:")
        # for line in A:
        #     print("\033[1;34m{}\033[0m".format(line))
        # print("Elevator B:")
        # for line in B:
        #     print("\033[1;35m{}\033[0m".format(line))
        # print("Elevator C:")
        # for line in C:
        #     print("\033[1;36m{}\033[0m".format(line))
    # print(outputfile)
    ac = checkAll(inputfile, outputfile)
    t_ac = passed_time < maxtime
    if ac is True and t_ac is True:
        if passed_time > basetime + 20:
            print("\033[1;33mWarning: {}, time:{}, base_time: {}\033[0m"
                  .format(test_data_in, passed_time, basetime, maxtime))
            return True, passed_time
        print("\033[1;32mPassed: {}, time:{}, base_time: {}\033[0m".format(test_data_in, passed_time, basetime))
        return True, passed_time
    if ac is not True:
        print("\033[1;31mFailed: {}\n\tWA: {}\033[0m".format(test_data_in, ac))
        return False, passed_time
    if t_ac is not True:
        print("\033[1;31mWarning: {}\n\tTLE: {}, max_time: {}\033[0m".format(test_data_in, passed_time, maxtime))
        return True, passed_time


def parseInput(inputfile):
    personRequests = []
    for line in inputfile:
        result = re.search(r'\[(.*)\](-?\d+)-FROM-(-?\d+)-TO-(-?\d+)', line.strip(), re.M)
        personRequests.append(result.groups())
    return personRequests


def run(p, output):
    while True:
        line = p.stdout.readline()
        if not line:
            break
        # print(line)
        output.append(line.decode().strip())


def callProgram(cmd, inputFile):
    # print(cmd)
    #     os.chdir("temp")
    #     print(inputFile)
    output = []
    if cfg.CLOSE_STDERR:
        p = subprocess.Popen(cmd,
                             shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p = subprocess.Popen(cmd,
                             shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    w = threading.Thread(target=run, args=(p, output,))
    last_time = 0
    for line in inputFile:
        result = re.search(r'\[(.*)\](.*)', line.strip(), re.M)
        sleeptime = result.group(1)
        inputLine = result.group(2)
        #     print(sleeptime)
        time.sleep(float(sleeptime) - last_time)
        last_time = float(sleeptime)
        write_str = inputLine + '\r\n'
        #         print(write_str)
        p.stdin.write(write_str.encode("UTF-8"))
        p.stdin.flush()
        time.sleep(0.01)
    w.start()
    p.stdin.close()
    try:
        if p.wait(cfg.TIME_LIMIT) != 0:
            return output
    except subprocess.TimeoutExpired:
        p.kill()
        p.terminate()
        print("\033[1;31mError: TimeoutExpired: May in the endless loop/wait. Check your 'synchronized'.")
        return output
    # print(p.returncode)
    if p.returncode != 0:
        print("\033[1;31mError: return code {} is not 0\033[0m".format(p.returncode))
        return output

    #     os.chdir("..")
    #     print(output)
    return output

def parseOutputABC(inputfile):
    sequenceA = []
    sequenceB = []
    sequenceC = []
    for line in inputfile:
        result = re.search(r'-A', line.strip(), re.M)
        if result is not None:
            sequenceA.append(line)
            continue
        result = re.search(r'-B', line.strip(), re.M)
        if result is not None:
            sequenceB.append(line)
            continue
        result = re.search(r'-C', line.strip(), re.M)
        if result is not None:
            sequenceC.append(line)
            continue
    return sequenceA, sequenceB, sequenceC

def parseOutput(inputfile):
    sequence = []
#     IN = []
#     OUT = []
#     OPEN = []
#     CLOSE = []
    for line in inputfile:
        result = re.search(r'\[(.*)\]IN-(-?\d+)-(-?\d+)', line.strip(), re.M)
        if result is not None:
            sequence.append(["IN", result.groups()])
            continue
        result = re.search(r'\[(.*)\]OUT-(-?\d+)-(-?\d+)', line.strip(), re.M)
        if result is not None:
            sequence.append(["OUT", result.groups()])
            continue
        result = re.search(r'\[(.*)\]OPEN-(-?\d+)', line.strip(), re.M)
        if result is not None:
            sequence.append(["OPEN", result.groups()])
            continue
        result = re.search(r'\[(.*)\]CLOSE-(-?\d+)', line.strip(), re.M)
        if result is not None:
            sequence.append(["CLOSE", result.groups()])
            continue
        result = re.search(r'\[(.*)\]ARRIVE-(-?\d+)', line.strip(), re.M)
        if result is not None:
            sequence.append(["ARRIVE", result.groups()])
            continue
    return sequence


def check_1_1(input, output, eId):
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
        estimate_time = abs(level[i + 1] - level[i]) * cfg.LEVEL_TIME[eId]
        if level[i] * level[i + 1] < 0:
            estimate_time -= cfg.LEVEL_TIME[eId]
        if not (time[i + 1] - time[i] >= estimate_time - cfg.EPS):
            return "The elevator has no enough time to move such far distance at {}： {}. {}, {}".format(i, [sequence[i-1], sequence[i], sequence[i+1]], time[i + 1] - time[i], estimate_time - cfg.EPS)
    return True


def check_1_2(intput, output, eId):
    sequence = output
    length = len(sequence)
    for i, (mesType, mes) in enumerate(sequence):
        if mesType == "OPEN" and i != 0:
            index = i + 1
            while index < len(sequence) and sequence[index][0] != "CLOSE":
                index += 1
            diff = cfg.DOOR_TIME
            if index == len(sequence):
                return "No Close with {}".format(sequence[i])
            if sequence[index][0] == "CLOSE":
                diff = cfg.DOOR_TIME * 2
            if not (float(sequence[index][1][0]) - float(sequence[i][1][0]) >= diff) - cfg.EPS:
                # print(sequence[i + 1], sequence[i])
                return "The elevator has no enough time to open/close at {}： {}".format(i, [sequence[index], sequence[i], sequence[i+1]])
        # if mesType == "CLOSE" and i != length - 1:
        #     index = i - 1
        #     while index > 0 and sequence[index][0] != "OPEN":
        #         index -= 1
        #     diff = 0.25
        #     if sequence[index][0] == "OPEN":
        #         diff = 0.5
        #     if not (float(sequence[i][1][0]) - float(sequence[index][1][0]) > diff - 0.001):
        #         # print(sequence[i], sequence[i - 1])
        #         return "The elevator has no enough time to close at {}".format(i)
    return True


def getLevel(sequence):
    mesType, mes = sequence
    if mesType in ["OPEN", "CLOSE", "ARRIVE"]:
        return int(mes[1])
    else:
        return int(mes[2])


def getTime(sequence):
    return float(sequence[1][0])


def getId(sequence):
    mesType, mes = sequence
    assert mesType == "IN" or mesType == "OUT"
    return int(mes[1])


def check_1_3(input, output, eId):
    sequence = output
    isClosed = True
    for i, (mesType, mes) in enumerate(sequence):
        if i != 1 and not isClosed and (getLevel(sequence[i - 1]) != getLevel(sequence[i])):
            # print(sequence[i - 1], sequence[i])
            return "The elevator is open at {} while you want it move： {}".format(i, [sequence[i-1], sequence[i], sequence[i+1]])
        if mesType == "OPEN":
            isClosed = False
        if mesType == "CLOSE":
            isClosed = True
    return True


def check_1_4(input, output, eId):
    sequence = output
    isOpen = False
    for i, (mesType, mes) in enumerate(sequence):
        if not isOpen and (mesType == "IN" or mesType == "OUT"):
            return "The elevator is closed at {} while you want someone in/out： {}".format(i, [sequence[i-1], sequence[i], sequence[i+1]])
        if mesType == "OPEN":
            if isOpen is True:
                return "The elevator is open at {} while you want it open again： {}".format(i, [sequence[i - 1],
                                                                                                   sequence[i],
                                                                                                   sequence[i + 1]])

            isOpen = True
        if mesType == "CLOSE":
            if isOpen is False:
                return "The elevator is closed at {} while you want it close again： {}".format(i, [sequence[i - 1],
                                                                                                   sequence[i],
                                                                                                   sequence[i + 1]])

            isOpen = False
    if isOpen == True:
        return "Elevator is not closed at the end."
    return True

def check_3(input, output, eId):
    sequence = output
    levelNow = 1
    arrivalTime = 0
    for i, (mesType, mes) in enumerate(sequence):
        if mesType == "ARRIVE":
            level = getLevel(sequence[i])
            if level in [0]:
                return "Bad arrive 0 at {}： {}".format(i, [sequence[-1], sequence[i], sequence[i+1]])
            time = getTime(sequence[i])
            if levelNow in [-1, 1]:
                if not 0 < abs(levelNow - level) <= 2:
                    return "Bad arrive 0 at {}： {}".format(i, [sequence[-1], sequence[i], sequence[i+1]])
            else:
                if not 0 < abs(levelNow - level) <= 1:
                    #print(levelNow, level)
                    return "Bad arrive at {}： {}".format(i, [sequence[-1], sequence[i], sequence[i+1]])
            if not abs(arrivalTime - time) >= 0.4 - cfg.EPS:
                return "Bad arrive at {}： {}".format(i, [sequence[-1], sequence[i], sequence[i+1]])
            arrivalTime = time
            levelNow = level
    return True

def check_4(input, output, eId):
    sequence = output
    inside = set()
    for i, (mesType, mes) in enumerate(sequence):
        if mesType == "IN":
            inside.add(getId(sequence[i]))
            maxN = 0
            if eId == "A":
                maxN = 6
            if eId == "B":
                maxN = 8
            if eId == "C":
                maxN = 7
            if len(inside) > maxN:
                return "Elevator is full at {}： {}".format(i, [sequence[-1], sequence[i], sequence[i + 1]])
        if mesType == "OUT":
            if getId(sequence[i]) not in inside:
                return "{} not in elevator at {}： {}".format(getId(sequence[i]), i, [sequence[-1], sequence[i], sequence[i + 1]])
            inside.remove(getId(sequence[i]))
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
#         print(id_now)
        #         print(sequence[i])
        if mesType == "IN":
            thisID = getId(sequence[i])
            level = getLevel(sequence[i])
            if (thisID not in id_now) or (level != id_now[thisID]):
                return "{} is not at floor {} while you want the guy in.".format(thisID, level)
            del id_now[thisID]
            if thisID in ele:
                return "{} has been in the elevator at {} while you want the guy in again.".format(thisID, i)
            ele.add(thisID)
        if mesType == "OUT":
            thisID = getId(sequence[i])
            if thisID not in ele:
                return "{} is not in the elevator at {} while you want the guy out.".format(thisID, i)
            ele.remove(thisID)
            id_now[thisID] = getLevel(sequence[i])
    if len(ele) > 0:
        return "{} still in the elevator.".format(ele)
    for id_ in id_set:
        if id_now[int(id_)] != id_to[int(id_)]:
            return "{} in the wrong floor at the end.".format(id_)
    return True


def checkAllSequence(input, output, eId):
    r_1_1 = check_1_1(input, output, eId)
    r_1_2 = check_1_2(input, output, eId)
    r_1_3 = check_1_3(input, output, eId)
    r_1_4 = check_1_4(input, output, eId)
    r_4 = check_4(input, output, eId)
#     r_2 = check_2(input, output)
    r_3 = check_3(input, output, eId)
    if r_1_1 is not True:
        return "check_1_1: \n\t" + str(r_1_1) + "\n\t" + str(output)
    if r_1_2 is not True:
        return "check_1_2: \n\t" + str(r_1_2) + "\n\t" + str(output)
    if r_1_3 is not True:
        return "check_1_3: \n\t" + str(r_1_3) + "\n\t" + str(output)
    if r_1_4 is not True:
        return "check_1_4: \n\t" + str(r_1_4) + "\n\t" + str(output)
    if r_4 is not True:
        return "check_4: \n\t" + str(r_4) + "\n\t" + str(output)
#     if r_2 is not True:
#         return "check_2: \n\t" + str(r_2) + "\n\t" + str(output)
    if r_3 is not True:
        return "check_3: \n\t" + str(r_3) + "\n\t" + str(output)
    return True

def checkAll(inputfile, outputfile):
    input = parseInput(inputfile)
    sequenceAll = parseOutput(outputfile)
    sequenceA, sequenceB, sequenceC = parseOutputABC(outputfile)
    outputSequenceA = parseOutput(sequenceA)
    outputSequenceB = parseOutput(sequenceB)
    outputSequenceC = parseOutput(sequenceC)
    r_A = checkAllSequence(input, outputSequenceA, "A")
    r_B = checkAllSequence(input, outputSequenceB, "B")
    r_C = checkAllSequence(input, outputSequenceC, "C")
    r_All = check_2(input, sequenceAll)
    if r_A is not True:
        return "Error Elevator A: " + str(r_A) + "\n\t" + str(outputfile)
    if r_B is not True:
        return "Error Elevator B: " + str(r_B) + "\n\t" + str(outputfile)
    if r_C is not True:
        return "Error Elevator C: " + str(r_C) + "\n\t" + str(outputfile)
    if r_All is not True:
        return r_All + "\n\t" + str(outputfile)
    return True

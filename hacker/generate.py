from xeger import Xeger
from random import *

operatorNoPat = "[+-]\\ {0,2}"
operatorPat = "\\ {0,2}[+-]\\ {0,2}"
multPat = "\\ {0,2}\\*\\ {0,2}"
consPat = "[+-]?[1-9][0-9]{0,1}"
monoPat = "x( {0,1}\\^ {0,1}[+-]?[1-9])?"
leftPat = "\\ {0,2}\\(\\ {0,2}"
rightPat = "\\ {0,2}\\)\\ {0,2}"
indexPat = "(\\^ {0,1}[+-]?[1-9])?"
pat = Xeger(limit=20)
nest = 0


# togetherPat = "(" + monoPat + "|" + sinPat + "|" + cosPat + "|" + consPat + ")"
# firstPat = "([+-] {0,2}){1,2}" + togetherPat
# midPat = "( {0,2}\\* {0,2}" + togetherPat + "){0,3} {0,2}"
# termPat = firstPat + midPat


def generator():
    s = generate_poly()
    while len(s) > 200:
        s = generate_poly()
    return s


def generate_poly():
    poly = ""
    operator = randint(0, 1)
    if operator:
        poly += pat.xeger(operatorPat)
    poly += generate_term()
    if nest:
        times = randint(0, 1)
    else:
        times = randint(0, 2)
    for i in range(0, times):
        poly += pat.xeger(operatorPat) + generate_term()
    return poly


def generate_term():
    term = ""
    operator = randint(0, 1)
    if operator:
        term += pat.xeger(operatorNoPat)
    term += generate_factor()
    if nest:
        times = randint(0, 2)
    else:
        times = randint(0, 4)
    for i in range(0, times):
        term += pat.xeger(multPat) + generate_factor()
    return term


def generate_factor():
    global nest
    if nest < 3:
        factor_type = randint(1, 5)
    else:
        factor_type = randint(1, 2)
    factor = ""
    if factor_type == 1:
        factor = pat.xeger(consPat)
    elif factor_type == 2:
        factor = pat.xeger(monoPat)
    elif factor_type == 3:
        nest += 1
        factor = "sin" + pat.xeger(leftPat) + generate_factor() + pat.xeger(rightPat) + pat.xeger(indexPat)
        nest -= 1
    elif factor_type == 4:
        nest += 1
        factor = "cos" + pat.xeger(leftPat) + generate_factor() + pat.xeger(rightPat) + pat.xeger(indexPat)
        nest -= 1
    elif factor_type == 5:
        nest += 1
        factor = "(" + generate_poly() + ")"
        nest -= 1
    return factor

# def generator():
#     string = Xeger(limit=50)
#     return_string = "  "
#     for i in range(4):
#         string_out = string.xeger(termPat)
#         return_string += string_out
#
#     # insert_chars = ["+", "-", "2", "9", "5", "*", "(", ")", " ", "s", "^"]
#     # loop_num = randint(1, 3)
#     #
#     # for i in range(0, loop_num):
#     #     insert_position = randint(0, len(return_string)-1)
#     #     insert_num = randint(0, len(insert_chars)-1)
#     #     return_string = return_string[:insert_position] + insert_chars[insert_num] + return_string[insert_position:]
#
#     return return_string


print(generator())

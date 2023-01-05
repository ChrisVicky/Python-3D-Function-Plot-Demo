from os import EX_CANTCREAT
import re
from enum import Enum, unique
import numpy as np


@unique
class number(Enum):
    # blank space 
    SPACE = 256,
    # single operand
    NUM = 0, 
    X = 1, 
    Y = 2,
    


class sign(Enum):
    # functions
    SIN = 3, 
    COS = 4, 
    TAN = 5,

    # operations
    PLUS = 21, 
    MINUS = 22,
    DIVIDE = 23, 
    TIMES = 24,
    POWER = 25
    
    # others
    FR_BRACKET = 100
    BA_BRACKET = 101


def Error(str):
    print(f"\33[1;31m{str}\33[0m")


def Success(str):
    print(f"\33[1;34m{str}\33[0m")

def War(str):
    print(f"\33[1;33m{str}\33[0m")

def Log(str):
    print(f"\33[1;34m{str}\33[0m")


class rule:
    def __init__(self, p, token_type, priority):
        self.pattern = p
        self.type = token_type
        self.priority = priority

rules = [
    rule(re.compile(" +"), number.SPACE, 0),
    rule(re.compile("[0-9]"), number.NUM, 0),
    rule(re.compile("[xX]"), number.X, 0),
    rule(re.compile("[yY]"), number.Y, 0),
    rule(re.compile("\\+"), sign.PLUS, 1),
    rule(re.compile("\\-"), sign.MINUS, 1),
    rule(re.compile("\\*"), sign.TIMES, 2),
    rule(re.compile("\\/"), sign.DIVIDE, 2),
    rule(re.compile("\\^"), sign.POWER, 3),
    rule(re.compile("\\("), sign.FR_BRACKET, 1),
    rule(re.compile("\\)"), sign.BA_BRACKET, 1),
    rule(re.compile("[sS][iI][nN]"), sign.SIN, 5),
    rule(re.compile("[cC][oO][sS]"), sign.COS, 5),
    rule(re.compile("[tT][aA][nN]"), sign.TAN, 5)
]


class tokens:
    def __init__(self, type, str, priority):
        self.type = type
        self.str = str
        self.priority = priority


token = []


def make_tokens(target):
    while(len(token)):
        token.pop()
    flag = False
    temp = target
    l = 0
    cnt = 0
    while(temp):
        flag = False
        for r in rules:
            m = r.pattern.match(temp, 0)
            if(m):
                flag = True
                l += len(m[0])
                temp = target[l:]
                if(r.type==number.SPACE) :
                    break
                token.append(tokens(r.type, m[0], r.priority))
                if(r.type==sign.FR_BRACKET):
                    cnt += 1
                elif(r.type==sign.BA_BRACKET):
                    cnt -= 1
                if(cnt < 0):
                    Error("WRONG EXPRESSION! BRACKET ERROR")
                    return False
        if(flag==False):
            Error(f"No Match at '{temp}' ")
            return False
    if(cnt!=0):
        Error("WRONG EXPRESSION! BRACKET ERROR")
        return False
    return True


# 以下部分为计算

exe_flag = True
INF = 0xffffffff
EXPE_ = 0.000001

def is_sign(temp):
    return temp in sign
    # return temp.value >= number.PLUS.value and temp.value <= number.BA_BRACHET.value

def case_x(str, x,y):
    return x
def case_y(str, x,y):
    return y

def case_NUM(str, invalidx,invalidy):
    temp = int(str)
    temp_matrix = np.zeros(invalidx.shape)
    temp_matrix += temp
    # Success(f"array = {temp_matrix}, array_size={temp_matrix.shape}")
    return temp_matrix

def default(str, invalidx, inalidy):
    global exe_flag
    exe_flag = False
    Error(f"Expecting a Number or Variable Here {str}")
    return 0

def defaul(val1, val2):
    global exe_flag
    exe_flag = False
    Error(f"Expecting a Number or Variable Here val1, val2")
    return 0

def case_plus(val1, val2):
    return val1 + val2

def case_minus(val1, val2):
    return val1 - val2

def case_times(val1, val2):
    return val1 * val2

def case_divide(val1, val2):
    return np.divide(val1, val2, out=np.zeros_like(val1), where=val2!=0)

def case_power(val1, val2):
    return np.power(val1, val2)

def case_tan(val1, val2):
    return np.tan(val2)

def case_sin(val1, val2):
    return np.sin(val2)

def case_cos(val1, val2):
    return np.cos(val2)

switch_num = {
    number.NUM : case_NUM,
    number.X : case_x,
    number.Y : case_y,
}

switch_sign = {
    sign.PLUS   : case_plus,
    sign.MINUS  : case_minus,
    sign.TIMES  : case_times,
    sign.DIVIDE : case_divide,
    sign.POWER  : case_power,
    sign.SIN    : case_sin,
    sign.COS    : case_cos,
    sign.TAN    : case_tan
}


def get_op(q,p):
    pri = 100
    cnt = 0
    op = -1
    for i in range(q,p):
        if(is_sign(token[i].type)):
            if(token[i].type==sign.BA_BRACKET):
                cnt -= 1    
            elif(token[i].type==sign.FR_BRACKET):
                cnt += 1
            elif(cnt==0 and is_sign(token[i].type) and token[i].priority < pri):
                pri = token[i].priority
                op = i        
    return op

def check_brancket(q,p):
    cnt = 0
    global exe_flag
    for i in range(q,p):
        if(token[i].type == sign.FR_BRACKET):
            cnt += 1
        elif(token[i].type == sign.BA_BRACKET):
            cnt -= 1
        if(cnt==0):
            return False
        if(cnt < 0):
            exe_flag = False
            return False
    if(cnt):
        return True
    exe_flag = False
    return False


def exe(q,p,x,y):
    global exe_flag
    if exe_flag == False:
        return 0
    data = 0
    if(q==p):
        data = switch_num.get(token[q].type, default) (token[q].str,x,y)
    elif(q > p):
        exe_flag = False
        Error("Unknown Problems")
        data = 0
    else:
        if(check_brancket(q,p)):
            data = exe(q+1, p-1,x,y)
        else:
            op = get_op(q,p)
            val1 = 0
            if(op>q):
                val1 = exe(q,op-1,x,y)
            val2 = exe(op+1,p,x,y)
            data = switch_sign.get(token[op].type, default)(val1, val2)
    
    return data

def DO(str, x, y):
    global exe_flag
    token_flag = make_tokens(str)
    if token_flag == False:
        Error("No answer")
        return None, False, None
    name = ""
    Success("The Tokens")
    for t in token:
        name += t.str
        Success(f"Tokens = {t.str} type = {t.type}")
    Success("Calculating. . . . .")
    ans = exe(0,len(token)-1, x, y)
#    Success(f"ans={ans}")
    return ans, True, name


'''    
def case_divide(val1, val2):
    r_cnt = 0
    for row in val2:
        c_cnt = 0
        cut_cnt = 0
        for c in row:
            if abs(c)<abs(EXPE_):
                cut_cnt += 1
            c_cnt += 1
        if cut_cnt > c_cnt/2:
            val1 = np.delete(val1, r_cnt, 0)
            val2 = np.delete(val2, r_cnt, 0)
        r_cnt += 1

    Success(str(val2.size))
    return np.divide(val1, val2, out=np.zeros_like(val1), where=val2!=0)
    return val1 / val2
'''

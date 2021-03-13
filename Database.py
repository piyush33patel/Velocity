from collections import deque
from os import name

special = {",":"comma", ";":"semicolon", " ":"space", ".":"fullstop"}
digits = {"0":"zero", "1":"one", "2":"two", "3":"three", "4":"four", "5":"five", "6":"six", "7":"seven", "8":"eight", "9":"nine"}
error_map = dict()
occur_map = dict()

def initializeDict():    
    for i in range(ord('a'), ord('z')+1):
        error_map[chr(i)] = 0
        occur_map[chr(i)] = 0    
    for i in range(ord('A'), ord('Z')+1):
        error_map[chr(i)] = 0
        occur_map[chr(i)] = 0 
    for i in special.values():
        error_map[i] = 0
        occur_map[i] = 0
    for i in digits:
        error_map[i] = 0
        occur_map[i] = 0

def generateDatabase(log_path, paragraph_path):
    fp = open(log_path, "r", encoding='utf-16')
    logs = fp.read().split("-")
    fp.close()
    logs = logs[0:len(logs)-1]
    fp = open(paragraph_path, "r")
    paragraph = fp.read()
    fp.close()
    paragraph = paragraph[0:len(paragraph)-1]
    second(logs, paragraph)

def increaseCount(map, character, frequecy):
    if character in special.keys():
        character = special[character]
    elif character in digits.keys():
        character = digits[character]
    map[character] = map[character]+ frequecy

def second(logs, paragraph):
    initializeDict()
    log_pointer = 0
    para_pointer = 0
    incorrectChar = ""
    incorrectCount = 0
    while log_pointer < len(logs) and para_pointer < len(paragraph):
        if logs[log_pointer]==paragraph[para_pointer]:    
            incorrectChar = paragraph[para_pointer]
            if incorrectCount > 0:
                increaseCount(error_map, incorrectChar, incorrectCount//2)
                incorrectCount = 0
            increaseCount(occur_map, incorrectChar, 1)
            log_pointer += 1
            para_pointer += 1
        else:
            incorrectCount += 1
            log_pointer += 1

    print("printing occurences")
    for key in error_map.keys():
        if error_map[key] != 0:
            print(f"{key} : {error_map[key]}")
    print("printing occurences")

    # print("printing occurences")
    # for key in occur_map.keys():
    #     if occur_map[key] != 0:
    #         print(f"{key} : {occur_map[key]}")
    # print("printing occurences")
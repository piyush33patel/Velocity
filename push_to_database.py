from mysql.connector import connect

special = {",":"comma", ";":"semicolon", " ":"space", ".":"fullstop"}
digits = {"0":"zero", "1":"one", "2":"two", "3":"three", "4":"four", "5":"five", "6":"six", "7":"seven", "8":"eight", "9":"nine"}
error_map = dict()
pressed_map = dict()
paragraph_map = dict()


def repeatedThing(attribute, map):
    big = ""
    small = ""
    digits = ""    
    for i in range(ord('a'), ord('z')+1):
        small += f"{map[chr(i)]},\n"        
    for i in range(ord('A'), ord('Z')+1):
        big += f"{map[chr(i)]},\n"
    for i in range(ord('0'), ord('9')+1):
        digits += f"{map[chr(i)]},\n"

    values = f"({attribute},\n"
    values += f"{small}{big}{digits}"
    values += f"{map['comma']},\n"
    values += f"{map['semicolon']},\n"
    values += f"{map['space']},\n"
    values += f"{map['fullstop']})"
    return values

def initializeDict():    
    for i in range(ord('a'), ord('z')+1):
        error_map[chr(i)] = 0
        pressed_map[chr(i)] = 0    
        paragraph_map[chr(i)] = 0    
    for i in range(ord('A'), ord('Z')+1):
        error_map[chr(i)] = 0
        pressed_map[chr(i)] = 0 
        paragraph_map[chr(i)] = 0
    for i in special.values():
        error_map[i] = 0
        pressed_map[i] = 0
        paragraph_map[i] = 0
    for i in digits:
        error_map[i] = 0
        pressed_map[i] = 0
        paragraph_map[i] = 0

def mapTheLog(map, character, frequecy):
    if character in special.keys():
        character = special[character]
    elif character in digits.keys():
        character = digits[character]
    map[character] = map[character] + int(frequecy)

def pushToDatabase(table_name, primary_key, primary_key_value, values):
    mydb = connect(host="localhost", user="root", passwd="", database="velocity")
    print(mydb)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE {primary_key}={primary_key_value}")
    res = cursor.fetchall()
    if len(res)==0:
        cursor.execute(f"INSERT INTO {table_name} VALUES {values}")
        mydb.commit()
    mydb.close()

def generateDatabase(timestamp, log_path, para_number):
    fp = open(log_path, "r", encoding='utf-16')
    logs = fp.read().split("%")
    fp.close()
    logs = logs[0:len(logs)-1]
    initializeDict()
    for i in logs:
        now = i.split("-")
        chars = str(now[0])
        mapTheLog(paragraph_map, chars, 1)
        extra = now[1]
        extra = extra[1:len(extra)-1]
        mapTheLog(pressed_map, chars, 1)
        for j in extra:
            mapTheLog(pressed_map, j, 1)
        if len(extra) > 0:
            mapTheLog(error_map, chars, len(extra))
    pushToDatabase("paragraphs", "para_number", para_number, repeatedThing(para_number, paragraph_map))
    pushToDatabase("keys_pressed", "keylog_id", timestamp, repeatedThing(timestamp, pressed_map))
    pushToDatabase("errors_made", "keylog_id", timestamp, repeatedThing(timestamp, error_map))
    
    # print("printing occurences")
    # for key in error_map.keys():
    #     if error_map[key] != 0:
    #         print(f"{key} : {error_map[key]}")
    # print("printing occurences")

    # print("printing occurences")
    # for key in pressed_map.keys():
    #     if pressed_map[key] != 0:
    #         print(f"{key} : {pressed_map[key]}")
    # print("printing occurences")
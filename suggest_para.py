from mysql.connector import connect

current_para = 0

special = {",":"comma", ";":"semicolon", " ":"space", ".":"fullstop"}
digits = {"0":"zero", "1":"one", "2":"two", "3":"three", "4":"four", "5":"five", "6":"six", "7":"seven", "8":"eight", "9":"nine"}
columns = []

def initializeDict():    
    columns.append('keylod_id')
    for i in range(ord('a'), ord('z')+1):   
        columns.append(f'small_{chr(i)}')
    for i in range(ord('A'), ord('Z')+1):
        columns.append(f'big_{chr(i)}')
    for i in digits:
        columns.append(f'digit_{i}')
    for i in special.values():
        columns.append(i)


def suggestPara(para_number):
    current_para = para_number
    initializeDict()
    user_name = ""
    user_email = ""
    with open("users.txt", "r") as fp:
        user_name = fp.readline()
        user_email = fp.readline()
        user_name = user_name[0:len(user_name)-1]
        user_email = user_email[0:len(user_email)-1]

    mydb = connect(host="localhost", user="root", passwd="", database="velocity")
    cursor = mydb.cursor()
    cursor.execute(f'''
                    SELECT * 
                    FROM keys_pressed as kp 
                    WHERE kp.keylog_id IN (SELECT ts.keylog_id 
                                            FROM transactions AS ts 
                                                JOIN users AS us ON ts.email = us.email AND ts.email='{user_email}')
                    ''')
    res = cursor.fetchall()

    maxJustPrev = 0
    maxJustPrevCh = '?'
    maxOverall = 0
    maxOverallCh = '?'
    answer = []
    for i in res:
        temp = []
        maxWrongCh = '?'
        maxValue = 0
        doneWithID = False
        for j in range(0, len(i)):
            temp.append(i[j])
            if doneWithID and maxValue <= i[j]:
                maxValue = i[j]
                maxWrongCh = columns[j]
            doneWithID = True
        answer.append(temp)
        if maxJustPrevCh=='?':
            maxJustPrevCh = maxWrongCh
            maxJustPrev = maxValue
        if maxValue >= maxOverall:
            maxOverall = maxValue
            maxOverallCh = maxWrongCh

    # NOW got the characters
    print(f'{maxOverall} : {maxOverallCh}')
    print(f'{maxJustPrev} : {maxJustPrevCh}')

    cursor.execute(f'''
                    SELECT ps.para_number
                    FROM paragraphs AS ps
                    WHERE ps.{maxOverallCh} = (SELECT MAX({maxOverallCh})
                                        FROM paragraphs
                                        WHERE para_number != {current_para})
                            AND ps.para_number != {current_para}
                    ''')

    suggestions = set()
    res = cursor.fetchall()
    print(f'res1 : {res}')
    for i in res:
        for j in i:
            suggestions.add(j)

    cursor.execute(f'''
                    SELECT ps.para_number
                    FROM paragraphs AS ps
                    WHERE ps.{maxJustPrevCh} = (SELECT MAX({maxJustPrevCh})
                                        FROM paragraphs 
                                        WHERE para_number != {current_para})
                            AND ps.para_number != {current_para}
                    ''')
    res = cursor.fetchall()
    print(f'res1 : {res}')
    for i in res:
        for j in i:
            suggestions.add(j)
    
    print(40 * '*')
    print(suggestions)
    print(f'PARAGRAPHS SUGGESTED TO {user_name} : ')
    for i in suggestions:
        print(f'paragraph_number : {i}')
    print(40 * '*')

    mydb.commit()
    mydb.close()
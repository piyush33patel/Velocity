from mysql.connector import connect

def repeatedThing(attribute):
    big = ""
    small = ""
    digits = ""    
    for i in range(ord('a'), ord('z')+1):
        small += f"small_{chr(i)} int,\n"
        big += f"big_{chr(i)} int,\n"
    for i in range(ord('0'), ord('9')+1):
        digits += f"digit_{chr(i)} int,\n"

    total = f"({attribute} varchar(30),\n"
    total += f"{small}{big}{digits}"
    total += "comma int,\n"
    total += "semicolon int,\n"
    total += "space int,\n"
    total += "fullstop int,\n"
    total += f"PRIMARY KEY ({attribute}))"
    return total

mydb = connect(host="localhost", user="root", passwd="")
cursor = mydb.cursor()
cursor.execute('''CREATE DATABASE IF NOT EXISTS velocity''')
mydb.close()

mydb = connect(host="localhost", user="root", passwd="", database="velocity")
print(mydb)
cursor = mydb.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users(
    name varchar(20) NOT NULL,
    email varchar(30) NOT NULL,
    PRIMARY KEY (email)
    )''')

cursor.execute(f"CREATE TABLE IF NOT EXISTS paragraphs {repeatedThing('para_number')}")
cursor.execute(f"CREATE TABLE IF NOT EXISTS keys_pressed {repeatedThing('keylog_id')}")
cursor.execute(f"CREATE TABLE IF NOT EXISTS errors_made {repeatedThing('keylog_id')}")

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions(
    keylog_id varchar(30),
    email varchar(30) NOT NULL,
    para_number varchar(30) NOT NULL,
    PRIMARY KEY (keylog_id),
    FOREIGN KEY (email) REFERENCES users(email),
    FOREIGN KEY (para_number) REFERENCES paragraphs(para_number)
    )''')

mydb.close()

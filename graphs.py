from tkinter import Label
from mysql.connector import connect
import matplotlib.pyplot as plt
import numpy as np

special = ["comma", "semicolon", "space", "fullstop"]
digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
error = []
pressed = []
paragraph = []
attributes = []

def initializeDict():    
    for i in range(ord('a'), ord('z')+1):
        attributes.append(chr(i))
    for i in range(ord('A'), ord('Z')+1):
        attributes.append(chr(i))
    for i in digits:
        attributes.append(i)
    for i in special:
        attributes.append(i)

def getDataFromDatabase(para_number, keylog_id):
    mydb = connect(host="localhost", user="root", passwd="", database="velocity")
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM paragraphs WHERE para_number={para_number}")
    paragraph_db = cursor.fetchall()[0]
    cursor.execute(f"SELECT * FROM errors_made WHERE keylog_id={keylog_id}")
    error_db = cursor.fetchall()[0]
    cursor.execute(f"SELECT * FROM keys_pressed WHERE keylog_id={keylog_id}")
    pressed_db = cursor.fetchall()[0]
    mydb.close()
    initializeDict()
    paragraph_db = paragraph_db[1:len(paragraph_db)]
    error_db = error_db[1:len(error_db)]
    pressed_db = pressed_db[1:len(pressed_db)]

    x_labels = []
    error = []
    paragraph = []
    pressed = []
    
    for i in range(0, len(paragraph_db)):
        if paragraph_db[i]==0 and error_db[i]==0 and pressed_db[i]==0:
            continue
        else:
            x_labels.append(attributes[i])
            paragraph.append(paragraph_db[i])
            pressed.append(pressed_db[i])
            error.append(error_db[i])
    plt.xticks(rotation = 35)
    plt.xticks(np.arange(0, len(x_labels)), x_labels)
    plt.bar(np.arange(0, len(x_labels))-0.25, np.array(paragraph), width=0.25, label="character occurences")
    plt.bar(np.arange(0, len(x_labels)), np.array(pressed), width=0.25, label="keys pressed", color="#9ACD32")
    plt.bar(np.arange(0, len(x_labels))+0.25, np.array(error), width=0.25, label="errors made", color="#FF4500")
    plt.legend(loc="best")
    plt.show()
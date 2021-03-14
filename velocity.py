from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename
from collections import deque
from datetime import datetime
from database import generateDatabase
import os


def openFile():    
    global path
    tempPath = askopenfilename(initialdir = "Paragraphs/", filetypes=[("Text Documents", "*.txt")])
    if len(tempPath)==0:
        return
    path = tempPath
    toType.clear()
    typed.clear()
    user.clear()
    text_box.config(state=NORMAL)
    text_box.delete("1.0", END)
    entry_box.config(state=NORMAL)
    entry_box.delete(0, END)
    openParagraph(path, paragraph, toType)

def help():
    showinfo("Help", "We don't provide any help, we believe God help those who help themselves.")

def about():
    showinfo("About", "Project developed by Rishabh and Piyush.")


def getCharacter(word):
    if(len(word)==1):
        return word
    elif word=="space":
        return " "
    elif word=="BackSpace":
        return word
    elif word=="comma":
        return ","
    elif word=="semicolon":
        return ";"
    elif word=="period":
        return "."
    else:
        return word

def openParagraph(path, paragraph, toType):
    global logs
    logs = ""
    text_box.config(state=NORMAL)
    file = open(path)
    paragraph = file.read()
    paragraph = paragraph[0:len(paragraph)-1]
    text_box.insert(1.0, paragraph)
    text_box.config(state=DISABLED)
    text_box.pack()
    file.close()
    for i in paragraph:
        toType.append(i)

def generateLogs():
    today = datetime.today()
    file_name = f"Key-Logs/{today.year}{today.month}{today.day}{today.hour}{today.minute}{today.second}{today.microsecond}.txt"
    print(file_name)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    fp = open(file_name, "w", encoding='utf-16')
    fp.write(logs)
    fp.close()    
    generateDatabase(file_name)

def display(ch):
    global logs
    global incorrectCount
    text_box.config(state=NORMAL)
    empty = False
    next = ch
    if next=="BackSpace" or next.isalnum() or next==" " or next=="." or next=="," or next==";":
        if next=='BackSpace':
            text_box.tag_remove("start", 1.0, 'end')
            if len(user) == 0:
                empty = True
            if empty==False and len(typed)==len(user) and typed[0]==user[0]:
                toType.appendleft(typed.popleft())
            if empty==False:
                incorrectCount.append(user[0])
                user.popleft()
        else:
            user.appendleft(next)
        if empty==False and len(typed)==len(user)-1 and toType[0]==next:
            typed.appendleft(toType.popleft())
            incorrectCount.reverse()
            logs += f"{next}-{incorrectCount}%"
            incorrectCount = []

    text_box.tag_add("start", 1.0, f'end-{len(toType)+1}c')
    text_box.tag_config("start", foreground="orange")
    text_box.config(state=DISABLED)
    if len(toType) == 0:
        entry_box.config(state=DISABLED)
        okay = messagebox.showinfo("Velocity", "Now analysing your typing...")
        if okay=="ok":
            print("showing typing information.....")
            generateLogs()
        return

def action(event):
    ch = getCharacter(event.keysym)
    display(ch)



if __name__ == "__main__":
    window = Tk()
    window.title("VELOCITY - speed + direction")
    window.geometry("600x400")
    window.minsize(width=200, height=200)

    text_frame = Frame(window, height=30, width=30, highlightbackground="black", highlightthickness=1)
    text_frame.pack(pady=12)
    editor_frame = LabelFrame(window, padx=2, pady=2, bd=0, text="Input your text here")
    editor_frame.pack(pady=10)

    text_box = Text(text_frame, height=12, width=50, padx=5, pady=5, state=NORMAL, font=("", 12), wrap=WORD)
    
    logs = ""
    path = "Paragraphs/2.txt"
    paragraph = ""
    toType = deque()
    typed = deque()
    user = deque()
    incorrectCount = []
    openParagraph(path, paragraph, toType)

    menubar = Menu(window)
    menubar.add_command(label = "Open", command = openFile)
    menubar.add_command(label = "Help", command = help)
    menubar.add_command(labe = "About", command = about)
    window.config(menu = menubar)

    entry_box = Entry(editor_frame, width=25, font=("", 16))
    entry_box.bind("<Key>", action)
    entry_box.pack()
    window.mainloop()

    
'''
You can include these characters in your text file:
1) Alphabets
2) Digits
3) Semi-Colon
4) Full-Stop
5) Spaces
6) Comma
NOTE : New Line character is not allowed
'''
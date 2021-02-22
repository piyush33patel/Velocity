from tkinter import *
from collections import deque

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
    file = open(path)
    paragraph = file.read()
    paragraph = paragraph[0:len(paragraph)-1]
    text_box.insert(1.0, paragraph)
    text_box.config(state=DISABLED)
    text_box.pack()
    file.close()
    for i in paragraph:
        toType.append(i)

def display(ch):
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
                user.popleft()
        else:
            user.appendleft(next)
        if empty==False and len(typed)==len(user)-1 and toType[0]==next:
            typed.appendleft(toType.popleft())

    text_box.tag_add("start", 1.0, f'end-{len(toType)+1}c')
    text_box.tag_config("start", foreground="orange")

    text_box.config(state=DISABLED)
    print(f"User : {len(user)}")
    print(f"Progress : {len(typed)}")
    print(f"Pending : {len(toType)}")
    print("\n")

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
        
    #change this path to any file path
    path = "Paragraphs/two.txt"
    paragraph = ""
    toType = deque()
    typed = deque()
    user = deque()
    openParagraph(path, paragraph, toType)

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
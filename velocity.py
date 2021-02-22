from tkinter import *
from tkinter import Frame
from tkinter import LabelFrame
from tkinter import Text
from tkinter import Entry
from tkinter import NORMAL
from tkinter import DISABLED
from tkinter.messagebox import showinfo
from collections import deque

def new_file():
    pass

def open_file():
    file = open("Paragraphs/two.txt")
    paragraph = file.read()
    paragraph = paragraph[0: len(paragraph)-1]
    text_box.delete(1.0, END)
    text_box.insert(1.0, paragraph)
    file.close()

def quit_app():
    window.destroy()

def about_app():
    showinfo("Velocity", "Software developed under btp project.")

#function to get either character, number or escape sequence
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

#display function to change the colour
def display(event):
    text_box.config(state=NORMAL)
    ch = getCharacter(event.keysym)
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

#main program starts here
if __name__ == '__main__':

    window = Tk()
    window.title("VELOCITY - speed + direction")
    window.geometry("600x400")
    window.minsize(width=200, height=200)

    menu_bar = Menu(window)
    file_menu = Menu(menu_bar, tearoff = 0)

    file_menu.add_command(label = "New", command = new_file)
    file_menu.add_command(label = "Open", command = open_file)
    file_menu.add_command(label = "Quit", command = quit_app)
    menu_bar.add_cascade(labe = "File", menu = file_menu)

    help_menu = Menu(menu_bar, tearoff = 0)
    help_menu.add_command(label = "About Velocity", command=about_app)
    help_menu.add_command(label = "Help")
    menu_bar.add_cascade(label = "Help", menu=help_menu)

    window.config(menu = menu_bar)
    
    label = Label(window, text = "Welcome User", bg = "white",
    fg = "purple", pady = 2, padx = 10, font = ("comicsansms",15),
    borderwidth = 10)
    label.pack()

    text_frame = Frame(window, height=30, width=30, highlightbackground="black", highlightthickness=1)
    text_frame.pack(pady=12)
    editor_frame = LabelFrame(window, padx=2, pady=2, bd=0, text="Input your text here")
    editor_frame.pack(pady=10)

    text_box = Text(text_frame, height=12, width=50, padx=5, pady=5, state=NORMAL, font=("", 12))

    file = open("Paragraphs/one.txt")
    paragraph = file.read()
    paragraph = paragraph[0:len(paragraph)-1]
    text_box.insert(1.0, paragraph)
    file.close()

    text_box.config()
    text_box.pack()
    toType = deque()
    for i in paragraph:
        toType.append(i)
    typed = deque()
    user = deque()

    entry_box = Entry(editor_frame, width=25, font=("", 16))
    entry_box.bind("<Key>", display)
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

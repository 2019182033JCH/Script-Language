from tkinter import *
from tkinter.ttk import *

# from customtkinter import *
# Tk = CTk
# Frame = CTkFrame
# Label = CTkLabel
# Button = CTkButton
# Entry = CTkEntry
# ScrolledText = CTkTextbox
# Checkbutton = CTkCheckBox
# Radiobutton = CTkRadioButton

# set_default_color_theme("dark-blue") # Themes: "blue" (standard), "green", "dark-blue"
# set_appearance_mode("dark") # 'system', 'light'


import logging
logging.basicConfig(
    level=logging.INFO,
    format='(%(lineno)d): %(message)s'
)

window = Tk()       # 기본 윈도우 만들기
window.title('My Application')
# window.geometry('640x480+100+100') # 640 x 480 크기로, (100, 100) 위치에 생성
window.resizable(False, False) # 창 크기 변경 막기 (width, height)

# 보이지 않는 액자
first_line_frame = Frame(window)
first_line_frame.pack()

label = Label(first_line_frame, text='hello, World')
label.pack(side=LEFT)
# label.place(x=100, y=100)

def rotate(): # 버튼 누를 시 회전
    text = label.cget('text')
    text = text[1:] + text[0]
    label.config(text=text)

button = Button(first_line_frame, text='Hello', command=rotate)
button.pack()


# 텍스트 입력창
def change_text(event=None):
    new_text = entry.get()
    label.config(text=new_text.center(100, ' '))

entry = Entry(window, width=50)
entry.bind('<Return>', change_text)
entry.pack()

# 대용량 텍스트 넣기
from tkinter.scrolledtext import ScrolledText

wiki_python = '''Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation via the off-side rule.[33]
Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library.[34][35]
Guido van Rossum began working on Python in the late 1980s as a successor to the ABC programming language and first released it in 1991 as Python 0.9.0.[36] Python 2.0 was released in 2000. Python 3.0, released in 2008, was a major revision not completely backward-compatible with earlier versions. Python 2.7.18, released in 2020, was the last release of Python 2.[37]
Python consistently ranks as one of the most popular programming languages.
'''
textbox = ScrolledText(window, width=50, height=20, font=('Consolas', 12))
textbox.insert(END, wiki_python) # 텍스트 위젯 내부의 텍스트 맨 끝 부분
textbox.pack(fill=BOTH, expand=True, padx=10, pady=10)

# color tag
# textbox.tag_config('YELLOW', background='yellow', foreground='red')
# textbox.tag_add('YELLOW', '2.0', '2.10')

# check button
def over18_clicked():
    logging.info(f'{over18.get()=}')

over18 = IntVar() # 버튼값 연계용 정수 변수
cb = Checkbutton(window, text='over 18', variable=over18, command=over18_clicked)
over18.set(0) # check 기본값 false로
cb.pack()

# radio button - 여러개 중 하나 선택
def gender_updated(var, index, mode): # var, index, mode는 정해진 양식
    logging.info(f'{gender.get()=}')

gender = StringVar(value='male') # 초기값이 male인, 문자열 변수
Radiobutton(window, text="Male", value='male', variable=gender).pack()
Radiobutton(window, text="Female", value='female', variable=gender).pack()
gender.trace_add('write', gender_updated) # 변수의 상황을 추적하면서, write 되면


pattern_frame = LabelFrame(window, text='Pattern List')
pattern_frame.pack()

pattern_var = StringVar()
pattern_entry = Entry(pattern_frame, textvariable=pattern_var)
pattern_entry.pack()

import re

# 새로운 패턴을 넣고, 엔터를 치면, 정규식으로 검색
def add_pattern(event=None):
    pattern = pattern_entry.get()
    pattern_list.insert(0, pattern)
    search_pattern(pattern)

def search_pattern(pattern):
    pattern_re = re.compile(pattern)
    target_text = textbox.get('1.0', END) # 현재 스크롤텍스트 모든 내용을 확보
    lines = target_text.splitlines()

    # 기존에 검색하여 색을 태깅한 부분을 지움.
    textbox.tag_config('found', background='yellow', foreground='red')
    textbox.tag_remove('found', '1.0', END)

    for i, line in enumerate(lines):
        # 한 줄에 대해서, 매칭 오브젝트 리스트를 가져온다.
        for mo in pattern_re.finditer(line):
            # mo.span()[0], mo.span()[1] : 검색된 단어의 시작 / 끝 위치.
            textbox.tag_add(
                'found',
                f'{i+1}.0+{mo.span()[0]}chars', # 시작 위치 지정
                f'{i+1}.0+{mo.span()[1]}chars'
            )



pattern_entry.bind('<Return>', add_pattern)

pattern_list = Listbox(pattern_frame, selectmode=SINGLE, height=4)
pattern_list.insert(0, 'Python')
pattern_list.pack(fill=X, expand=True)

def set_pattern(event=None):
    # 리스트에서 현재 선택된 인덱스를 가져와야
    index = pattern_list.curselection()
    # 리스트박스에 들어있는 요소 중에서 index에 해당되는 요소
    pattern = pattern_list.get(index)
    # 엔트리의 텍스트로 설정
    pattern_var.set(pattern)

pattern_list.bind('<<ListboxSelect>>', set_pattern)















def stop(event=None):
    window.quit()

window.bind('<Escape>', stop)
window.mainloop()   # 기본 메인루프
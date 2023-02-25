# import win32api
#
# drives = win32api.GetLogicalDriveStrings()
# drives = drives.split('\000')[:-1]
# print(drives)

import os
# import string
# from ctypes import windll
#
# def get_drives():
#     drives = []
#     bitmask = windll.kernel32.GetLogicalDrives()
#     for letter in string.ascii_uppercase:
#         if bitmask & 1:
#             drives.append(letter)
#         bitmask >>= 1
#     return drives
#
# if (name == 'main'):
#     print(get_drives())     # On my PC, this prints ['A', 'C', 'D', 'F', 'H']

# available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
# print(available_drives)

drives = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
print(os.getcwd())
print(drives)

from tkinter import *
from tkinter import ttk
 
 
# удаление выделенного элемента
def select():
    selection = file_listbox.curselection()
    # мы можем получить удаляемый элемент по индексу
    selected_language = file_listbox.get(selection[0])
    # print(selected_language)
    # print(file_listbox.size())
    for root, dirs, files in os.walk(cur_dir):
        # print(root)
        for _dir in dirs:
            print(_dir)
    
        for _file in files:
            print(_file)
    
 
# добавление нового элемента
def add():
    new_language = language_entry.get()
    file_listbox.insert(0, new_language)
 
root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")
root.columnconfigure(index=0, weight=4)
root.columnconfigure(index=1, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=3)
root.rowconfigure(index=2, weight=1)
 
# текстовое поле и кнопка для добавления в список
language_entry = ttk.Entry()
language_entry.grid(column=0, row=0, padx=6, pady=6, sticky=EW)
ttk.Button(text="Добавить", command=add).grid(column=1, row=0, padx=6, pady=6)
 
# создаем список
cur_dir = os.getcwd()
cur_list = os.listdir(cur_dir)
list_var = Variable(value=cur_list)
file_listbox = Listbox(listvariable=list_var)
file_listbox.grid(row=1, column=0, columnspan=2, sticky=EW, padx=5, pady=5)
 
# добавляем в список начальные элементы
# file_listbox.insert(END, "Python")
# file_listbox.insert(END, "C#")
 
ttk.Button(text="Перейти в папку", command=select).grid(row=2, column=1, padx=5, pady=5)
 
root.mainloop()

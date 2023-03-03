import os
from tkinter import *
from tkinter import ttk


def get_abspath(dir, name = ''):
    return os.path.abspath(dir + '/' + name)

def search_file(path, name):
    for item in os.listdir(path):
        if item == name and os.path.isfile(item):
            print('Name: ', name)
            print('Size: ', os.path.getsize(item))
            print('Path: ', os.path.abspath(item))
            return
        search_file(os.path.abspath(item), name)

def get_file_selected():
    selection = file_listbox.curselection()
    return file_listbox.get(selection[0])

def search():
    name = file_entry.get()

    if name == '':
        return

    selected = get_file_selected()
    search_file(set_cur_dir(selected), name)

def add(index, name):
    index += 1
    file_listbox.insert(index, name)
    return index

def set_cur_dir(dir):
    global cur_dir

    if dir in drives:
        cur_dir = get_abspath(dir)
    elif len(cur_dir) == 3 and dir == '..':
        cur_dir = ''
    else:
        path = get_abspath(cur_dir, dir)
        if not os.path.isdir(path):
            if os.path.isfile(path):
                print(os.path.getsize(path))
            return False
        cur_dir = path
    return True

def set_cur_list():
    global cur_list

    if cur_dir == '':
        cur_list = drives
    else:
        cur_list = ['..'] + os.listdir(cur_dir)

def select():
    selected = get_file_selected()
    print(selected)

    if not set_cur_dir(selected):
        return

    print(cur_dir)

    set_cur_list()
    file_listbox.delete(0, END)

    i = 0
    for item in cur_list:
        # if cur_dir == '' or os.path.isdir(get_abspath(cur_dir, item)):
            i = add(i, item)

    print(cur_list)
 
root = Tk()
root.title("METANIT.COM")
root.geometry("700x500")
root.columnconfigure(index=0, weight=4)
root.columnconfigure(index=1, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=3)
root.rowconfigure(index=2, weight=1)
 
# текстовое поле и кнопка для добавления в список
file_entry = ttk.Entry()
file_entry.grid(column=0, row=0, padx=6, pady=6, sticky=EW)
# ttk.Button(text="Добавить", command=add).grid(column=1, row=0, padx=6, pady=6)
 
drives = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]

# создаем список
cur_dir = ''
cur_list = drives
list_var = Variable(value=cur_list)
file_listbox = Listbox(listvariable=list_var)
file_listbox.grid(row=1, column=0, columnspan=2, sticky=EW, padx=5, pady=5)
 
# добавляем в список начальные элементы
# file_listbox.insert(END, "Python")
# file_listbox.insert(END, "C#")
 
ttk.Button(text="Перейти в папку", command=select).grid(row=2, column=1, padx=5, pady=5)

tree = ttk.Treeview()
# установка заголовка
tree.heading("#0", text="Отделы", anchor=NW)
tree.grid(row=1, column=2)
 
tree.insert("", END, iid=1, text="Административный отдел", open=True)
tree.insert("", END, iid=2, text="IT-отдел")
tree.insert("", END, iid=3, text="Отдел продаж")
 
tree.insert(1, index=END, text="Tom")
tree.insert(2, index=END, text="Bob")
tree.insert(2, index=END, text="Sam")

root.mainloop()

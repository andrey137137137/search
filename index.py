import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd


def show_message(str, type = 'w'):
    if type == 'i':
        return messagebox.showinfo('Сообщение', str)
    if type == 'w':
        return messagebox.showwarning('Предупреждение', str)
    messagebox.showerror('Ошибка', str)

def select_file_name():
    global file_name, file_size, file_mtime
    temp = fd.askopenfilename()
    file_name = os.path.basename(temp)
    file_size = os.path.getsize(temp)
    file_mtime = os.path.getmtime(temp)

def get_abspath(dir, name = ''):
    return os.path.abspath(os.path.join(dir, name))

def add_to_tree(index, text):
    if index == 0:
        id = ''
        iid = 1
    else:
        id = index
        iid = index + 1
    tree.insert(parent=id, index=END, iid=iid, text=text, open=True)

def build_tree(path):
    parts = path.split('\\')
    print(len(parts))

    for item in tree.get_children(''):
        tree.delete(item)

    add_to_tree(0, parts[0])

    i = 1
    while i < len(parts):
        add_to_tree(i, parts[i])
        i += 1

def search_file(root, name):
    global deep_counter
    print(deep_counter)
    print(root)
    if deep_counter >= deep:
        return
    try:
        for item in os.listdir(root):
            path = get_abspath(root, item)
            print(path)
            print(item)
            print(name)
            if item == name and os.path.isfile(path) and file_size == os.path.getsize(path) and file_mtime == os.path.getmtime(path):
                print('Name: ', name)
                print('Size: ', os.path.getsize(path))
                print('Path: ', os.path.abspath(path))
                show_message('Name: ' + name, 'i')
                build_tree(path)
                deep_counter = deep
                return
            if os.path.isdir(path):
                search_file(path, name)
    except:
        return
    finally:
        deep_counter += 1

def get_file_selected():
    selection = file_listbox.curselection()
    
    if len(selection) == 0:
        show_message('Выберите директорию')
        return ''

    return file_listbox.get(selection[0])

def search():
    global deep_counter

    if file_name == '':
        show_message('Выберите файл')
        return

    # selected = get_file_selected()

    # if not selected:
    #     return

    # set_cur_dir(selected)

    if not cur_dir:
        show_message('Директория не выбрана')
        return

    deep_counter = 0
    search_file(cur_dir, file_name)

def add(index, name):
    index += 1
    file_listbox.insert(index, name)
    return index

def get_path(root, dir):
    if dir in drives:
        return get_abspath(dir)

    if len(root) == 3 and dir == '..':
        return ''

    path = get_abspath(root, dir)

    if os.path.isfile(path):
        print(os.path.getsize(path))

    return path

def set_label_value(path):
    global label_value, cur_dir
    cur_dir = path
    label_value.set(path)

def set_cur_dir(dir):
    global cur_dir, prev_cur_dir

    # if dir in drives:
    #     cur_dir = get_abspath(dir)
    # elif len(cur_dir) == 3 and dir == '..':
    #     cur_dir = ''
    # else:
    #     path = get_abspath(cur_dir, dir)
    #     if not os.path.isdir(path):
    #         if os.path.isfile(path):
    #             print(os.path.getsize(path))
    #         return False
    #     cur_dir = path
    # return True

    path = get_path(cur_dir, dir)

    if not path == '' and not os.path.isdir(path):
        return False

    prev_cur_dir = cur_dir
    # cur_dir = path
    set_label_value(path)
    return True

def set_cur_list():
    global cur_dir, cur_list, prev_cur_list

    if cur_dir == '':
        cur_list = drives
    else:
        try:
            prev_cur_list = cur_list
            cur_list = ['..'] + os.listdir(cur_dir)
        except:
            show_message('Невозможно открыть директорию: ' + cur_dir, 'e')
            # cur_dir = prev_cur_dir
            set_label_value(prev_cur_dir)
            cur_list = prev_cur_list

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
root.columnconfigure(index=0, weight=0)
root.columnconfigure(index=1, weight=0)
root.columnconfigure(index=2, weight=3)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)
 
# текстовое поле и кнопка для добавления в список
file_select = ttk.Button(text="Выбрать файл", command=select_file_name).grid(column=0, row=0, padx=6, pady=6, sticky=EW)
# ttk.Button(text="Добавить", command=add).grid(column=1, row=0, padx=6, pady=6)

deep = 10
deep_counter = 0
drives = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]

# создаем список
file_size = 0
cur_dir = prev_cur_dir = file_name = ''
cur_list = prev_cur_list = drives
list_var = Variable(value=cur_list)
file_listbox = Listbox(listvariable=list_var)
file_listbox.grid(row=1, column=0, columnspan=2, sticky=EW, padx=5, pady=5)
 
# добавляем в список начальные элементы
# file_listbox.insert(END, "Python")
# file_listbox.insert(END, "C#")

label_value = StringVar(value=cur_dir)
ttk.Label(textvariable=label_value).grid(row=0, column=2)
ttk.Button(text="Перейти в папку", command=select).grid(row=2, column=1, padx=5, pady=5)
ttk.Button(text="Найти", command=search).grid(row=0, column=1, padx=5, pady=5)

tree = ttk.Treeview()
# установка заголовка
# tree.heading("#0", text="Отделы", anchor=NW)
tree.grid(row=1, column=2)
 
tree.insert("", END, iid=1, text="Административный отдел", open=True)
tree.insert("", END, iid=2, text="IT-отдел")
tree.insert("", END, iid=3, text="Отдел продаж")
 
tree.insert(1, index=END, text="Tom")
tree.insert(2, index=END, text="Bob")
tree.insert(2, index=END, text="Sam")

root.mainloop()

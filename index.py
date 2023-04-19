import shutil

from os import *
from os import path as p

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd


def show_message(str, type="w"):
    if type == "i":
        return mb.showinfo("Сообщение", str)
    if type == "w":
        return mb.showwarning("Предупреждение", str)
    mb.showerror("Ошибка", str)


def get_abspath(dir, name=""):
    return p.abspath(dir + "/" + name)


def add_to_tree(index, text):
    if index == 0:
        id = ""
        iid = 1
    else:
        id = index
        iid = index + 1
    tree.insert(parent=id, index=END, iid=iid, text=text, open=True)


def clean_tree():
    for item in tree.get_children(""):
        tree.delete(item)


def build_tree(path):
    parts = path.split("\\")
    print(len(parts))

    clean_tree()
    add_to_tree(0, parts[0])

    i = 1
    while i < len(parts):
        add_to_tree(i, parts[i])
        i += 1


def isOnDeep():
    return deep_counter >= deep.get()


def search_file(root, name):
    global deep_counter, is_found
    if isOnDeep():
        return
    try:
        print(deep_counter)
        print(root)
        for item in listdir(root):
            if isOnDeep():
                return
            path = get_abspath(root, item)
            print(path)
            print(item)
            print(name)
            if p.isfile(path):
                is_found = True
                if all([to_check_name.get(), not item == name]):
                    is_found = False
                if all(
                    [
                        is_found,
                        to_check_size.get(),
                        not file_size == p.getsize(path),
                    ]
                ):
                    is_found = False
                if all(
                    [
                        is_found,
                        to_check_mtime.get(),
                        not file_mtime == p.getmtime(path),
                    ]
                ):
                    is_found = False
                if is_found:
                    print("Name: ", name)
                    print("Size: ", p.getsize(path))
                    print("Mtime: ", p.getmtime(path))
                    # show_message("Name: " + item, "i")
                    build_tree(path)
                    deep_counter = deep.get()
                    return
            elif p.isdir(path):
                search_file(path, name)
    except:
        return
    finally:
        deep_counter += 1


# def test_file(path):
#     global file_name, file_size, file_mtime
#     file_name = p.basename(path)
#     file_size = p.getsize(path)
#     file_mtime = p.getmtime(path)
#     search()


def search(path):
    global file_name, file_size, file_mtime, deep_counter, is_found

    file_name = p.basename(path)
    file_size = p.getsize(path)
    file_mtime = p.getmtime(path)
    is_found = False
    deep_counter = 0
    search_file(cur_dir, file_name)

    if not is_found:
        clean_tree()
        shutil.copy2(path, cur_dir)
        # show_message("Файл " + file_name + " не найден")


def select_file_names():
    if all(
        [not to_check_name.get(), not to_check_size.get(), not to_check_mtime.get()]
    ):
        show_message("Необходимо выбрать как минимум один параметр сравнения")
        return

    # selected = get_file_selected()

    # if not selected:
    #     return

    # set_cur_dir(selected)

    if not cur_dir:
        show_message("Директория не выбрана")
        return

    file_names = fd.askopenfilenames()

    if len(file_names) == 0:
        show_message("Выберите один или несколько файлов")
        return

    for path in file_names:
        search(path)


def add(index, name):
    index += 1
    file_listbox.insert(index, name)
    return index


def get_path(root, dir):
    if dir in drives:
        print(dir)
        return get_abspath(dir)

    if len(root) == 3 and dir == "..":
        return ""

    path = get_abspath(root, dir)

    if p.isfile(path):
        print(p.getsize(path))

    return path


def set_label_value(path):
    global label_value, cur_dir
    cur_dir = path
    label_value.set(path)


def set_cur_dir(dir):
    global cur_dir, prev_cur_dir

    path = get_path(cur_dir, dir)
    print(path)

    if not path == "" and not p.isdir(path):
        return False

    prev_cur_dir = cur_dir
    set_label_value(path)
    return True


def set_cur_list():
    global cur_dir, cur_list, prev_cur_list

    if cur_dir == "":
        cur_list = drives
    else:
        try:
            prev_cur_list = cur_list
            cur_list = [".."] + listdir(cur_dir)
        except:
            show_message("Невозможно открыть директорию: " + cur_dir, "e")
            set_label_value(prev_cur_dir)
            cur_list = prev_cur_list


def get_file_selected():
    selection = file_listbox.curselection()

    if len(selection) == 0:
        show_message("Выберите директорию")
        return ""

    return file_listbox.get(selection[0])


def select():
    selected = get_file_selected()
    print(selected)

    if not selected:
        return

    if not set_cur_dir(selected):
        return

    print(cur_dir)

    set_cur_list()
    file_listbox.delete(0, END)

    i = 0
    for item in cur_list:
        if cur_dir == "" or p.isdir(get_abspath(cur_dir, item)):
            i = add(i, item)

    print(cur_list)


root = Tk()
root.title("SEARCH")
root.geometry("700x500")
ttk.Style().configure(
    ".", font="helvetica 13", foreground="#004D40", padding=8, background="#B2DFDB"
)
root.columnconfigure(index=0, weight=0)
root.columnconfigure(index=1, weight=0)
root.columnconfigure(index=2, weight=3)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)

file_select = ttk.Button(text="Выбрать файл", command=select_file_names).grid(
    column=0, row=0, padx=6, pady=6, sticky=EW
)

deep = IntVar(value=1000)
Entry(textvariable=deep).grid(row=2, column=2)

deep_counter = 0
is_found = False

drives = [chr(x) + ":" for x in range(65, 91) if p.exists(chr(x) + ":")]

file_size = 0
cur_dir = prev_cur_dir = file_name = ""
cur_list = prev_cur_list = drives
list_var = Variable(value=cur_list)

file_listbox = Listbox(listvariable=list_var)
file_listbox.grid(row=1, column=0, columnspan=2, sticky=EW, padx=5, pady=5)

label_value = StringVar(value=cur_dir)
ttk.Label(textvariable=label_value).grid(row=0, column=2)
ttk.Button(text="Перейти в папку", command=select).grid(row=2, column=1, padx=5, pady=5)
# ttk.Button(text="Найти", command=search).grid(row=0, column=1, padx=5, pady=5)

tree = ttk.Treeview()
# tree.heading("#0", text="Отделы", anchor=NW)
tree.grid(row=1, column=2)

tree.insert("", END, iid=1, text="Административный отдел", open=True)
tree.insert("", END, iid=2, text="IT-отдел")
tree.insert("", END, iid=3, text="Отдел продаж")

tree.insert(1, index=END, text="Tom")
tree.insert(2, index=END, text="Bob")
tree.insert(2, index=END, text="Sam")

to_check_name = IntVar()
ttk.Checkbutton(text="По имени", variable=to_check_name, state=ACTIVE).grid(
    row=3, column=0
)
to_check_size = IntVar()
ttk.Checkbutton(text="По размеру", variable=to_check_size).grid(row=3, column=1)
to_check_mtime = IntVar()
ttk.Checkbutton(text="По дате создания", variable=to_check_mtime).grid(row=3, column=2)
root.mainloop()

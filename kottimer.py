import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog

from datetime import datetime, timezone
import zipfile
import os
import zipfile
import pandas as pd
from io import BytesIO
import zipfile
import os
import os
import zipfile
import shutil
import json
data_f = 'output.json'
data = {}
if data_f in os.listdir():
    with open(data_f, 'r') as file:
        data = json.load(file)
else:
    data = {"a":"2023-02-12 12:51","b":"2023-02-12 12:51"}
    with open(data_f, 'w') as file:
        json.dump(data, file, indent=4)

print(data)

def zip_temp_folder(zip_filename):
    temp_folder = 'temp'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Проходим по всем файлам в папке temp
        for root, dirs, files in os.walk(temp_folder):
            for file in files:
                # Получаем полный путь к файлу
                file_path = os.path.join(root, file)
                # Добавляем файл в архив, сохраняя структуру папок
                zipf.write(file_path, os.path.relpath(file_path, temp_folder))

    # Очищаем папку temp
    shutil.rmtree(temp_folder)
    os.makedirs(temp_folder)  # Создаем папку temp заново, если нужно

# Пример использования

def extract_xmls(file_path, output_dir):

    # Убедимся, что выходная директория существует
    os.makedirs(output_dir, exist_ok=True)

    # Открываем ZIP-файл
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # Извлекаем все файлы
        zip_ref.extractall(output_dir)
        print(f"Содержимое {file_path} успешно извлечено в {output_dir}")



def get_current_time(input_time=None):
    if input_time:
        # Преобразуем входное время из строки в объект datetime
        local_time = datetime.strptime(input_time, '%Y-%m-%d %H:%M')
        # Переводим локальное время в UTC
        utc_time = local_time.replace(tzinfo=timezone.utc)
    else:
        # Получаем текущее время в UTC
        utc_time = datetime.now(timezone.utc)

    # Форматируем время в нужный формат
    formatted_time = utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return formatted_time


def ch_time_mody(path , create ,modi ,data):#меняет время в core.xml
    pos_time_index=[]
    with open(path,"r") as f:
        f = f.read().split(">")
        for i in f:
            if len(list(i))!=0:
                if list(i)[0].isdigit() == True:
                    pos_time_index.append(f.index(i))

        for i in pos_time_index:
            print(f[i])

        #смена create index1
        current_time = get_current_time(create) 
        f[pos_time_index[0]] = f"{current_time}</dcterms:created"
        data['a']=create
        #смена modificate index2
        current_time = get_current_time(modi) 
        data['b']=modi


        
        with open(data_f, 'w') as file:
            json.dump(data, file, indent=4)

        f[pos_time_index[1]] = f"{current_time}</dcterms:modified"
        for i in pos_time_index:
            print(f[i])                 
        return ">".join(f)


# Переменная для хранения списка файлов
file_storage = []

def on_drop(event):
    files = event.data.split()
    file_list.delete(0, tk.END)  # Очистить текущее содержимое
    for file in files:
        file_list.insert(tk.END, file)  # Добавить файлы в список





def apply_changes():
    global file_storage
    modification_date = modification_date_entry.get()
    creation_date = creation_date_entry.get()
    files = file_list.get(0, tk.END)

    # Сохранение списка файлов в переменной
    file_storage = list(files)
    file_storage = ["".join(i.split("{")) for i in file_storage]
    file_storage = ["".join(i.split("}")) for i in file_storage]
    file_storage = ["".join(list(i)) for i in file_storage]
    for i in file_storage:
        path =i
        extract_xmls(path, 'temp')
        new_core = ch_time_mody("temp/docProps/core.xml",creation_date,modification_date ,data)
        with open("temp/docProps/core.xml","w") as f:
            f.write(new_core)
        zip_temp_folder("new_time/"+path.split("/")[-1])


def clear_selection():
    file_list.delete(0, tk.END)  # Очистить список файлов
    global file_storage
    file_storage = []  # Очистить переменную для хранения файлов

def select_files():
    global file_storage
    # Открытие диалогового окна выбора файлов
    file_storage = filedialog.askopenfilenames(title="Выберите файлы")
    
    # Преобразование кортежа в список
    file_storage = list(file_storage)
    
    # Очистка Listbox перед добавлением новых файлов
    file_list.delete(0, tk.END)
    
    # Обработка выбранных файлов и добавление их в Listbox
    for path in file_storage:
        file_list.insert(tk.END, path)

def clear_selection():
    # Очистка выбора в Listbox
    file_list.delete(0, tk.END)


# Создание основного окна
root = tk.Tk()
root.title("Файловый менеджер")
root.geometry("400x400")
root.resizable(False, False)
# Поле для отображения выбранных файлов
file_list = tk.Listbox(root, selectmode=tk.MULTIPLE, width=100, height=10)
file_list.pack(pady=10)

# Поле для ввода даты изменения
modification_date_label = tk.Label(root, text="Дата изменения (YYYY-MM-DD):")
modification_date_label.pack()
modification_date_entry = tk.Entry(root)
modification_date_entry.pack(pady=5)
modification_date_entry.insert(0, data['a']) 

# Поле для ввода даты создания
creation_date_label = tk.Label(root, text="Дата создания (YYYY-MM-DD):")
creation_date_label.pack()
creation_date_entry = tk.Entry(root)
creation_date_entry.pack(pady=5)
creation_date_entry.insert(0, data['b']) 

# Кнопка применить изменения
apply_button = tk.Button(root, text="Применить изменения", command=apply_changes)
apply_button.pack(pady=5)

# Кнопка очистить выбор
clear_button = tk.Button(root, text="Очистить выбор", command=clear_selection)
clear_button.pack(pady=5)

# Кнопка для выбора файлов
select_button = tk.Button(root, text="Выбрать файлы", command=select_files)
select_button.pack()

# Запуск основного цикла
root.mainloop()
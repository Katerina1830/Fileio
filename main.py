from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import requests
from tkinter import messagebox as mb
import pyperclip #Автоматическое копирование ссылки в буфер обмена.
# Сначала установим pyperclip
import json #Сохранение в формате JSON
import os

history_file = 'upload_history.json'


def save_history(file_path, link):
    history = [] #список
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            history = json.load(f)

    history.append({"file_path": os.path.basename(file_path), "download_link": link})
    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)# 4-отступ


def upload():
    try:# обработка исключения try и except
        filepath = fd.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                #files = {'file': open(filepath, 'rb')} #редактируем эту строку
                # и получается она files = {'file': f}
                response = requests.post('https://file.io', files=files)
                response.raise_for_status()  # Проверка на ошибки HTTP
                link = response.json()['link']
                entry.delete(0, END)
                entry.insert(0, link)
                pyperclip.copy(link)# Копирование ссылки в буфер обмена
                save_history(filepath, link)
                mb.showinfo('Ссылка скопирована', f'Ссылка {link} успешно скопирована в буфер обмена')
    except Exception as e:
        mb.showerror('Ошибка', f'Произошла ошибка: {e}')


def show_history(): #показать всю историю
    if not os.path.exists(history_file):
        mb.showinfo("История", "История загрузок пуста")
        return

    # Создаем два лист  бокса
    files_listbox = Listbox(history_window, width=50, height=20)
    files_listbox.grid(row=0, column=0, padx=(10, 0), pady=10)

    links_listbox = Listbox(history_window, width=50, height=20)
    links_listbox.grid(row=0, column=1, padx=(0,10), pady=10)

    with open(history_file, "r") as file:
        history = json.load(f)
        for item in history:
            files_listbox.insert(END, item['file_path'])
            links_listbox.insert(END, item['download_link'])

window = Tk()
window.title("Сохранение файлов в облаке")
window.geometry("360x100")

button = ttk.Button(text="Загрузить файл", command=upload)
button.pack()


entry = ttk.Entry()
entry.pack()

history_button = ttk.Button(text="Показать Историю", command=show_history)
history_button.pack()

window.mainloop()
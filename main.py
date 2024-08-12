from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import requests
from tkinter import messagebox as mb
import pyperclip #Автоматическое копирование ссылки в буфер обмена.
# Сначала установим pyperclip

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
                mb.showinfo('Ссылка скопирована', f'Ссылка {link} успешно скопирована в буфер обмена')
    except Exception as e:
        mb.showerror('Ошибка', f'Произошла ошибка: {e}')


window = Tk()
window.title("Сохранение файлов в облаке")
window.geometry("360x100")

button = ttk.Button(text="Загрузить файл", command=upload)
button.pack()


entry = ttk.Entry()
entry.pack()

window.mainloop()
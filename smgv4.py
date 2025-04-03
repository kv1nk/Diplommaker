from tkinter import Tk, Button, Label, filedialog, messagebox, Text, Entry, colorchooser, Toplevel
from tkinter.ttk import Progressbar
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

# Функция для выбора фонового изображения
def select_background():
    global background_path
    background_path = filedialog.askopenfilename(
        title="Выберите фоновое изображение",
        filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")]
    )
    if background_path:
        for widget in root.winfo_children():
            if isinstance(widget, Label) and widget.cget("text").startswith("Выбран файл:"):
                widget.destroy()
        Label(root, text=f"Выбран файл: {os.path.basename(background_path)}").pack()

# Функция для открытия папки со шрифтами
def open_fonts_folder():
    fonts_folder = "C:/Windows/Fonts" if os.name == "nt" else "/usr/share/fonts"
    os.startfile(fonts_folder)  # Открываем папку со шрифтами

# Функция для подтверждения выбора шрифта
def confirm_font():
    global font_path
    font_path = font_entry.get()
    if os.path.isfile(font_path):
        for widget in root.winfo_children():
            if isinstance(widget, Label) and widget.cget("text").startswith("Выбран шрифт:"):
                widget.destroy()
        Label(root, text=f"Выбран шрифт: {os.path.basename(font_path)}").pack()
    else:
        messagebox.showerror("Ошибка", "Указанный файл шрифта не найден!")

# Функция для выбора цвета текста
def select_color():
    global text_color
    color = colorchooser.askcolor()[1]  # Возвращает HEX-код цвета
    if color:
        text_color = color
        for widget in root.winfo_children():
            if isinstance(widget, Label) and widget.cget("text").startswith("Выбран цвет:"):
                widget.destroy()
        Label(root, text=f"Выбран цвет: {text_color}", fg=text_color).pack()

# Функция для выбора папки сохранения
def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory(title="Выберите папку для сохранения дипломов")
    if output_folder:
        for widget in root.winfo_children():
            if isinstance(widget, Label) and widget.cget("text").startswith("Выбрана папка:"):
                widget.destroy()
        Label(root, text=f"Выбрана папка: {output_folder}").pack()

# Функция для обновления прогресс-бара
def update_progress(current, total):
    progress = int((current / total) * 100)
    progress_bar["value"] = progress
    progress_label.config(text=f"{progress}% ({current} из {total})")
    root.update_idletasks()  # Обновляем интерфейс

# Функция для предпросмотра и выбора позиции текста
def preview():
    if not background_path or not font_path:
        messagebox.showerror("Ошибка", "Выберите фоновое изображение и шрифт!")
        return

    # Открываем фоновое изображение
    try:
        background = Image.open(background_path)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть фоновое изображение: {e}")
        return

    # Создаем окно предпросмотра
    preview_window = Toplevel(root)
    preview_window.title("Предпросмотр и выбор позиции текста")
    preview_window.geometry("1280x720")

    # Масштабируем изображение до размеров окна с сохранением пропорций
    bg_width, bg_height = background.size
    window_width, window_height = 1280, 720
    ratio = min(window_width / bg_width, window_height / bg_height)
    new_width = int(bg_width * ratio)
    new_height = int(bg_height * ratio)
    resized_background = background.resize((new_width, new_height))  # Используем resize без указания метода

    # Конвертируем изображение для отображения в Tkinter
    img_tk = ImageTk.PhotoImage(resized_background)
    label = Label(preview_window, image=img_tk)
    label.image = img_tk  # Сохраняем ссылку на изображение
    label.pack()

    # Функция для выбора позиции текста (центр текста)
    def set_text_position(event):
        # Рассчитываем позицию текста относительно исходного изображения
        x = int(event.x / ratio)
        y = int(event.y / ratio)
        global text_position
        text_position = (x, y)
        messagebox.showinfo("Позиция выбрана", f"Центр текста будет на координатах: {x}, {y}")
        preview_window.destroy()  # Закрываем окно предпросмотра после выбора позиции

    # Привязываем клик мыши к выбору позиции
    label.bind("<Button-1>", set_text_position)

# Функция для предпросмотра и выбора цвета текста
def preview_color():
    if not background_path:
        messagebox.showerror("Ошибка", "Выберите фоновое изображение!")
        return

    # Открываем фоновое изображение
    try:
        background = Image.open(background_path)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть фоновое изображение: {e}")
        return

    # Создаем окно предпросмотра
    preview_window = Toplevel(root)
    preview_window.title("Предпросмотр и выбор цвета текста")
    preview_window.geometry("1280x720")

    # Масштабируем изображение до размеров окна с сохранением пропорций
    bg_width, bg_height = background.size
    window_width, window_height = 1280, 720
    ratio = min(window_width / bg_width, window_height / bg_height)
    new_width = int(bg_width * ratio)
    new_height = int(bg_height * ratio)
    resized_background = background.resize((new_width, new_height))  # Используем resize без указания метода

    # Конвертируем изображение для отображения в Tkinter
    img_tk = ImageTk.PhotoImage(resized_background)
    label = Label(preview_window, image=img_tk)
    label.image = img_tk  # Сохраняем ссылку на изображение
    label.pack()

    # Функция для выбора цвета текста с изображения
    def pick_color(event):
        x = int(event.x / ratio)
        y = int(event.y / ratio)
        color = background.getpixel((x, y))
        global text_color
        text_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        for widget in root.winfo_children():
            if isinstance(widget, Label) and widget.cget("text").startswith("Выбран цвет:"):
                widget.destroy()
        Label(root, text=f"Выбран цвет: {text_color}", fg=text_color).pack()
        preview_window.destroy()

    # Привязываем клик мыши к выбору цвета
    label.bind("<Button-1>", pick_color)

# Функция для генерации дипломов
def generate_diplomas():
    if not background_path or not font_path:
        messagebox.showerror("Ошибка", "Выберите фоновое изображение и шрифт!")
        return

    # Получаем список имен из текстового поля
    names_list = names_text.get("1.0", "end").strip().split("\n")
    if not names_list:
        messagebox.showerror("Ошибка", "Введите список имен!")
        return

    # Проверяем, выбрана ли папка для сохранения
    if not output_folder:
        messagebox.showerror("Ошибка", "Выберите папку для сохранения дипломов!")
        return

    # Открываем фоновое изображение
    try:
        background = Image.open(background_path)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть фоновое изображение: {e}")
        return

    # Общее количество имен
    total_names = len(names_list)

    # Проходим по каждому имени
    for i, name in enumerate(names_list, start=1):
        image = background.copy()
        draw = ImageDraw.Draw(image)

        # Настройки шрифта и текста
        try:
            name_font = ImageFont.truetype(font_path, int(font_size.get()))
            # Рассчитываем размер текста
            text_bbox = draw.textbbox((0, 0), name, font=name_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            # Корректируем позицию текста (центр)
            x = text_position[0] - text_width // 2
            y = text_position[1] - text_height // 2
            # Рисуем текст
            draw.text(
                (x, y),  # Используем скорректированную позицию
                name,
                font=name_font,
                fill=text_color
            )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при нанесении текста: {e}")
            return

        # Убираем недопустимые символы из имени файла
        valid_name = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
        if not valid_name:
            valid_name = f"diploma_{i}"  # Если имя пустое, используем запасное имя

        # Сохранение изображения с указанием расширения .png
        output_path = os.path.join(output_folder, f"{valid_name}.png")
        try:
            image.save(output_path)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл {output_path}: {e}")
            return

        # Обновляем прогресс-бар
        update_progress(i, total_names)

    messagebox.showinfo("Готово", "Дипломы успешно созданы!")

def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

    if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
        event.widget.event_generate("<<SelectAll>>")

# Создаем главное окно
root = Tk()
root.title("Генератор дипломов")
root.geometry("500x850")  # Увеличиваем высоту окна

# Переменные для хранения путей и параметров
background_path = None
font_path = None
text_color = "#000000"  # Черный цвет по умолчанию
text_position = (100, 100)  # Позиция текста по умолчанию
output_folder = None  # Папка для сохранения дипломов

# Поле для ввода списка имен
Label(root, text="Введите список имен (каждое имя с новой строки):").pack()
names_text = Text(root, height=10, width=50)
names_text.pack()

# Кнопка для загрузки списка имен из файла
def load_names():
    file_path = filedialog.askopenfilename(
        title="Выберите файл с именами",
        filetypes=[("Текстовые файлы", "*.txt")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            names_text.delete("1.0", "end")
            names_text.insert("1.0", file.read())

Button(root, text="Загрузить список имен из файла", command=load_names).pack(pady=10)

# Кнопка для выбора фонового изображения
Button(root, text="Выбрать фоновое изображение", command=select_background).pack(pady=10)

# Кнопка для открытия папки со шрифтами
Button(root, text="Открыть папку со шрифтами", command=open_fonts_folder).pack(pady=10)

# Поле для ввода пути к шрифту
Label(root, text="Введите путь к шрифту:").pack()
font_entry = Entry(root, width=50)
font_entry.insert(0, "C:/Windows/Fonts/calibri.ttf")  # Устанавливаем значение по умолчанию
font_entry.pack()

# Кнопка для подтверждения выбора шрифта
Button(root, text="Подтвердить выбор шрифта", command=confirm_font).pack(pady=10)

# Поле для выбора размера шрифта
Label(root, text="Размер шрифта:").pack()
font_size = Entry(root)
font_size.insert(0, "120")  # Значение по умолчанию
font_size.pack()

# Кнопка для выбора цвета текста
Button(root, text="Выбрать цвет текста", command=select_color).pack(pady=10)

# Кнопка для предпросмотра и выбора позиции текста
Button(root, text="Предпросмотр и выбор позиции текста", command=preview).pack(pady=10)

# Кнопка для предпросмотра и выбора цвета текста
Button(root, text="Предпросмотр и выбор цвета текста", command=preview_color).pack(pady=10)

# Кнопка для выбора папки сохранения
Button(root, text="Выбрать папку для сохранения", command=select_output_folder).pack(pady=10)

# Кнопка для генерации дипломов
Button(root, text="Создать дипломы", command=generate_diplomas).pack(pady=20)

# Прогресс-бар
progress_bar = Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Метка для отображения прогресса
progress_label = Label(root, text="0% (0 из 0)")
progress_label.pack()

root.bind_all("<Key>", _onKeyRelease, "+")
# Запуск основного цикла
root.mainloop()
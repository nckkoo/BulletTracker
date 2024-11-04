import tkinter as tk

# Основные настройки окна
root = tk.Tk()
root.title("Bullet Tracker")
root.geometry("900x450")
root.configure(bg="black")

# Премиальные цвета для кнопок
colors = ["#F5F5F5", "#DC143C", "#2D2D2D"]  # Белый, мягкий красный и серый
bullet_states = [0] * 8  # Изначально все кнопки белые

# Шрифты и стиль
font_style = ("Helvetica Neue", 14, "bold")

# Создаем холст для рендеринга кнопок и рамку вокруг кнопок
canvas = tk.Canvas(root, width=800, height=250, bg="black", highlightthickness=2, highlightbackground="gray")
canvas.pack(pady=20)

# Список для хранения кнопок
bullets = []

# Функция для изменения состояния кнопки по клику или клавише
def toggle_bullet(index):
    bullet_states[index] = (bullet_states[index] + 1) % 3  # Переключаем состояние
    canvas.itemconfig(bullets[index]['circle'], fill=colors[bullet_states[index]])  # Меняем цвет круга

# Центрируем кнопки по горизонтали
start_x = 100  # Начальное положение для первой кнопки
button_spacing = 80  # Расстояние между кнопками

# Создаем круги с тенями и размещаем их по центру рамки
for i in range(8):
    x = start_x + i * button_spacing  # Расположение кнопок по горизонтали

    # Создаём "тень" под кнопкой
    shadow = canvas.create_oval(x+2, 102, x + 52, 152, fill="#1A1A1A", outline="")  

    # Создаём кнопку-круг с утонченным цветом и обводкой
    circle = canvas.create_oval(x, 100, x + 50, 150, fill=colors[0], outline="", width=0)

    # Центрируем текст и стиль
    text = canvas.create_text(x + 25, 125, text=str(i + 1), fill="#141414", font=font_style)

    # Объединяем элементы кнопки в один объект
    bullets.append({"circle": circle, "text": text})

    # Привязываем каждый элемент к функции клика и устанавливаем курсор "рука"
    canvas.tag_bind(circle, "<Button-1>", lambda event, idx=i: toggle_bullet(idx))
    canvas.tag_bind(text, "<Button-1>", lambda event, idx=i: toggle_bullet(idx))
    canvas.tag_bind(circle, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(circle, "<Leave>", lambda e: canvas.config(cursor=""))

# Функция сброса всех кнопок
def reset_bullets():
    for i in range(8):
        bullet_states[i] = 0  # Возвращаем кнопки в белое состояние
        canvas.itemconfig(bullets[i]['circle'], fill=colors[0])

# Кнопка RESET
reset_button = tk.Button(root, text="RESET", command=reset_bullets, font=font_style, bg="#DC143C", fg="white", relief="flat", cursor="hand2")
reset_button.pack(pady=10)

# Создаем перегородку (с зелёным цветом и высотой от верхней до нижней границы рамки)
separator = canvas.create_line(85, 10, 85, 240, fill="lime", width=3)


# Функции для перетаскивания перегородки
def start_move(event):
    canvas.bind("<Motion>", move_separator)
    canvas.config(cursor="hand2")  # Устанавливаем курсор "рука"

def stop_move(event):
    canvas.unbind("<Motion>")
    canvas.config(cursor="")  # Убираем курсор "рука"

def move_separator(event):
    x = event.x
    # Ограничиваем движение перегородки в пределах кнопок
    if 100 < x < 700:
        canvas.coords(separator, x, 10, x, 240)

# Привязываем события к перегородке
canvas.tag_bind(separator, "<Button-1>", start_move)
canvas.tag_bind(separator, "<ButtonRelease-1>", stop_move)
canvas.tag_bind(separator, "<Enter>", lambda e: canvas.config(cursor="hand2"))  # Курсор "рука" при наведении
canvas.tag_bind(separator, "<Leave>", lambda e: canvas.config(cursor=""))        # Сброс курсора при уходе

# Привязка клавиш Ctrl+1-8 и Ctrl+NumPad 1-8 для установки перегородки
def on_ctrl_key_press(event):
    if event.state & 0x4:  # Проверяем, что нажат Ctrl
        key_map = {
            "1": 165, "2": 245, "3": 325, "4": 405, "5": 485, "6": 565, "7": 645, "8": 725,
            "KP_1": 1765, "KP_2": 245, "KP_3": 325, "KP_4": 405, "KP_5": 485, "KP_6": 565, "KP_7": 645, "KP_8": 725
        }
        if event.keysym in key_map:
            # Перемещаем перегородку в указанное положение
            x = key_map[event.keysym]
            canvas.coords(separator, x, 10, x, 240)

# Привязка клавиш для переключения состояния кнопок 1-8 и нумпад
def on_key_press(event):
    key_map = {
        "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7,
        "KP_1": 0, "KP_2": 1, "KP_3": 2, "KP_4": 3, "KP_5": 4, "KP_6": 5, "KP_7": 6, "KP_8": 7
    }
    if event.keysym in key_map:
        toggle_bullet(key_map[event.keysym])

# Подключаем обработку событий клавиш к окну
root.bind("<KeyPress>", on_key_press)
root.bind("<Control-KeyPress>", on_ctrl_key_press)

root.mainloop()

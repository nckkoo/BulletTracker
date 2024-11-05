import tkinter as tk
import webbrowser
from pynput.keyboard import Key, Listener

root = tk.Tk()
root.title("Bullet Tracker")
root.geometry("900x450")
root.configure(bg="black")
root.resizable(False, False)

colors = ["#F5F5F5", "#DC143C", "#2D2D2D"]
bullet_states = [0] * 8
action_history = []
redo_history = []
global_hotkeys_enabled = False
listener = None
font_style = ("Helvetica Neue", 14, "bold")

canvas = tk.Canvas(root, width=800, height=250, bg="black", highlightthickness=2, highlightbackground="gray")
canvas.pack(pady=20)

extra_circles_states = [[0] * 8 for _ in range(2)]
extra_circles = []

def toggle_extra_circle(row, col):
    extra_circles_states[row][col] = (extra_circles_states[row][col] + 1) % 3
    canvas.itemconfig(extra_circles[row][col], fill=colors[extra_circles_states[row][col]])

def set_extra_circles_color(row, count, color):
    for col in range(8):
        canvas.itemconfig(extra_circles[row][col], fill=color if col < count else colors[0])
        extra_circles_states[row][col] = colors.index(color) if col < count else 0

extra_circle_size = 16
start_x = 250
for row in range(2):
    row_circles = []
    for col in range(8):
        x = start_x + col * (extra_circle_size * 2 + 10)
        y = 180 + row * (extra_circle_size * 2 + 10)
        circle = canvas.create_oval(x, y, x + extra_circle_size, y + extra_circle_size, fill=colors[0], outline="")
        row_circles.append(circle)
        canvas.tag_bind(circle, "<Button-1>", lambda event, r=row, c=col: toggle_extra_circle(r, c))
        canvas.tag_bind(circle, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(circle, "<Leave>", lambda e: canvas.config(cursor=""))
    extra_circles.append(row_circles)

def reset_extra_circles():
    for row in range(2):
        for col in range(8):
            extra_circles_states[row][col] = 0
            canvas.itemconfig(extra_circles[row][col], fill=colors[0])

bullets = []
def toggle_bullet(index):
    action_history.append((index, bullet_states[index]))
    if len(action_history) > 8:
        action_history.pop(0)
    bullet_states[index] = (bullet_states[index] + 1) % 3
    canvas.itemconfig(bullets[index]['circle'], fill=colors[bullet_states[index]])
    redo_history.clear()

def reset_bullets():
    for i in range(8):
        bullet_states[i] = 0
        canvas.itemconfig(bullets[i]['circle'], fill=colors[0])
    canvas.coords(separator, 405, 45, 405, 120)
    update_last_key("SPACE (RESET)")

def update_last_key(text):
    last_key_label.config(text=f"LAST KEY: {text}")

start_x = 100
button_spacing = 80
for i in range(8):
    x = start_x + i * button_spacing
    shadow = canvas.create_oval(x + 2, 62, x + 52, 112, fill="#1A1A1A", outline="")
    circle = canvas.create_oval(x, 60, x + 50, 110, fill=colors[0], outline="", width=0)
    text = canvas.create_text(x + 25, 85, text=str(i + 1), fill="#141414", font=font_style)
    bullets.append({"circle": circle, "text": text})
        # Enable clicking on each main circle to change its color
    canvas.tag_bind(circle, "<Button-1>", lambda event, idx=i: toggle_bullet(idx))
    canvas.tag_bind(text, "<Button-1>", lambda event, idx=i: toggle_bullet(idx))
        # Set cursor to hand when hovering over the circle
    canvas.tag_bind(circle, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(circle, "<Leave>", lambda e: canvas.config(cursor=""))
    canvas.tag_bind(text, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(text, "<Leave>", lambda e: canvas.config(cursor=""))

def toggle_hotkeys():
    global global_hotkeys_enabled
    if not global_hotkeys_enabled:
        hotkey_button.config(bg="white", fg="black")
        enable_global_hotkeys()
        global_hotkeys_enabled = True
        update_last_key("GH ENABLED")
    else:
        hotkey_button.config(bg="#DC143C", fg="white")
        disable_global_hotkeys()
        global_hotkeys_enabled = False
        update_last_key("GH DISABLED")
        bind_local_hotkeys()  # Бинд локальных хоткеев при выключении GH

def enable_global_hotkeys():
    global listener
    disable_local_hotkeys()  # Убираем локальные хоткеи
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.ctrl_pressed = False
    listener.alt_pressed = False
    listener.shift_pressed = False
    listener.start()

def on_press(key):
    is_focused = root.focus_get() is not None
    global_mode = global_hotkeys_enabled or is_focused

    if key in [Key.ctrl_l, Key.ctrl_r]:
        listener.ctrl_pressed = True
    if key in [Key.alt_l, Key.alt_r]:
        listener.alt_pressed = True
    if key in [Key.shift_l, Key.shift_r]:
        listener.shift_pressed = True

    if hasattr(key, 'vk') and 49 <= key.vk <= 56:
        number_pressed = key.vk - 48
        if listener.ctrl_pressed and listener.alt_pressed:
            update_last_key(f"CTRL+ALT+{number_pressed}")
            set_extra_circles_color(1, number_pressed, colors[2])
        elif listener.alt_pressed:
            update_last_key(f"ALT+{number_pressed}")
            set_extra_circles_color(0, number_pressed, colors[1])
        elif listener.ctrl_pressed:
            update_last_key(f"CTRL+{number_pressed}")
            position_separator(number_pressed - 1)
        elif not listener.alt_pressed and not listener.ctrl_pressed:
            update_last_key(f"{number_pressed}")
            toggle_bullet(number_pressed - 1)

    elif key == Key.space:
        update_last_key("SPACE")
        reset_all()

def on_release(key):
    if key in [Key.ctrl_l, Key.ctrl_r]:
        listener.ctrl_pressed = False
    if key in [Key.alt_l, Key.alt_r]:
        listener.alt_pressed = False
    if key in [Key.shift_l, Key.shift_r]:
        listener.shift_pressed = False

def disable_global_hotkeys():
    global listener
    if listener:
        listener.stop()
        listener = None

def reset_all():
    reset_bullets()
    reset_extra_circles()

separator = canvas.create_line(405, 45, 405, 120, fill="lime", width=10)

def position_separator(index):
    separator_positions = [165, 245, 325, 405, 485, 565, 645, 725]
    canvas.coords(separator, separator_positions[index], 45, separator_positions[index], 120)
    update_last_key(f"CTRL+{index + 1}")

def start_move(event):
    canvas.bind("<Motion>", move_separator)
    canvas.config(cursor="hand2")

def stop_move(event):
    canvas.unbind("<Motion>")
    canvas.config(cursor="")

def move_separator(event):
    x = event.x
    if 10 < x < 790:
        canvas.coords(separator, x, 10, x, 240)

hotkeys1 = [
    ("             1 2 3 4 5 6 7 8", "|   COUNT SHELLS"),
    ("CTRL + 1 2 3 4 5 6 7 8", "|   MOVE SEPARATOR")
]

hotkeys2 = [
    ("ALT + 1 2 3 4 5 6 7 8", "|   COUNT LIVE SHELLS"),
    ("CTRL + ALT + 1 2 3 4 5 6 7 8", "|   COUNT BLANK SHELLS")
]

canvas.tag_bind(separator, "<Button-1>", start_move)
canvas.tag_bind(separator, "<ButtonRelease-1>", stop_move)
canvas.tag_bind(separator, "<Enter>", lambda e: canvas.config(cursor="hand2"))
canvas.tag_bind(separator, "<Leave>", lambda e: canvas.config(cursor=""))

bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

credit_text = tk.Label(bottom_frame, text="DEVELOPED BY NIKITA KOVALENKO", font=("Helvetica", 10), fg="gray", bg="black", anchor="w")
credit_text.grid(row=0, column=0, sticky="w", padx=(10, 0))

SPACE_text = tk.Label(root, text="SPACE", font=("Helvetica", 10), bg="black", fg="gray", relief="flat")
SPACE_text.place(x=400, y=335, width=100, height=40)

hotkey_button = tk.Button(root, text="GLOBAL HOTKEYS", command=toggle_hotkeys, font=font_style, bg="#DC143C", fg="white", relief="flat", cursor="hand2")
hotkey_button.place(x=350, y=400, width=200, height=40)

reset_button = tk.Button(root, text="RESET", command=reset_all, font=font_style, bg="#DC143C", fg="white", relief="flat", cursor="hand2")
reset_button.place(x=400, y=300, width=100, height=40)

last_key_label = tk.Label(bottom_frame, text="LAST KEY: NONE", font=("Helvetica", 10), fg="gray", bg="black", anchor="e")
last_key_label.grid(row=0, column=2, sticky="e", padx=(0, 10))

bottom_frame.grid_columnconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(1, weight=1)
bottom_frame.grid_columnconfigure(2, weight=1)

contact_text = tk.Label(bottom_frame, text="CONTACT", font=("Helvetica", 10), fg="gray", bg="black", cursor="hand2")
contact_text.grid(row=1, column=0, sticky="w", padx=(10, 0))
contact_text.bind("<Button-1>", lambda e: webbrowser.open("https://www.t.me/backwoodshoneyberry"))

hotkeys_frame1 = tk.Frame(root, bg="black")
hotkeys_frame1.place(x=10, y=300)

hotkeys_frame2 = tk.Frame(root, bg="black")
hotkeys_frame2.place(x=610, y=300)

for index, (key_combo, description) in enumerate(hotkeys1):
    key_label = tk.Label(hotkeys_frame1, text=f"{key_combo} ", font=("Helvetica", 8), fg="gray", bg="black", anchor="w")
    desc_label = tk.Label(hotkeys_frame1, text=description, font=("Helvetica", 8), fg="gray", bg="black", anchor="w")
    
    key_label.grid(row=index, column=0, sticky="w", padx=0)
    desc_label.grid(row=index, column=1, sticky="w", padx=0)

for index, (key_combo, description) in enumerate(hotkeys2):
    key_label = tk.Label(hotkeys_frame2, text=f"{key_combo} ", font=("Helvetica", 8), fg="gray", bg="black", anchor="w")
    desc_label = tk.Label(hotkeys_frame2, text=description, font=("Helvetica", 8), fg="gray", bg="black", anchor="w")
    
    key_label.grid(row=index, column=0, sticky="w", padx=0)
    desc_label.grid(row=index, column=1, sticky="w", padx=0)




def bind_local_hotkeys():
    root.bind("<KeyPress-1>", lambda e: (toggle_bullet(0), update_last_key("1")))
    root.bind("<KeyPress-2>", lambda e: (toggle_bullet(1), update_last_key("2")))
    root.bind("<KeyPress-3>", lambda e: (toggle_bullet(2), update_last_key("3")))
    root.bind("<KeyPress-4>", lambda e: (toggle_bullet(3), update_last_key("4")))
    root.bind("<KeyPress-5>", lambda e: (toggle_bullet(4), update_last_key("5")))
    root.bind("<KeyPress-6>", lambda e: (toggle_bullet(5), update_last_key("6")))
    root.bind("<KeyPress-7>", lambda e: (toggle_bullet(6), update_last_key("7")))
    root.bind("<KeyPress-8>", lambda e: (toggle_bullet(7), update_last_key("8")))

    root.bind("<Alt-KeyPress-1>", lambda e: (set_extra_circles_color(0, 1, colors[1]), update_last_key("ALT+1")))
    root.bind("<Alt-KeyPress-2>", lambda e: (set_extra_circles_color(0, 2, colors[1]), update_last_key("ALT+2")))
    root.bind("<Alt-KeyPress-3>", lambda e: (set_extra_circles_color(0, 3, colors[1]), update_last_key("ALT+3")))
    root.bind("<Alt-KeyPress-4>", lambda e: (set_extra_circles_color(0, 4, colors[1]), update_last_key("ALT+4")))
    root.bind("<Alt-KeyPress-5>", lambda e: (set_extra_circles_color(0, 5, colors[1]), update_last_key("ALT+5")))
    root.bind("<Alt-KeyPress-6>", lambda e: (set_extra_circles_color(0, 6, colors[1]), update_last_key("ALT+6")))
    root.bind("<Alt-KeyPress-7>", lambda e: (set_extra_circles_color(0, 7, colors[1]), update_last_key("ALT+7")))
    root.bind("<Alt-KeyPress-8>", lambda e: (set_extra_circles_color(0, 8, colors[1]), update_last_key("ALT+8")))

    root.bind("<Control-Alt-KeyPress-1>", lambda e: (set_extra_circles_color(1, 1, colors[2]), update_last_key("CTRL+ALT+1")))
    root.bind("<Control-Alt-KeyPress-2>", lambda e: (set_extra_circles_color(1, 2, colors[2]), update_last_key("CTRL+ALT+2")))
    root.bind("<Control-Alt-KeyPress-3>", lambda e: (set_extra_circles_color(1, 3, colors[2]), update_last_key("CTRL+ALT+3")))
    root.bind("<Control-Alt-KeyPress-4>", lambda e: (set_extra_circles_color(1, 4, colors[2]), update_last_key("CTRL+ALT+4")))
    root.bind("<Control-Alt-KeyPress-5>", lambda e: (set_extra_circles_color(1, 5, colors[2]), update_last_key("CTRL+ALT+5")))
    root.bind("<Control-Alt-KeyPress-8>", lambda e: (set_extra_circles_color(1, 8, colors[2]), update_last_key("CTRL+ALT+8")))
    root.bind("<Control-Alt-KeyPress-6>", lambda e: (set_extra_circles_color(1, 6, colors[2]), update_last_key("CTRL+ALT+6")))
    root.bind("<Control-Alt-KeyPress-7>", lambda e: (set_extra_circles_color(1, 7, colors[2]), update_last_key("CTRL+ALT+7")))

    root.bind("<Control-KeyPress-1>", lambda e: (position_separator(0), update_last_key("CTRL+1")))
    root.bind("<Control-KeyPress-2>", lambda e: (position_separator(1), update_last_key("CTRL+2")))
    root.bind("<Control-KeyPress-3>", lambda e: (position_separator(2), update_last_key("CTRL+3")))
    root.bind("<Control-KeyPress-4>", lambda e: (position_separator(3), update_last_key("CTRL+4")))
    root.bind("<Control-KeyPress-5>", lambda e: (position_separator(4), update_last_key("CTRL+5")))
    root.bind("<Control-KeyPress-6>", lambda e: (position_separator(5), update_last_key("CTRL+6")))
    root.bind("<Control-KeyPress-7>", lambda e: (position_separator(6), update_last_key("CTRL+7")))
    root.bind("<Control-KeyPress-8>", lambda e: (position_separator(7), update_last_key("CTRL+8")))

    root.bind("<space>", lambda e: (reset_all(), update_last_key("SPACE (RESET)")))


def disable_local_hotkeys():
    for i in range(8):
        root.unbind(f"{i+1}")
        root.unbind(f"<Alt-KeyPress-{i+1}>")
        root.unbind(f"<Control-Alt-KeyPress-{i+1}>")
        root.unbind(f"<Control-KeyPress-{i+1}>")
    root.unbind("<space>")

bind_local_hotkeys()
root.mainloop()

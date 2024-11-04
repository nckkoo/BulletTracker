import tkinter as tk

# Main window settings
root = tk.Tk()
root.title("Bullet Tracker")  # Title of the window
root.geometry("900x450")      # Size of the window
root.configure(bg="black")     # Background color of the window
root.resizable(False, False)   # Disable window resizing

# Button colors for different states: white (default), red (active), dark gray (disabled)
colors = ["#F5F5F5", "#DC143C", "#2D2D2D"]
bullet_states = [0] * 8  # Initial states for each bullet button (all set to default)
action_history = []  # Stack for storing history of actions (up to 8)
redo_history = []  # Stack for redo actions

# Font style used for button text and labels
font_style = ("Helvetica Neue", 14, "bold")

# Canvas creation with a gray border
canvas = tk.Canvas(root, width=800, height=250, bg="black", highlightthickness=2, highlightbackground="gray")
canvas.pack(pady=20)

# List to store button objects for easy reference
bullets = []

# Function to toggle button state (0 -> 1 -> 2 -> 0) on click or key press
def toggle_bullet(index):
    # Save the current state for Undo purposes
    action_history.append((index, bullet_states[index]))
    if len(action_history) > 8:  # Limit history to 8 entries
        action_history.pop(0)

    bullet_states[index] = (bullet_states[index] + 1) % 3  # Cycle through states
    canvas.itemconfig(bullets[index]['circle'], fill=colors[bullet_states[index]])  # Change button color

    # Clear redo history as we made a new change
    redo_history.clear()

# Function to undo the last action
def undo_action(event=None):
    if action_history:
        index, previous_state = action_history.pop()
        redo_history.append((index, bullet_states[index]))  # Save current state to redo history
        bullet_states[index] = previous_state
        canvas.itemconfig(bullets[index]['circle'], fill=colors[previous_state])
        update_last_key("CTRL+Z (Undo)")

# Function to redo the last undone action
def redo_action(event=None):
    if redo_history:
        index, previous_state = redo_history.pop()
        action_history.append((index, bullet_states[index]))  # Save current state to action history
        bullet_states[index] = previous_state
        canvas.itemconfig(bullets[index]['circle'], fill=colors[previous_state])
        update_last_key("CTRL+SHIFT+Z (Redo)")

# Function to update the last key label
def update_last_key(text):
    last_key_label.config(text=f"LAST KEY: {text}")

# Horizontal layout parameters for bullet buttons
start_x = 100  # Initial x-coordinate for the first button
button_spacing = 80  # Space between buttons

# Creating bullet buttons as circles with shadow effect
for i in range(8):
    x = start_x + i * button_spacing  # Calculate x position for each button

    # Create shadow under each button
    shadow = canvas.create_oval(x + 2, 102, x + 52, 152, fill="#1A1A1A", outline="")

    # Create the main button circle with default color
    circle = canvas.create_oval(x, 100, x + 50, 150, fill=colors[0], outline="", width=0)

    # Centering the button label with the button number (1 to 8)
    text = canvas.create_text(x + 25, 125, text=str(i + 1), fill="#141414", font=font_style)

    # Store each button and label in bullets list for later access
    bullets.append({"circle": circle, "text": text})

    # Bind click events and cursor change to each button
    canvas.tag_bind(circle, "<Button-1>", lambda event, idx=i: toggle_bullet(idx))
    canvas.tag_bind(text, "<Button-1>", lambda event, idx=i: toggle_bullet(idx))
    canvas.tag_bind(circle, "<Enter>", lambda e: canvas.config(cursor="hand2"))  # Change cursor on hover
    canvas.tag_bind(circle, "<Leave>", lambda e: canvas.config(cursor=""))       # Reset cursor on exit

# Reset function to set all bullet buttons to the default state
def reset_bullets():
    for i in range(8):
        bullet_states[i] = 0  # Reset each button state
        canvas.itemconfig(bullets[i]['circle'], fill=colors[0])  # Reset color to default
    canvas.coords(separator, 405, 10, 405, 240)  # Reset separator to center position
    update_last_key("Space (RESET)")

# RESET button with red color
reset_button = tk.Button(root, text="RESET", command=reset_bullets, font=font_style, bg="#DC143C", fg="white", relief="flat", cursor="hand2")
reset_button.pack(pady=10)

# Creating a green separator line between bullet buttons
separator = canvas.create_line(85, 10, 85, 240, fill="lime", width=3)

# Functions for dragging the separator line horizontally
def start_move(event):
    canvas.bind("<Motion>", move_separator)
    canvas.config(cursor="hand2")  # Change cursor to hand

def stop_move(event):
    canvas.unbind("<Motion>")
    canvas.config(cursor="")  # Reset cursor when drag stops

def move_separator(event):
    x = event.x
    # Limit movement within canvas borders
    if 10 < x < 790:
        canvas.coords(separator, x, 10, x, 240)

# Bind separator events for dragging and cursor changes
canvas.tag_bind(separator, "<Button-1>", start_move)
canvas.tag_bind(separator, "<ButtonRelease-1>", stop_move)
canvas.tag_bind(separator, "<Enter>", lambda e: canvas.config(cursor="hand2"))  # Hand cursor on hover
canvas.tag_bind(separator, "<Leave>", lambda e: canvas.config(cursor=""))       # Reset cursor on exit

# Function for positioning separator using Ctrl+1-8 or NumPad keys
def on_ctrl_key_press(event):
    if event.state & 0x4:  # Check if Ctrl is pressed
        key_map = {
            "1": 165, "2": 245, "3": 325, "4": 405, "5": 485, "6": 565, "7": 645, "8": 725,
            "KP_1": 165, "KP_2": 245, "KP_3": 325, "KP_4": 405, "KP_5": 485, "KP_6": 565, "KP_7": 645, "KP_8": 725
        }
        if event.keysym in key_map:
            # Move the separator to the specified position
            x = key_map[event.keysym]
            canvas.coords(separator, x, 10, x, 240)
            update_last_key(f"CTRL+{event.keysym}")

# Function to toggle bullet states using keys 1-8 or NumPad
def on_key_press(event):
    key_map = {
        "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7,
        "KP_1": 0, "KP_2": 1, "KP_3": 2, "KP_4": 3, "KP_5": 4, "KP_6": 5, "KP_7": 6, "KP_8": 7
    }
    if event.keysym in key_map:
        toggle_bullet(key_map[event.keysym])
        update_last_key(event.keysym)

# Bind spacebar to trigger the RESET function
root.bind("<space>", lambda event: reset_bullets())

# Bind key events for bullet toggling and separator positioning
root.bind("<KeyPress>", on_key_press)
root.bind("<Control-KeyPress>", on_ctrl_key_press)
root.bind("<Control-z>", undo_action)  # Bind CTRL+Z for undo
root.bind("<Control-Shift-Z>", redo_action)  # Bind CTRL+SHIFT+Z for redo

# Create a frame to hold both labels in the bottom row
bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)  # Padding around the entire frame

# Developer credit label on the left
credit_text = tk.Label(bottom_frame, text="DEVELOPED BY NIKITA KOVALENKO", font=("Helvetica", 10), fg="gray", bg="black", anchor="w")
credit_text.pack(side="left", padx=(9.5, 9.5), pady=5)  # Padding to the right and top/bottom

# Last key label on the right
last_key_label = tk.Label(bottom_frame, text="LAST KEY: NONE", font=("Helvetica", 10), fg="gray", bg="black", anchor="e")
last_key_label.pack(side="right", padx=(9.5, 9.5), pady=5)  # Padding to the left and top/bottom

root.mainloop()

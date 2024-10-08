import tkinter as tk
from tkinter import messagebox
import math
from pypresence import Presence
import time
import pygame
import os
import json
import threading
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

print("Give us a moment, we are starting up...")
print("Started! Have fun controlling!")
pygame.mixer.init()

def play_startup_sound():
    try:
        pygame.mixer.music.load("startup.mp3")
        pygame.mixer.music.set_volume(100.0)
        pygame.mixer.music.play()
    except Exception as e:
        logging.error("Error in play_startup_sound: %s", str(e))

def show_guide():
    guide_message = """
    Welcome to Vector24!

    1. **Drawing a Vector**: Left-click and hold to start drawing a line, and the heading will be displayed.
    2. **Permanent Line (Approach Lines)**: Right-click and hold to start drawing a line to make the line permanent. This is useful for making ILS Runway Lines for approaches
    3. **Clear All Lines**: Double right-click anywhere on the canvas.
    4. **Discord Rich Presence**: Your drawing activity will appear on your Discord profile (if enabled).
    5. **Selecting ATC Positions**: Navigate to the "Position" menu to choose your ATC position from a list of available airports.

    Enjoy using the tool!
    """
    messagebox.showinfo("Guide to Vector24", guide_message)

def check_first_run():
    config_file = "config.json"
    try:
        if not os.path.exists(config_file):
            with open(config_file, "w") as f:
                json.dump({"first_run": True, "discord_rpc_enabled": True, "atc_position": "Tower"}, f)
            return True, True, "Tower"
        else:
            with open(config_file, "r") as f:
                config_data = json.load(f)
                return config_data.get("first_run", True), config_data.get("discord_rpc_enabled", True), config_data.get("atc_position", "Tower")
    except Exception as e:
        logging.error("Error in check_first_run: %s", str(e))
        return True, True, "Tower"

def update_config():
    config_file = "config.json"
    try:
        with open(config_file, "w") as f:
            json.dump({
                "first_run": False,
                "discord_rpc_enabled": discord_rpc_enabled.get(),
                "atc_position": atc_position
            }, f)
    except Exception as e:
        logging.error("Error in update_config: %s", str(e))

client_id = '1292041649945444402'
rpc = Presence(client_id)
rpc_connected = False

def connect_rpc():
    global rpc_connected
    if discord_rpc_enabled.get():
        try:
            rpc.connect()
            rpc_connected = True
        except Exception as e:
            logging.error("Error in connect_rpc: %s", str(e))
            rpc_connected = False

def update_discord_presence(heading):
    if discord_rpc_enabled.get() and rpc_connected:
        try:
            rpc.update(
                state=f"Directing a plane to heading {heading}°" if atc_position else "No position selected",
                details=f"Vectoring aircraft on {atc_position}" if atc_position else "No position selected",
                large_image="logo",
                large_text="Made by aerosd and awdev_",
                start=time.time()
            )
        except Exception as e:
            logging.error("Error in update_discord_presence: %s", str(e))

def update_heading(event, is_right_click=False):
    try:
        if is_mouse_pressed:
            mouse_x, mouse_y = event.x, event.y
            dx = mouse_x - start_x
            dy = start_y - mouse_y
            angle = math.atan2(dy, dx)
            heading = (math.degrees(angle) + 360) % 360
            heading = (90 - heading) % 360
            rounded_heading = round(heading / 5) * 5
            if rounded_heading == 0:
                rounded_heading = 360
            heading_label.config(text=f"Heading: {int(rounded_heading):03d}")
            canvas.coords(current_line, start_x, start_y, mouse_x, mouse_y)
            update_discord_presence(rounded_heading)
    except Exception as e:
        logging.error("Error in update_heading: %s", str(e))
        
def update_preview_line(event):
    global preview_line
    try:
        if is_mouse_pressed and preview_line:
            mouse_x, mouse_y = event.x, event.y
            canvas.coords(preview_line, start_x, start_y, mouse_x, mouse_y)
            update_heading(event, is_right_click=True)  # Update heading during right-click dragging
    except Exception as e:
        logging.error("Error in update_preview_line: %s", str(e))
        
def update_start_point(event):
    global start_x, start_y, is_mouse_pressed, current_line
    try:
        start_x, start_y = event.x, event.y
        is_mouse_pressed = True
        current_line = canvas.create_line(start_x, start_y, start_x, start_y)
    except Exception as e:
        logging.error("Error in update_start_point: %s", str(e))

def reset_line(event):
    global is_mouse_pressed, current_line
    try:
        is_mouse_pressed = False
        canvas.delete(current_line)
        current_line = None
    except Exception as e:
        logging.error("Error in reset_line: %s", str(e))

def start_right_drawing(event):
    global start_x, start_y, is_mouse_pressed, preview_line
    start_x, start_y = event.x, event.y
    is_mouse_pressed = True
    preview_line = canvas.create_line(start_x, start_y, start_x, start_y, fill="blue", dash=(4, 2))

def create_permanent_line(event):
    global is_mouse_pressed, preview_line
    try:
        if is_mouse_pressed:
            mouse_x, mouse_y = event.x, event.y
            canvas.create_line(start_x, start_y, mouse_x, mouse_y, fill="red")
            is_mouse_pressed = False
            if preview_line is not None:
                canvas.delete(preview_line)
                preview_line = None
            dx = mouse_x - start_x
            dy = start_y - mouse_y
            angle = math.atan2(dy, dx)
            heading = (math.degrees(angle) + 360) % 360
            heading = (90 - heading) % 360
            rounded_heading = round(heading / 5) * 5
            if rounded_heading == 0:
                rounded_heading = 360

            heading_label.config(text="Heading: {:.2f}".format(rounded_heading))
            update_discord_presence(rounded_heading)
    except Exception as e:
        logging.error("Error in create_permanent_line: %s", str(e))
        
def clear_all_lines(event):
    try:
        canvas.delete("all")
        heading_label.config(text="Heading: 0.00")
    except Exception as e:
        logging.error("Error in clear_all_lines: %s", str(e))

def update_presence_loop():
    if discord_rpc_enabled.get() and rpc_connected:
        try:
            rpc.update(state="Idle", details=f"ATC at {atc_position}", large_image="logo", large_text="Vector24")
        except Exception as e:
            logging.error("Error in update_presence_loop: %s", str(e))
    

    root.after(15000, update_presence_loop)

def load_positions(file_path):
    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data.get('airports', {})
    except Exception as e:
        logging.error("Error in load_positions: %s", str(e))
        return {}

def toggle_rpc():
    try:
        if discord_rpc_enabled.get():
            connect_rpc()
            presence_thread = threading.Thread(target=update_presence_loop, daemon=True)
            presence_thread.start()
        else:
            if rpc_connected:
                rpc.close()
        update_config()
    except Exception as e:
        logging.error("Error in toggle_rpc: %s", str(e))

def select_atc_position(position):
    global atc_position
    try:
        atc_position = position
        update_config()
    except Exception as e:
        logging.error("Error in select_atc_position: %s", str(e))

def on_close():
    try:
        config_file = "config.json"
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config_data = json.load(f)
            
            if "atc_position" in config_data:
                del config_data["atc_position"]

            with open(config_file, "w") as f:
                json.dump(config_data, f)

        if discord_rpc_enabled.get() and rpc_connected:
            rpc.close()

        root.destroy()
    except Exception as e:
        logging.error("Error in on_close: %s", str(e))

root = tk.Tk()
root.title("Vector24")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("410x400")

x_position = screen_width - 400 
y_position = screen_height - 300  
root.geometry("+{}+{}".format(x_position, y_position))

root.attributes("-alpha", 0.35)
root.attributes("-topmost", True)
root.overrideredirect(False)

heading_label = tk.Label(root, text="Heading: 0", bg="white", fg="black", font=("Comic Sans MS", 12))
heading_label.pack(pady=11)

separator_canvas = tk.Canvas(root, width=400, height=2, bg="gray")
separator_canvas.pack(fill="x")
separator_canvas.create_line(0, 1, 400, 1, fill="black")

canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack(expand=True, fill="both")
canvas.pack_propagate(False)

start_x = 200
start_y = 150
is_mouse_pressed = False

current_line = None
root.bind("<Motion>", update_heading)
root.bind("<Button-1>", update_start_point)
root.bind("<ButtonRelease-1>", reset_line)
root.bind("<Button-3>", create_permanent_line)
root.bind("<Double-Button-3>", clear_all_lines)
root.bind("<ButtonPress-3>", start_right_drawing) 
root.bind("<ButtonRelease-3>", create_permanent_line) 
root.bind("<B3-Motion>", update_preview_line)  # Update the heading during right-click dragging
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

options_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=options_menu)

discord_rpc_enabled = tk.BooleanVar(value=True)
options_menu.add_checkbutton(label="Toggle Discord RPC", onvalue=True, offvalue=False, variable=discord_rpc_enabled, command=toggle_rpc)

atc_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Position", menu=atc_menu)

positions = load_positions("positions.json")
for airport, positions_dict in positions.items():
    airport_menu = tk.Menu(atc_menu, tearoff=0)
    for airport_name, positions in positions_dict.items():
        tower_menu = tk.Menu(airport_menu, tearoff=0)
        for position, atc_code in positions.items():
            tower_menu.add_command(label=f"{position} ({atc_code})", command=lambda p=atc_code: select_atc_position(p))
        airport_menu.add_cascade(label=airport_name, menu=tower_menu)
    atc_menu.add_cascade(label=airport, menu=airport_menu)

first_run, rpc_status, atc_position = check_first_run()
discord_rpc_enabled.set(rpc_status)

if discord_rpc_enabled.get():
    connect_rpc()  
    root.after(15000, update_presence_loop)  


if first_run:
    show_guide()
    update_config()

play_startup_sound()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

if discord_rpc_enabled.get() and rpc_connected:
    rpc.close()

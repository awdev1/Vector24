import tkinter as tk
from tkinter import messagebox
import math
from pypresence import Presence
import time
import pygame
import os
import json


print("Give us a moment, we are starting up...")
pygame.mixer.init()

def play_startup_sound():
    pygame.mixer.music.load("startup.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

def show_guide():
    guide_message = """
    Welcome to the Vector24!

    1. **Drawing a Vector**: Left-click and hold to start drawing a line, and the heading will be displayed.
    2. **Permanent Line**: Right-click while holding the left-click to make the line permanent.
    3. **Clear All Lines**: Double right-click anywhere on the canvas.
    4. **Discord Rich Presence**: Your drawing activity will appear on your Discord profile (if enabled).
    5. **Keyboard Shortcuts**: No additional shortcuts are available, but you can use the mouse for all actions.

    Enjoy using the tool!
    """
    messagebox.showinfo("Guide to Vector24", guide_message)

def check_first_run():
    config_file = "config.json"
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            json.dump({"first_run": True, "discord_rpc_enabled": True}, f)  # Add discord_rpc_enabled flag
        return True, True
    else:
        with open(config_file, "r") as f:
            config_data = json.load(f)
            return config_data.get("first_run", True), config_data.get("discord_rpc_enabled", True)  # Return both

def update_first_run_status():
    config_file = "config.json"
    with open(config_file, "w") as f:
        json.dump({"first_run": False, "discord_rpc_enabled": discord_rpc_enabled}, f)  # Save status

start_x = 200
start_y = 150
is_mouse_pressed = False

client_id = '1292041649945444402'
rpc = Presence(client_id)

# Discord RPC will only connect if enabled
def connect_rpc():
    if discord_rpc_enabled:
        try:
            rpc.connect()
        except Exception as e:
            print(f"Error connecting to Discord: {e}")

def update_discord_presence(heading):
    if discord_rpc_enabled:
        try:
            rpc.update(
                state=f"Directing aircraft to heading {heading}°",
                details="Vectoring aircraft in ATC24",
                large_image="logo",
                large_text="Vector24",
                start=time.time()
            )
        except Exception as e:
            print(f"Error updating Discord Presence: {e}")

def update_heading(event):
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
        heading_label.config(text="Heading: {:.2f}".format(rounded_heading))
        canvas.coords(current_line, start_x, start_y, mouse_x, mouse_y)
        update_discord_presence(rounded_heading)

def update_start_point(event):
    global start_x, start_y, is_mouse_pressed, current_line
    start_x, start_y = event.x, event.y
    is_mouse_pressed = True
    current_line = canvas.create_line(start_x, start_y, start_x, start_y)

def reset_line(event):
    global is_mouse_pressed, current_line
    is_mouse_pressed = False
    canvas.delete(current_line)
    current_line = None

def create_permanent_line(event):
    global start_x, start_y
    mouse_x, mouse_y = event.x, event.y
    canvas.create_line(start_x, start_y, mouse_x, mouse_y)

def clear_all_lines(event):
    canvas.delete("all")
    heading_label.config(text="Heading: 0.00")

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

heading_label = tk.Label(root, text="Heading: 0.00")
heading_label.pack(pady=10)

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack(expand=True, fill="both")
canvas.pack_propagate(False)

current_line = None

root.bind("<Motion>", update_heading)
root.bind("<Button-1>", update_start_point)
root.bind("<ButtonRelease-1>", reset_line)
root.bind("<Button-3>", create_permanent_line)
root.bind("<Double-Button-3>", clear_all_lines)

# Update presence loop only runs if Discord RPC is enabled
def update_presence_loop():
    if discord_rpc_enabled:
        while True:
            rpc.update(state="Idle", details="No active vectoring", large_image="logo", large_text="Vector24",)
            time.sleep(15)

import threading

# Check if this is the user's first time and load Discord RPC settings
first_run, discord_rpc_enabled = check_first_run()

if discord_rpc_enabled:
    presence_thread = threading.Thread(target=update_presence_loop, daemon=True)
    presence_thread.start()
    connect_rpc()

if first_run:
    show_guide()
    update_first_run_status()

play_startup_sound()

root.mainloop()

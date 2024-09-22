import pygetwindow as gw
import os
import keyboard
import time
from threading import Thread, Event

cursor_char = '>' # character used for cursor

'''
    Please note: any window title on your computer that contains the string in WINDOW_TITLE 
        will make the python script think that you are on the menu and therefore supress 
        all other keyboard inputs! 

    For example, editing a script called "menu.py" and WINDOW_TITLE is set to "menu", 
        if the script is running then it will think you are still on the python window and supress other keyboard inputs
'''

WINDOW_TITLE = "example" # window title

# if the window is at default size or is too big then there will be noticable flickering since a bigger console is being cleared
WINDOW = 'mode 40,14' # window size

# menu structure & option names, create a new one for each menu
MAIN_MENU = [
    "example option",
    "change me",
    "random text",
    "quit program"
]

# event for when window is focused
focus_event = Event()

# main class for handling your menus
class Menu:
    def __init__(self, options, render_func):
        self.options = options
        self.cursor_index = 0
        self.render_func = render_func

    def render(self):
        cls()
        logo()
        self.render_func(self.cursor_index)

    def handle_input(self):
        if focus_event.is_set():
            key_event = keyboard.read_event(suppress=True)
            if key_event.event_type == keyboard.KEY_DOWN:
                if key_event.name == "down" and self.cursor_index < len(self.options) - 1:
                    self.cursor_index += 1
                elif key_event.name == "up" and self.cursor_index > 0:
                    self.cursor_index -= 1
                elif key_event.name == "enter":
                    return self.options[self.cursor_index]
        else:
            time.sleep(0.1)  # sleep so doesnt refresh as much can be changed however
        return None

# render the menu, create a new one for each menu
def render_main_menu(cursor_index):
    menuCursor = [' '] * len(MAIN_MENU)
    menuCursor[cursor_index] = cursor_char
    
    print(f"""
    {menuCursor[0]} {MAIN_MENU[0]}
    {menuCursor[1]} {MAIN_MENU[1]}
    {menuCursor[2]} {MAIN_MENU[2]}

    {menuCursor[3]} {MAIN_MENU[3]}""")    

# logic for menu options, create a new one for each menu
def main_menu():
    menu = Menu(MAIN_MENU, render_main_menu)
    while True:
        menu.render()
        selection = menu.handle_input()
        if selection:
            if selection == MAIN_MENU[0]:
                pass
            elif selection == MAIN_MENU[1]:
                pass
            elif selection == MAIN_MENU[2]:
                pass
            elif selection == MAIN_MENU[3]:
                exit()

# clear screen, crucial for this to work properly
def cls():
    os.system('CLS')

# optional, add a logo for the top of the menu
def logo():
    print("""
                             _     
     _____ ____ _ _ __  _ __| |___ 
    / -_) \ / _` | '  \| '_ \ / -_)
    \___/_\_\__,_|_|_|_| .__/_\___|
                       |_|         """)

# checks if the app is in focus
def is_app_in_focus():
    active_window = gw.getActiveWindow()
    return active_window and WINDOW_TITLE in active_window.title

# thread 2 check focus
def check_focus():
    while True:
        if is_app_in_focus():
            focus_event.set()
        else:
            focus_event.clear()
        time.sleep(0.1)

# "main" loop
def main():
    print('\033[?25l', end="") # hides cursor
    os.system('title ' + WINDOW_TITLE) # sets cmd title to value of WINDOW_TITLE
    os.system(WINDOW)

    # thread for checking if window is focused
    focus_thread = Thread(target=check_focus, daemon=True)
    focus_thread.start()

    main_menu()

# RUN
if __name__ == "__main__":
    main()
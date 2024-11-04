import tkinter as tk
from tkinter import messagebox
import os
import configparser
import threading
import subprocess

class Form1(tk.Tk):
    def __init__(self, config_file='/home/micael/code/menu/config.ini'):
        super().__init__()
        self.config_file = config_file
        self.load_config()

        self.title("Menu_2")
        self.overrideredirect(True) 
        self.configure(background=self.backgroundColor)

        # Create a frame for the menu bar with a fixed height
        self.menu_bar = tk.Menu(self, bg=self.menuBarColor, fg=self.textColor, relief=tk.FLAT)
        self.config(menu=self.menu_bar)

        self.populate_menu()

        # Adjust the window height to fit the menu bar and set starting position
        self.geometry(f"{self.menuWidth}x{self.menuHeight}+{self.start_x}+{self.start_y}")

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)

        settings = config['Settings']
        self.rootFolder = settings['rootFolder']
        self.menuWidth = int(settings['MenuWidth'])
        self.menuHeight = int(settings['MenuHeight'])
        self.textSize = int(settings['TextSize'])
        self.start_x = int(settings['Start_X-Position'])
        self.start_y = int(settings['Start_Y-Position'])
        self.backgroundColor = settings['backgroundColor']
        self.menuBarColor = settings['menuBarColor']
        self.dropDownMenuTextColor = settings['menuBar_DropDownButton_TextColor']
        self.textColor = settings['textColor']
        self.textColor_Inactive = settings['textColor_Inactive']
        self.borderColor = settings['borderColor']

    def populate_menu(self):
        for item in os.listdir(self.rootFolder):
            item_path = os.path.join(self.rootFolder, item)
            if os.path.isdir(item_path):
                folder_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.menuBarColor, fg=self.textColor, relief=tk.RAISED)
                self.menu_bar.add_cascade(label=item, menu=folder_menu)

                for sub_item in os.listdir(item_path):
                    sub_item_path = os.path.join(item_path, sub_item)
                    display_label = os.path.splitext(sub_item)[0]  # Remove file extension for display
                    folder_menu.add_command(label=display_label, command=lambda p=sub_item_path: self.open_item(p))
            elif os.path.isfile(item_path):
                display_label = os.path.splitext(item)[0]  # Remove file extension for display
                self.menu_bar.add_command(label=display_label, command=lambda p=item_path: self.open_item(p))

    def open_item(self, item_path):
        _, file_extension = os.path.splitext(item_path)
        try:
            if file_extension == '.txt':
                self.open_text_file(item_path)
            elif file_extension == '.sh':
                self.execute_sh_file(item_path)
            elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                self.open_image_file(item_path)
            else:
                self.open_with_default_application(item_path)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open item: {e}")

    def open_text_file(self, file_path):
        subprocess.Popen(['notepad', file_path])

    def execute_sh_file(self, file_path):
        if file_path.endswith('.sh'):
            self.set_executable_permission(file_path)
        
        threading.Thread(target=self.execute_sh_command, args=(file_path,)).start()

    def execute_sh_command(self, file_path):
        try:
            subprocess.Popen(['bash', file_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute .sh file: {e}")

    def set_executable_permission(self, file_path):
        try:
            os.chmod(file_path, 0o755)  
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set executable permissions: {e}")

    def open_image_file(self, file_path):
        try:
            subprocess.Popen(['xdg-open', file_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image file: {e}")

    def open_with_default_application(self, file_path):
        try:
            subprocess.Popen(['xdg-open', file_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

if __name__ == "__main__":
    app = Form1()
    app.mainloop()

# dir_config.py

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class dirconfig(metaclass=SingletonMeta):
    _image_data_dir = 'D://ImageData/'

    @classmethod
    def get_dir(cls):
        return cls._image_data_dir

    @classmethod
    def set_dir(cls, new_dir):
        cls._image_data_dir = new_dir

    @classmethod
    def open_folder_dialog(cls):
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            cls.set_dir(folder_path)
        root.destroy()

# 下面是单例实例的便捷访问点
dir_config = dirconfig()

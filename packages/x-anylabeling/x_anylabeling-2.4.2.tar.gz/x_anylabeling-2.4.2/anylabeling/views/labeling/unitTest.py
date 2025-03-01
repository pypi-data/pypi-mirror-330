import tkinter as tk
from tkinter import ttk

root = tk.Tk()
progress_var = tk.IntVar()  # 使用IntVar或DoubleVar来跟踪进度条的值

# 创建一个水平进度条
progress_bar = ttk.Progressbar(
    master=root,
    orient=tk.HORIZONTAL,  # 水平方向
    length=300,           # 长度为300像素
    mode='determinate',   # 确定模式
    maximum=100,          # 最大值为100
    value=0,              # 初始值为0
    variable=progress_var # 绑定到变量
)

progress_bar.pack(pady=20)

# 更新进度条的值
progress_var.set(50)  # 设置进度条的当前值为50

root.mainloop()

import tkinter as tk
import subprocess
from tkinter import font as tkfont


def start_program():
    # 运行另一个Python文件并捕获输出
    file_path = r'D:\software\标准上位机\Data\code\main.py'
    process = subprocess.Popen(['python', file_path], stdout=subprocess.PIPE)
    output, _ = process.communicate()

    # 在文本显示框中显示命令行输出
    text_box.insert(tk.END, output.decode() + '\n')


def clear_text():
    # 清空文本框内容
    text_box.delete("1.0", tk.END)


def close_window():
    # 关闭窗口
    window.destroy()


if __name__ == '__main__':
    # 创建主窗口
    window = tk.Tk()

    # 创建开始按钮
    start_button = tk.Button(window, text="analysis start", command=start_program)
    start_button.pack()

    # 创建清空按钮
    clear_button = tk.Button(window, text="clear all data", command=clear_text)
    clear_button.pack()

    # 创建关闭按钮
    close_button = tk.Button(window, text="close window", command=close_window)
    close_button.pack()

    # 创建文本显示框
    text_box = tk.Text(window)
    text_box.pack()

    # 设置文本框字体大小
    text_font = tkfont.Font(family='Arial', size=24)
    text_box.configure(font=text_font)

    # 运行主循环
    window.mainloop()

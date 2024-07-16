#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   remove_dup_jpg.py
@Time    :   2024/07/04 11:50:10
@Author  :   biolxy
@Version :   1.0
@Contact :   biolxy@aliyun.com
@Desc    :   None
'''

import shutil
from pathlib import Path
import hashlib
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
# from ttkbootstrap import Style


# 用于计算文件的MD5值
def calculate_md5(filepath: Path) -> str:
    hash_md5 = hashlib.md5()
    with filepath.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# 遍历当前目录及子目录下的所有.jpg文件，并计算MD5值
def traverse_and_calculate_md5(inputdir: Path) -> list[str]:
    md5_values = []
    for filepath in inputdir.rglob('*.jpg'):
        if any(part == 'need_remove' for part in filepath.parts):
            continue  # 跳过当前循环迭代
        md5_value = calculate_md5(filepath)
        md5_values.append(f"{md5_value}\t{filepath}")
    return md5_values


# 保存MD5值到md5.txt文件
def save_md5_values(infile, md5_values: list[str]) -> None:
    with open(infile, "w") as f:
        for v in md5_values:
            f.write(v + "\n")

def remove_dup_jpg(inputdir, outputdir):
    # 计算当前路径下的 .jpg 的 md5
    # root_dir = Path(".")  # 当前目录
    md5_values = traverse_and_calculate_md5(inputdir)
    save_md5_values(outputdir / "md5.txt", md5_values)

    # infile = "md5.txt"
    # df = pd.DataFrame(pd.read_csv(infile, encoding='utf-8', sep='\t', names=["md5", "filepath"]))
    # df.sort_values(by="md5")
    # print(df)
    # df.to_csv("md5.remove_dup.txt", encoding='utf-8', sep='\t', index=False)
    res = dict()
    for num, md5_str in enumerate(md5_values):
        md5_value, filepath = md5_str.split("\t")
        filepath = Path(filepath)
        if md5_value in res:
            # 目标文件夹路径
            # folder_path = Path('need_remove')
            # 如果文件夹不存在，则创建它
            # if not folder_path.exists():
            #     folder_path.mkdir(parents=True, exist_ok=True)

            folder_path = outputdir
            # 目标文件路径
            dst = folder_path / filepath.name

            # 如果目标文件已存在，则改名
            if dst.exists():
                # dst.unlink() # 删除
                # 改名
                dst = dst.with_name(f"{dst.name}_{num}").with_suffix('.jpg')
            shutil.move(filepath, dst)
        else:
            res[md5_value] = 1



class Application(tk.Tk):
    """
    ref: https://ttkbootstrap.readthedocs.io/en/version-0.5/gallery/simple_data_entry_form.html
    """
    def __init__(self):
        super().__init__()
        self.title('biolxy v0.03 | 图片去重工具')
        # self.style = Style('darkly')
        self.form = EntryForm(self)
        self.form.pack(fill='both', expand='yes')


class EntryForm(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=(30, 10))
        self.columnconfigure(3, weight=1)

        # form headers
        ttk.Label(self, text='请选择输入输出的文件夹路径(请做好备份)：\n本程序会将源文件夹中重复的jpg文件移动到冗余文件夹中', width=60).grid(columnspan=3, pady=10)
        # ttk.Labelframe(bootstyle="info")

        # 创建选择输入文件夹按钮
        self.input_btn = ttk.Button(self, text="源文件夹", command=self.select_input_folder)
        self.input_btn.grid(row=1, column=0, padx=20, pady=10, sticky='ew')

        # 显示选择的输入文件夹
        self.input_label = ttk.Label(self, text="请选择文件夹", style='info.TLabel')
        self.input_label.grid(row=1, column=1, padx=20, pady=10, sticky='ew')

        # 创建选择输出文件夹按钮
        self.output_btn = ttk.Button(self, text="冗余图片保存位置", command=self.select_output_folder)
        self.output_btn.grid(row=2, column=0, padx=20, pady=10, sticky='ew')

        # 显示选择的输出文件夹
        self.output_label = ttk.Label(self, text="请选择文件夹",style='info.TLabel')
        self.output_label.grid(row=2, column=1, padx=20, pady=10, sticky='ew')

        # submit button
        # self.submit = ttk.Button(self, text='确认执行', style='success.TButton', command=self.run_dedup)
        self.submit = ttk.Button(self, text='确认执行', style='success.TButton', command=self.run_dedup)
        self.submit.grid(row=3, column=0, sticky='ew', padx=20, pady=10)

        # cancel button
        self.cancel = ttk.Button(self, text='取消/退出', style='danger.TButton', command=self.quit)
        self.cancel.grid(row=3, column=1, sticky='ew')

    def print_form_data(self):
        print(self.input.get(), self.output.get())

    def run_dedup(self):
        if(self.confirm_selection()):
            remove_dup_jpg(Path(self.input_folder), Path(self.output_folder))
            self.show_finished_window()

    def show_finished_window(self):
        self.finished_window = tk.Toplevel(self)
        self.finished_window.title("执行状态")
        # 先设置窗口大小
        self.finished_window.geometry("150x100")
        # 然后立即居中窗口
        self.center_window(self.finished_window)
        self.status_label = tk.Label(self.finished_window, text="运行结束\n窗口将在3秒后关闭")

        self.status_label.pack(pady=10)

        # 启动倒计时
        self.countdown(3)

    def countdown(self, seconds):
        if seconds > 0:
            self.status_label.config(text=f"运行结束\n窗口将在{seconds}秒后关闭")
            self.finished_window.after(1000, self.countdown, seconds - 1)
        else:
            self.finished_window.destroy()

    def center_window(self, window):
        # 简单的居中窗口方法
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (window.winfo_width() / 2)
        y = (screen_height / 2) - (window.winfo_height() / 2)
        window.geometry(f'+{int(x)}+{int(y)}')  # 注意这里只设置了x和y位置，没有重复设置大小

    def select_input_folder(self):
        self.input_folder = filedialog.askdirectory()
        if self.input_folder:
            self.input_label.config(text=self.input_folder)
        else:
            self.input_label.config(text="请选择文件夹")

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.output_label.config(text=self.output_folder)
        else:
            self.output_label.config(text="请选择文件夹")

    def confirm_selection(self):
        status = False
        if hasattr(self, 'input_folder') and hasattr(self, 'output_folder'):
            if self.input_folder != "" and self.output_folder != "":
                status = True
        if status:
            return True
        else:
            messagebox.showwarning("Selection", "请选择输入输出文件夹")
            return False


if __name__ == "__main__":
    Application().mainloop()

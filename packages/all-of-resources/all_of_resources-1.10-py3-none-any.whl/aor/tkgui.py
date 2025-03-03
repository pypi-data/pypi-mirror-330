#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk,filedialog,messagebox as msg
from threading import Thread
import webbrowser
from . import core
import os

from .__main__ import version
__version__ = version


class AorUI:
    def __init__(self, master=None, data_pool=None):
        # build ui
        self.root = tk.Tk(master)
        self.root.geometry("413x200")
        self.root.iconphoto(True,tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "icon.png")))

        self.main_w = self.root.winfo_reqwidth()
        self.main_h = self.root.winfo_reqheight()
        self.center()

        self.root.resizable(False, False)
        self.root.title("All Of Resources {} - Minecraft 资源提取器".format(__version__))
        self.mcdir_t = ttk.Label(self.root, name="mcdir_t")
        self.mcdir_t.configure(text='选择.minecraft目录: ')
        self.mcdir_t.place(anchor="nw", relx=0.0, rely=0.0, x=8, y=8)
        self.mcdir = ttk.Entry(self.root, name="mcdir")
        self.minecraftdir = tk.StringVar()
        self.minecraftdir_old = tk.StringVar()
        self.mcdir.configure(textvariable=self.minecraftdir)
        self.mcdir.bind("<KeyRelease>", self.mcver_update)
        self.mcdir.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            rely=0.0,
            width=248,
            x=124,
            y=8)
        self.mcdir_browse = ttk.Button(self.root, name="mcdir_browse")
        self.mcdir_browse.configure(text='...')
        self.mcdir_browse.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.0,
            width=25,
            x=376,
            y=8)
        self.mcdir_browse.configure(command=self.select_minecraft)
        self.mcver_t = ttk.Label(self.root, name="mcver_t")
        self.mcver_t.configure(text='选择版本: ')
        self.mcver_t.place(anchor="nw", relx=0.0, rely=0.0, x=8, y=40)
        self.mcver = ttk.Combobox(self.root, name="mcver", state="readonly")
        self.mcversion = tk.StringVar()
        self.mcver.configure(textvariable=self.mcversion)
        self.mcver.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.0,
            width=277,
            x=124,
            y=40)
        self.extract_t = ttk.Label(self.root, name="extract_t")
        self.extract_t.configure(text='解压路径: ')
        self.extract_t.place(anchor="nw", relx=0.0, rely=0.0, x=8, y=70)
        self.extractdir = tk.StringVar()
        self.extract = ttk.Entry(self.root, name="extract", textvariable=self.extractdir)
        self.extract.bind("<KeyRelease>", self.mcver_update)
        self.extract.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.0,
            width=248,
            x=124,
            y=70)
        self.extract_browse = ttk.Button(self.root, name="extract_browse")
        self.extract_browse.configure(text='...')
        self.extract_browse.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.0,
            width=25,
            x=376,
            y=70)
        self.extract_browse.configure(command=self.select_extract)
        self.content = ttk.Label(self.root, text="All Of Resources By SystemFileB\n给个Star awa\n\n注意：解压路径需要使用空文件夹")
        self.content.place(anchor="nw", x=8, y=95)
        self.progress = ttk.Progressbar(self.root, name="progress")
        self.prog = tk.IntVar()
        self.progress.configure(orient="horizontal", variable=self.prog, maximum=2000)
        self.progress.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.0,
            width=281,
            x=8,
            y=168)
        self.start_b = ttk.Button(self.root, name="start_b")
        self.start_b.configure(text='开始',state="disabled")
        self.start_b.place(anchor="nw", height=22, width=50, x=355, y=168)
        self.start_b.configure(command=self.start)
        self.about_b = ttk.Button(self.root, name="about_b")
        self.about_b.configure(text='关于')
        self.about_b.place(anchor="nw", height=22, width=50, x=297, y=168)
        self.about_b.configure(command=self.about)

    def center(self):
        wm_min = self.root.wm_minsize()
        wm_max = self.root.wm_maxsize()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        """ `winfo_width` / `winfo_height` at this point return `geometry` size if set. """
        x_min = min(screen_w, wm_max[0],
                    max(self.main_w, wm_min[0],
                        413,
                        self.root.winfo_reqwidth()))
        y_min = min(screen_h, wm_max[1],
                    max(self.main_h, wm_min[1],
                        200,
                        self.root.winfo_reqheight()))
        x = screen_w - x_min
        y = screen_h - y_min
        self.root.geometry(f"{x_min}x{y_min}+{x // 2}+{y // 2}")

    def run(self):
        self.root.mainloop()

    def select_minecraft(self):
        dir=filedialog.askdirectory(title="选择.minecraft目录")
        if dir:
            self.minecraftdir.set(dir)
            self.mcver_update()

    def mcver_update(self,e=None):
        result=core.check(self.minecraftdir.get(), self.mcversion.get(), self.extractdir.get())
        self.mcver.configure(values=result[0])
        if self.minecraftdir_old.get()!=self.minecraftdir.get() and result[0]:
            self.mcver.current(0)
        if result[1]:
            self.start_b.configure(state="normal")
            self.content.configure(text=result[2])
        
        self.minecraftdir_old.set(self.minecraftdir.get())

    def select_extract(self):
        dir=filedialog.askdirectory(title="选择解压路径")
        if dir:
            self.extractdir.set(dir)
            self.mcver_update()

    def start(self):
        self.start_b.configure(state="disabled")
        self.root.protocol("WM_DELETE_WINDOW", self.donotclose)
        Thread(target=self.task, args=(self.mcversion.get(), self.extractdir.get())).start()

    def task(self, version, path):
        result=core.task(self.minecraftdir.get(),version,path,self.callback)
        if result[0]=="E":
            msg.showerror("All Of Resources", result[1])
        else:
            msg.showinfo("All Of Resources", result[1])
        
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.prog.set(0)
        self.mcver_update()
    
    def callback(self, progress, msg):
        self.prog.set(progress)
        self.content.configure(text=msg)

    def donotclose(self,e=None):
        pass


    def about(self):
        if msg.askyesno("All Of Resources", "All Of Resources By SystemFileB\n给个Star awa\n\n如果你使用了python -m aor -f或python -m aor --flutter来启动的话，你就可以试试手机端的体验 (或者更棒的UI)！\n\n是否进入项目的github？"):
            webbrowser.open("https://github.com/SystemFileB/all-of-resources")

def main():
    app = AorUI()
    app.run()
if __name__ == "__main__":
    main()
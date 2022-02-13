#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
from urllib.parse import urlparse
import threading
import json
import webbrowser
import pyperclip
import time
import os

if not "my_link_list.json" in os.listdir():
    d = {}
    with open("my_link_list.json", "w") as f:
        json.dump(d, f)

class Collector:
    def __init__(self):
        self.root = Tk()
        self.root.title("Link Collector")
        self.root.geometry("575x649")
        self.root.configure(bg="gray88")

        currentDir = StringVar()
        currentDir.set(os.getcwd())
        self.my_url = StringVar()

        with open("my_link_list.json") as f:
            self.link_list = json.load(f)

        Entry(self.root,textvariable=currentDir,width=95).place(x=0,y=0)
        self.urlEntry = Entry(self.root,textvariable=self.my_url,width=43,font=("arial",18))
        self.urlEntry.place(x=5,y=35)
        Button(self.root,text="SAVE URL",width=79,bg="gray77",command=self.enter_name).place(x=5,y=70)
        self.canvas = Canvas(self.root,bg="black")
        self.canvas.place(x=5,y=110)
        self.scrollbar = Scrollbar(self.canvas,orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.linkBox = Listbox(self.canvas,height=32,width=55)
        self.linkBox.pack()
        self.linkBox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.linkBox.yview)
        self.searchEntry = Entry(self.root,font=("arial",14),width=13)
        self.searchEntry.place(x=363,y=110)
        Button(self.root,text="SEARCH",bg="gray77").place(x=513,y=110)
        self.numLinks = Label(self.root,text='{} LINKS'.format(len(self.link_list)),bg='black',fg='green',width=25,font=("arial",10))
        self.numLinks.place(x=363,y=180)
        Button(self.root,text="COPY NEW LINK",bg="gray77",width=28,height=2,command=self.init_copy).place(x=363,y=210)
        Button(self.root,text="ACCESS",bg="gray77",width=28,height=2).place(x=363,y=260)
        Button(self.root,text="DELETE",bg="gray77",width=28,height=2).place(x=363,y=330)
        Button(self.root,text="DELETE ALL",bg="gray77",width=28,height=2).place(x=363,y=380)
        Button(self.root,text="CLEAR SELECTION",bg="gray77",width=28,height=2).place(x=363,y=430)
        Button(self.root,text="SAVE HTML FILE",bg="gray77",width=28,height=2).place(x=363,y=500)
        Button(self.root,text="SAVE LIST",bg="gray77",width=28,height=2).place(x=363,y=550)
        
        self.show_list()

        self.root.mainloop()

    def copy_paste(self):
        messagebox.showinfo("COPY URL","Copy the URL you want.")
        self.ultima_copia = pyperclip.paste().strip()
        while True:
            time.sleep(0.1)
            self.copia = pyperclip.paste().strip()
            if self.copia != self.ultima_copia:
                self.my_url.set(self.copia)
                self.ultima_copia = self.copia
                break

    def enter_name(self):
        if self.urlEntry.get() != "":
            is_url = self.validate_url(self.urlEntry.get())
            if is_url:
                self.window = Tk()
                self.window.geometry("470x300")
                self.window.title("Link Name")
                Label(self.window,text="ENTER LINK NAME",width=67).place(x=0,y=45)
                entry_name = Entry(self.window,width=23,font=('arial',20))
                entry_name.place(x=55,y=90)
                Button(self.window,text="SET NAME",width=10,height=2,bg="gray77",command=lambda:self.set_name(entry_name.get())).place(x=194,y=180)
            else:
                messagebox.showwarning("Invalid URL","Enter a valid URL.")
                self.my_url.set("")

    def show_list(self):
        if len(self.link_list) > 0:
            self.my_list = []
            c = 1
            for i in self.link_list:
                self.linkBox.insert(END,(str(c)+"- "+i))
                self.my_list.append(self.link_list[i])
                c+=1
            
    def set_name(self,entry_name):
        self.window.destroy()
        self.linkBox.delete(0,END)
        self.link_list[entry_name] = self.urlEntry.get()
        with open("my_link_list.json", "w") as f:
            json.dump(self.link_list, f)
        self.show_list()
        self.numLinks.configure(text='{} LINKS'.format(len(self.link_list)))
        
    def init_copy(self):
        t2 = threading.Thread(target=self.copy_paste)
        t2.start()

    def validate_url(self,url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

if __name__=="__main__":
    Collector()
    

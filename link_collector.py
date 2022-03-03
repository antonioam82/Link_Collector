#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox, filedialog
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
        self.selMode = 'normal'
        self.search = StringVar()

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
        self.searchEntry = Entry(self.root,textvariable=self.search,font=("arial",14),width=13)
        self.searchEntry.place(x=363,y=110)
        Button(self.root,text="SEARCH",bg="gray77",command=self.search_name).place(x=513,y=110)
        self.showAll = Button(self.root,state='disabled',text="SHOW ALL LINKS",width=28,command=self.show_all)
        self.showAll.place(x=363,y=138)
        self.numLinks = Label(self.root,text='{} LINKS'.format(len(self.link_list)),bg='black',fg='green',width=25,font=("arial",10))
        self.numLinks.place(x=363,y=205)
        Button(self.root,text="IMPORT NEW LINK",bg="gray77",width=28,height=2,command=self.init_copy).place(x=363,y=245)
        Button(self.root,text="ACCESS",bg="gray77",width=28,height=2,command=self.init_task).place(x=363,y=295)
        Button(self.root,text="DELETE",bg="gray77",width=28,height=2,command=self.remove_link).place(x=363,y=365)
        Button(self.root,text="DELETE ALL",bg="gray77",width=28,height=2,command=self.delete_listbox).place(x=363,y=415)
        Button(self.root,text="CLEAR SELECTION",bg="gray77",width=28,height=2,command=self.clear_selection).place(x=363,y=465)
        self.selMod = Button(self.root,text="SELECTION MODE: NORMAL",bg="gray77",width=28,height=2,command=self.selection_mode)
        self.selMod.place(x=363,y=515)
        Button(self.root,text="SAVE LIST",bg="gray77",width=28,height=2,command=self.write_doc).place(x=363,y=585)#35
        
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

    def show_all(self):
        self.linkBox.delete(0,END)
        with open("my_link_list.json") as f:
            self.link_list = json.load(f)
        self.show_list()
        self.showAll.configure(state='disabled')

    def delete_listbox(self):
        if self.linkBox.size() > 0:
            message = messagebox.askquestion("REMOVING",'Do you want to remove all link list?')
            if message == "yes":
                self.link_list = {}
                self.update_json()
                self.linkBox.delete(0,END)
                self.numLinks.configure(text='{} LINKS'.format(len(self.link_list)))#rep

    def selection_mode(self):
        if self.selMode == 'normal':
            self.linkBox.configure(selectmode='multiple')
            self.selMod.configure(text="SELECTION MODE: MULTIPLE")
            self.selMode = 'multiple'
        else:
            self.linkBox.configure(selectmode='normal')
            self.selMod.configure(text="SELECTION MODE: NORMAL")
            self.selMode = 'normal'
            
    def enter_name(self):
        if self.urlEntry.get() != "":
            is_url = self.validate_url(self.urlEntry.get())
            if is_url:
                self.window = Tk()
                self.window.geometry("470x300")
                self.window.title("Link Name")
                Label(self.window,text="ENTER LINK NAME",width=67).place(x=0,y=45)
                entry_name = Entry(self.window,width=25,font=('arial',20))
                entry_name.place(x=44,y=90)
                Button(self.window,text="SET NAME",width=10,height=2,bg="gray77",command=lambda:self.set_name(entry_name.get())).place(x=198,y=180)
            else:
                messagebox.showwarning("Invalid URL","Enter a valid URL.")
                self.my_url.set("")

    def search_name(self):
        c = 0
        self.my_list = []
        self.linkBox.delete(0,END)
        for i in self.link_list.keys():
            if self.searchEntry.get().lower() in i.lower():
                self.linkBox.insert(END,(str(c)+"- "+i))
                self.my_list.append(self.link_list[i])
                c+=1
        self.showAll.configure(state='normal') 

    def show_list(self):
        if len(self.link_list) > 0:
            self.my_list = []
            c = 1
            for i in self.link_list:
                self.linkBox.insert(END,(str(c)+"- "+i))
                self.my_list.append(self.link_list[i])
                c+=1
            
    def set_name(self,entry_name):
        if entry_name != "":
            self.window.destroy()
            self.linkBox.delete(0,END)
            self.link_list[entry_name] = self.urlEntry.get()
            self.update_json()
            self.show_list()
            self.numLinks.configure(text='{} LINKS'.format(len(self.link_list)))

    def update_json(self):
        with open("my_link_list.json", "w") as f:
            json.dump(self.link_list, f)

    def remove_link(self):
        any_selected = self.is_any_selected()
        if any_selected:
            message = messagebox.askquestion("REMOVE LINK",'Delete selected link/s from link list?')
            if message == "yes":
                for i in self.linkBox.curselection():
                    del self.link_list[self.get_key(self.my_list[i])]
                self.linkBox.delete(0,END)
                self.update_json()
                self.show_list()
                self.numLinks.configure(text='{} LINKS'.format(len(self.link_list)))

    def get_key(self,val):
        for key, value in self.link_list.items():
            if val == value:
                return key

    def open_page(self):
        try:
            for i in self.linkBox.curselection():
                print(i)
                webbrowser.open_new(self.my_list[i])
        except Exception as e:
            messagebox.showwarning("Access trouble", str(e))
            

    def clear_selection(self):
        for i in self.linkBox.curselection():
            self.linkBox.selection_clear(i)


    def is_any_selected(self):
        for i in range(0,self.linkBox.size()):
            if self.linkBox.selection_includes(i):
                sel = True
                break
        else:
            sel = False
        return sel    

    def init_task(self):
        self.any_selected = self.is_any_selected()
        if self.any_selected:
            t = threading.Thread(target=self.open_page)
            t.start()
        else:
            messagebox.showwarning("No Link Selected","Select a link to go.")

    def write_doc(self):
        if self.linkBox.size() > 0:
            doc = filedialog.asksaveasfilename(initialdir="/",
                  title="Save as", initialfile="saved links",defaultextension=".txt")
            if doc != "":
                new_file = open(doc,"w")
                new_file.write("SAVED LINKS:\n\n")
                for key, value in self.link_list.items():
                    new_file.write("{}: {}\n\n".format(key, value))
                new_file.close()
                messagebox.showinfo("Saved","Text document saved correctly.")
        else:
            messagebox.showwarning("NO ITEMS","There's nothing to save.")


    def init_copy(self):
        tc = threading.Thread(target=self.copy_paste)
        tc.start()

    def validate_url(self,url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

if __name__=="__main__":
    Collector()
    

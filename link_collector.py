#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
import json
import webbrowser
import os

class Collector:
    def __init__(self):
        self.root = Tk()
        self.root.title("Link Collector")
        self.root.geometry("575x649")
        self.root.configure(bg="gray88")

        currentDir = StringVar()
        currentDir.set(os.getcwd())

        Entry(self.root,textvariable=currentDir,width=95).place(x=0,y=0)
        self.url = Entry(self.root,width=43,font=("arial",18))
        self.url.place(x=5,y=35)
        Button(self.root,text="SAVE",width=79,bg="gray77").place(x=5,y=70)
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
        self.numLinks = Label(self.root,text='0 LINKS',bg='black',fg='green',width=25,font=("arial",10))
        self.numLinks.place(x=363,y=180)
        Button(self.root,text="NEW LINK",bg="gray77",width=28,height=2).place(x=363,y=210)
        Button(self.root,text="ACCESS",bg="gray77",width=28,height=2).place(x=363,y=260)
        
        self.root.mainloop()

if __name__=="__main__":
    Collector()
    

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

        currentDir = StringVar()
        currentDir.set(os.getcwd())

        Entry(self.root,textvariable=currentDir,width=95).place(x=0,y=0)
        self.url = Entry(self.root,width=43,font=("arial",18))
        self.url.place(x=5,y=35)
        Button(self.root,text="SAVE",width=79,bg="gray77").place(x=5,y=70)

        self.root.mainloop()

if __name__=="__main__":
    Collector()
    

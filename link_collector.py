#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
import json
import webbrowser

class Collector:
    def __init__(self):
        self.root = Tk()
        self.root.title("Link Collector")
        self.root.geometry("530x590")

        self.root.mainloop()

if __name__=="__main__":
    Collector()
    

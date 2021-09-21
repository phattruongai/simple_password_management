'''Importing'''
from tkinter import *
from tkinter import ttk
import  tkinter.messagebox
import pathlib
import os
file_path = pathlib.Path(__file__).parent.resolve()
os.chdir(file_path)

from authentication_UI import *

if __name__ == '__main__':

    root = Tk()
    application = Authentication(root)
    root.mainloop()
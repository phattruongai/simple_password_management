from tkinter import *
from tkinter import ttk
import  tkinter.messagebox
import pandas as pd
import pathlib
import os
file_path = pathlib.Path(__file__).parent.resolve()
os.chdir(file_path)
from pw_manager_UI import *

class Authentication:
    file_path = pathlib.Path(__file__).parent.resolve()
    
    def __init__(self,root):
        self.df = pd.read_csv(f"{file_path}/pw.csv")
        self.user = str(self.df.loc[0,["name"]].values[0])
        self.passw = str(self.df.loc[0,["pass"]].values[0])
        self.root = root
        self.root.title('P Manager')
        self.root.geometry('250x150+400+250')

        '''Make Window 10X10'''

        rows = 0
        while rows<10:
            self.root.rowconfigure(rows, weight=1)
            self.root.columnconfigure(rows, weight=1)
            rows+=1

        '''Username and Password'''

        frame = LabelFrame(self.root, text='Login')
        frame.grid(row = 1,column = 1,columnspan=10,rowspan=10)

        Label(frame, text = ' Usename ').grid(row = 2, column = 1, sticky = W)
        self.username = Entry(frame)
        self.username.grid(row = 2,column = 2)

        Label(frame, text = ' Password ').grid(row = 5, column = 1, sticky = W)
        self.password = Entry(frame, show='*')
        self.password.grid(row = 5, column = 2)

        # Button

        ttk.Button(frame, text = 'LOGIN',command = self.login_user).grid(row=7,column=2)
        self.root.bind('<Return>', self.login_user)

        '''Message Display'''
        self.message = Label(text = '',fg = 'Red')
        self.message.grid(row=9,column=6)


    def login_user(self,*args):
        '''Check username and password entered are correct'''
        if self.username.get() == self.user and self.password.get() == self.passw:

            #Destroy current window
            self.root.destroy()
            
            #Open new window
            newroot = Tk()

            #connect to DB
            dbname = self.df.loc[1,'dbname']
            akdir = self.df.loc[1,'akdir']
            pass_manager = Pass_Manager(dbname,akdir)
            Pass_Manager_UI(newroot,pass_manager)
            newroot.mainloop()
        else:

            '''Prompt user that either id or password is wrong'''
            self.message['text'] = 'Username or Password incorrect. Try again!'
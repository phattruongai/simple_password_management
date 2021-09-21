from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import font
import pandas as pd
import pathlib
import os
file_path = pathlib.Path(__file__).parent.resolve()
os.chdir(file_path)
import pandas as pd
import boto3

class Pass_Manager(object):
    def __init__(self,table_name,AWS_KEY):
        df = pd.read_csv(AWS_KEY)
        self.ddb = boto3.resource('dynamodb', 
                     aws_access_key_id=f'{df.loc[0,"AWSAccessKeyId"]}',
                     aws_secret_access_key=f'{df.loc[0,"AWSSecretKey"]}',
                     region_name = 'ap-southeast-1')
        self.table = self.ddb.Table(table_name)
    
    def show_all(self):
        all_item = self.table.scan()
        # for item in all_item['Items']:
        #     print("-"*40)
        #     for key in item.keys():
        #         print(key,':',item[key])
        return all_item

    def find_service(self,service_type):
        items = self.table.query(
            KeyConditionExpression="service_type = :service_type", 
            ExpressionAttributeValues={
                ':service_type': service_type
            })['Items']
        # for item in items:
        #     print("-"*40)
        #     for key in item.keys():
        #         print(key,':',item[key])
        return items
    def add_item(self,item):
        self.table.put_item(Item=item)

class Pass_Manager_UI(object):
    def __init__(self,root,pass_manager):
        self.pass_manager = pass_manager
        self.root = root
        self.root.title('P Manager')
        self.root.geometry("655x525+300+50")

        
        frame = ttk.Frame(self.root)
        sa_btn = ttk.Button(frame, text = 'Show all',command = self.show_all)
        ft_btn = ttk.Button(frame, text = 'Find group',command = self.find_group)
        at_btn = ttk.Button(frame, text = 'Add new item',command = self.add_item)
        frame.grid(column=0,row=0)
        sa_btn.grid(column=0,row=0,padx=10)
        ft_btn.grid(column=0,row=1,padx=10)
        at_btn.grid(column=0,row=2,padx=10)

        self.t = Text(self.root, wrap = "none")
        self.t.tag_configure("modifiedfont",font=font.Font(family='Helvetica',size=14))
        ys = ttk.Scrollbar(self.root, orient = 'vertical', command = self.t.yview)
        xs = ttk.Scrollbar(self.root, orient = 'horizontal', command = self.t.xview)
        self.t['yscrollcommand'] = ys.set
        self.t['xscrollcommand'] = xs.set
        self.t.grid(column = 1, row = 0, sticky = 'nwes')
        self.t.insert('end', "Welcome!")
        xs.grid(column = 1, row = 1, sticky = 'we')
        ys.grid(column = 2, row = 0, sticky = 'ns')
        self.root.grid_columnconfigure(1, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)
        self.t['state'] = 'disabled'
        
    def show_all(self):
        self.t['state'] = 'normal'
        self.t.delete('1.0',END)
        all_items = self.pass_manager.show_all()
        for i,item in enumerate(all_items['Items']):
            sep_line = "-"*40
            self.t.insert('end',f"\n{i}.{sep_line}\n")
            for key in item.keys():
                if key == "service_type":
                    printkey = "Group"
                elif key == "service_name":
                    printkey = "Item name"
                else:
                    printkey = key
                self.t.insert('end',f"{printkey} : {item[key]}\n")
        self.t['state'] = 'disabled'

    def find_group(self):
        #popup a dialog to input group name
        group_name = simpledialog.askstring("Group name","Type the name of group you saved in")
        self.t['state'] = 'normal'
        self.t.delete('1.0',END)
        items = self.pass_manager.find_service(group_name)
        if len(items) == 0:
            messagebox.showwarning("Warning","You did not save any password in this group")
        else:
            for i,item in enumerate(items):
                sep_line = "-"*40
                self.t.insert('end',f"\n{i}.{sep_line}\n")
                for key in item.keys():
                    if key == "service_type":
                        printkey = "Group"
                    elif key == "service_name":
                        printkey = "Item name"
                    else:
                        printkey = key
                    self.t.insert('end',f"{key} : {item[key]}\n")
        self.t['state'] = 'disabled'

    def add_item(self):
        self.t['state'] = 'normal'
        def dismiss():
            dlg.grab_release()
            dlg.destroy()
        def add():
            item = {
                "service_type":gr_name.get(),
                "service_name":it_name.get(),
                "year":int(year.get())
            }
            values_str = vl_name.get('1.0', 'end')
            for x in values_str.split("\n"):
                if len(x) != 0:
                    item.update(
                        {
                            x.split(":")[0].strip():x.split(":")[1].strip()
                        }
                    )
            okcancel = messagebox.askokcancel("Confirm","Are you sure to add this item?")
            if okcancel:
                self.pass_manager.add_item(item)
                dismiss()
        dlg = Toplevel(self.root)
        dlg.geometry("350x300+400+100")

        btn = ttk.Frame(dlg)
        btn.grid(column=0,row=1,pady=10,sticky=E)
        add_btn = ttk.Button(btn, text="Add", command=add)
        cancel_btn = ttk.Button(btn, text="Cancel", command=dismiss)

        add_btn.grid(column=0,row=0)
        cancel_btn.grid(column=1,row=0,sticky=(E))

        inp = ttk.Frame(dlg)
        inp.grid(column=0,row=0)
        gr_name_lbl = Label(inp, text = ' Group Name ')
        gr_name = Entry(inp)
        it_name_lbl = Label(inp, text = ' Item Name ')
        it_name = Entry(inp)
        year_lbl = Label(inp, text = ' Year ')
        year = Entry(inp)
        vl_name_lbl = Label(inp, text = ' Values(YAML) ')
        vl_name = Text(inp,width=30,height=10,wrap='none')

        gr_name_lbl.grid(column=0,row=0,sticky=W)
        it_name_lbl.grid(column=0,row=1,sticky=W)
        year_lbl.grid(column=0,row=2,sticky=W)
        vl_name_lbl.grid(column=0,row=3,sticky=W)
        gr_name.grid(column=1,row=0,sticky=(W,E),pady=4)
        it_name.grid(column=1,row=1,sticky=(W,E),pady=0)
        year.grid(column=1,row=2,sticky=(W,E),pady=4)
        vl_name.grid(column=1,row=3,pady=0)
        
        dlg.protocol("WM_DELETE_WINDOW", dismiss) # intercept close button
        dlg.transient(self.root)   # dialog window is related to main
        dlg.wait_visibility() # can't grab until window appears, so we wait
        dlg.grab_set()        # ensure all input goes to our window
        dlg.wait_window()     # block until window is destroyed
        self.t['state'] = 'disabled'



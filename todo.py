
from tkinter import *
from tkinter.ttk import Treeview
from tkinter.messagebox import showerror, showinfo
import sqlite3
from datetime import datetime

# Globals CONSTANTS
FACILITATOR = "Gyan Ganga Institute of Technology and Sciences"
PROJECT = "To Do List"
AUTHOR = "Aryan Singh Thakur"
FILENAME = "todolist.db"
TABLENAME = "todolist"
FIELDS = "sno INTEGER PRIMARY KEY, task TEXT, comment TEXT, taskdate TEXT, tasktime TEXT"
currSNo = 0

# SQLite init
try: 
    connection = sqlite3.connect(FILENAME)
    cursor = connection.cursor()
    queryCreateTable = f"CREATE TABLE IF NOT EXISTS {TABLENAME} ({FIELDS});"
    cursor.execute(queryCreateTable)
    connection.commit()
except sqlite3.Error as e:
    showinfo("DataBase Error", f"Database Error: \n{str(e).title()}")    

# SQLite Functions
def insertDB(task, comment):
    try:
        cursor.execute(f"SELECT MAX(sno) FROM {TABLENAME};")
        max_sno = cursor.fetchone()[0]
        sno = max_sno + 1 if max_sno is not None else 1
        taskdate = datetime.today().strftime('%d-%m-%Y')
        tasktime = datetime.today().strftime('%H:%M:%S')
        insertQuery = f"INSERT INTO {TABLENAME} (sno, task, comment, taskdate, tasktime) VALUES (?, ?, ?, ?, ?);"
        cursor.execute(insertQuery, (sno, task, comment, taskdate, tasktime))
        connection.commit()
    except Exception as e:
        showinfo("Database Error", f"Writing Error: \n{str(e).title()}")
    finally:
        loadData()

def updateDB(sno, task, comment):
    try:
        taskdate = datetime.today().strftime('%d-%m-%Y')
        tasktime = datetime.today().strftime('%H:%M:%S')
        updateQuery = f"UPDATE {TABLENAME} SET task = ?, comment = ?, taskdate = ?, tasktime = ? WHERE sno = ?;"
        cursor.execute(updateQuery, (task, comment, taskdate, tasktime, sno))
        connection.commit()
    except Exception as e:
        showinfo("Database Error", f"Update Error: \n{str(e).title()}")    
    finally:
        loadData()

def deleteDB(sno):
    try:
        deleteQuery = f"DELETE FROM {TABLENAME} WHERE sno = ?;"
        cursor.execute(deleteQuery, (sno,))
        connection.commit()
        updateQuery = f"UPDATE {TABLENAME} SET sno = sno - 1 WHERE sno > ?;"
        cursor.execute(updateQuery, (sno,))
        connection.commit()
    except Exception as e:
        showinfo("Database Error", f"Deletion Error: \n{str(e).title()}")
    finally:
        loadData()

def fetchData():
    try:
        cursor.execute(f"SELECT * FROM {TABLENAME};")
        all_data = cursor.fetchall()
        return all_data
    except sqlite3.Error as e:
        showinfo("Database Warning", f"Read Error: \n{str(e).title()}")

def loadData():
    DATA = fetchData()
    for i in tree.get_children():
        tree.delete(i)
    for i in DATA:
        tree.insert("", "end", values=i)
    tree.update()

# Tk Functions
def onSelect():
    global currSNo
    curr = tree.item(tree.selection())
    taskEntry.delete(0, END)
    commentEntry.delete(0, END)
    taskEntry.insert(0, curr['values'][1])
    commentEntry.insert(0, curr['values'][2])
    currSNo = curr['values'][0]

def onClick(e):
    tree.after(50, onSelect)

def addTask():
    task = taskEntry.get()
    comment = commentEntry.get()
    insertDB(task, comment)

def updateTask():
    global currSNo
    task = taskEntry.get()
    comment = commentEntry.get()
    updateDB(currSNo, task, comment)

def deleteTask():
    global currSNo
    deleteDB(currSNo)

def about():
    about = Toplevel()
    about.title("About the Project")
    about.geometry("800x200+200+200")
    aboutLabel = Label(about, text=f"Facilitator:   {FACILITATOR}\nProject:       {PROJECT}\nAuthor:        {AUTHOR}\n                                          Thank you.", justify='left', font=('Consolas', 12))

    aboutLabel.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
    about.mainloop()

# root init
root = Tk()

# Tk Globals
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
XPOS = 50
YPOS = 20

# Root Window
root.title(f'{PROJECT} - {AUTHOR}')
root.geometry(f"{WIDTH-100}x{HEIGHT-100}+{XPOS}+{YPOS}")

# Ttk Treeview
tree = Treeview(root, columns=["sno", "task", "comment", "date", "time"], height=25, name='todolist', show='tree headings')
tree.selection
tree.heading("sno", text="S.No.")
tree.heading("task", text="Task")
tree.heading("comment", text="Comment")
tree.heading("date", text="Date")
tree.heading("time", text="Time")

tree.column("#0", width=0, stretch=False)
tree.column("sno", width=4)
tree.column("task", stretch=False)
tree.column("comment", stretch=False)
tree.column("date", width=10)
tree.column("time", width=10)

tree.place(relx=0.07, rely=0.07, relwidth=0.43, relheight=0.86)

# Buttons and Entries init
addButton       = Button(root, text="Add Task", font=("Universe", 14), command=addTask)
updateButton    = Button(root, text="Update Task", font=("Universe", 14), command=updateTask)
deleteButton    = Button(root, text="Delete Task", font=("Universe", 14), command=deleteTask)
aboutButton     = Button(root, text="About", font=("Universe", 14), command=about)
taskLabel       = Label(root, text="Task", font=("Universe", 14))
commentLabel    = Label(root, text="Comment", font=("Universe", 14))
taskEntry       = Entry(root, font=("Universe", 16), justify='center')
commentEntry    = Entry(root, font=("Universe", 16), justify='center')

# Buttons and Entries placement
taskEntry.place(relx=0.57, rely=0.07, relwidth=0.36, relheight=0.08)
taskLabel.place(relx=0.57, rely=0.15, relwidth=0.36, relheight=0.08)
commentEntry.place(relx=0.57, rely=0.22, relwidth=0.36, relheight=0.08)
commentLabel.place(relx=0.57, rely=0.30, relwidth=0.36, relheight=0.08)
addButton.place(relx=0.57, rely=0.49, relwidth=0.36, relheight=0.08)
updateButton.place(relx=0.57, rely=0.61, relwidth=0.36, relheight=0.08)
deleteButton.place(relx=0.57, rely=0.73, relwidth=0.36, relheight=0.08)
aboutButton.place(relx=0.57, rely=0.85, relwidth=0.36, relheight=0.08)

# Tk Bindings
tree.bind("<Button-1>", onClick)

# Tk Mainloop
loadData()
root.mainloop()
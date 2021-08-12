from tkinter import *
import sqlite3
from tkinter import messagebox
import sys

root = Tk()

connect = sqlite3.connect('official-doc-appoint-list.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE docsappoint (
                fname text,
                lname text,
                time real,
                total_people integer,
                reasoning text)
                """)

root.title('Doctor\'s appointment')
docicon = PhotoImage(file='C:\doctor-icon.png')
root.iconphoto(True, docicon)

fnameentry = Entry(root, width=40)
fnameentry.grid(row=0, column=1)
lnameentry = Entry(root, width=40)
lnameentry.grid(row=1, column=1)
timeentry = Entry(root, width=40)
timeentry.insert(0, 'time format is 13.41 (military form)')
timeentry.grid(row=2, column=1)
total_peopleentry = Entry(root, width=40)
total_peopleentry.grid(row=3, column=1)
reasoningentry = Entry(root, width=40)
reasoningentry.grid(row=4, column=1)

fnamelabel = Label(root, text='Enter First Name:', padx=2, font='Arial 12 bold')
fnamelabel.grid(row=0, column=0)
lnamelabel = Label(root, text='Enter Last Name:', padx=2, font='Arial 12 bold')
lnamelabel.grid(row=1, column=0)
timelabel = Label(root, text='Enter Time of Appointment:', padx=2, font='Arial 12 bold')
timelabel.grid(row=2, column=0)
total_peoplelabel = Label(root, text='Total people coming in:', padx=2, font='Arial 12 bold')
total_peoplelabel.grid(row=3, column=0)
reasoninglabel = Label(root, text='What are your/other\'s health concerns:', padx=2, font='Arial 12 bold')
reasoninglabel.grid(row=4, column=0)

def checkpeople():
    if space == True:
        if int(total_peopleentry.get()) > 10:
            messagebox.showerror(title='Too Much People', message='There can only be 10 people in at once')
        else:
            statuslabel = Label(root, text='Your appointment has been scheduled')
            statuslabel.grid(row=7, column=0, columnspan=2)


space = ''
def checktime():
    global space
    connect = sqlite3.connect('official-doc-appoint-list.db')
    cursor = connect.cursor()
    cursor.execute('SELECT time FROM docsappoint')
    times = cursor.fetchall()
    for time in times:
        if float(timeentry.get()) == float(time[0]):
            space = False
            messagebox.showerror(title='No space remaining', message='Please Check back For more space')
            sys.exit()
        else:
            space = True
            checkpeople()

def checkslot():
    connect = sqlite3.connect('official-doc-appoint-list.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO docsappoint VALUES (:fname, :lname, :time, :total_people, :reasoning)", {
        'fname' : fnameentry.get(),
        'lname' : lnameentry.get(),
        'time' : timeentry.get(),
        'total_people' : total_peopleentry.get(),
        'reasoning' : reasoningentry.get()
    })
    connect.commit()
    connect.close()
    checktime()

def clear():
    fnameentry.delete(0, END)
    lnameentry.delete(0, END)
    timeentry.delete(0, END)
    total_peopleentry.delete(0, END)
    reasoningentry.delete(0, END)

checkspot = Button(root, text='Apply', pady=5, font=('ComicSans 15 bold'), width=20, height=1, borderwidth=5, fg='#00008b', bg='#a9a9a9', command=checkslot)
checkspot.grid(row=5, column=0, columnspan=2, ipadx=65)

quitbutton = Button(root, text='Clear text', command=clear, width=12, pady=3, fg='purple')
quitbutton.grid(row=6, column=0)

quitbutton = Button(root, text='Quit', command=root.quit, width=12, pady=3, fg='red')
quitbutton.grid(row=6, column=1)


connect.commit()
connect.close()

root.mainloop()

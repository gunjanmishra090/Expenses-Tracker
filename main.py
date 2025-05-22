# import modules
from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox
import tkinter as tk



# object for database
data = Database(db='test.db')

# global variables
count = 0
selected_rowid = 0

# functions


def saveRecord():
    if len(item_name.get()) == 0:
        return
    global data
    data.insertRecord(item_name=item_name.get(
    ), item_price=item_amt.get(), purchase_date=transaction_date.get())


def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')


def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')


def fetch_records():
    f = data.fetchRecord('select rowid, * from expense_record')
    global count
    for rec in f:
        tv.insert(parent='', index='0', iid=count,
                  values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refreshData)


def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')

    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass


def update_record():
    if len(item_name.get()) == 0:
        return
    global selected_rowid
    selected = tv.focus()
    # Update record
    try:
        data.updateRecord(namevar.get(), amtvar.get(),
                          dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(
            namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error',  ep)

        # Clear entry boxes
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    tv.after(400, refreshData)


def spentAmount():
    f = data.fetchRecord(query="Select sum(item_price) from expense_record")
    totalExpense = 0
    for i in f:
        for j in i:
            totalExpense = j
    return totalExpense


def totalBalance():
    f = data.fetchRecord(query="Select sum(item_price) from expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo(
                'Current Balance: ', f"Total Expense: ' {j} \nBalance Remaining: {5000 - j}")


def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()


def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()
    clearEntries()


def startMainWindow():
    entry_window.withdraw()
    ws.deiconify()


def getMostExpensiveItem():
    item = data.fetchRecord(
        query="SELECT item_name, item_price FROM expense_record WHERE item_price = (SELECT MAX(item_price) FROM expense_record);")
    return item

# print(data.fetchRecord(query="SELECT item_name, item_price FROM expense_record WHERE item_price = (SELECT MAX(item_price) FROM expense_record);")[0][1])


# create tkinter object
ws = Tk()
ws.title('Daily Expenses')
ws.geometry("720x400")
ws.minsize(720, 400)
ws.maxsize(720, 400)
ws.withdraw()


# Entry tkinter window
entry_window = tk.Toplevel()
entry_window.geometry("500x300")
entry_window.minsize(500, 300)
entry_window.maxsize(500, 300)
# entry_window.withdraw()


# variables
# f = ('Times new roman', 14)
f = ('Georgia', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()


# add elements to second window
label = tk.Label(entry_window, text="Spendwise", font=f)
label.pack()
spentLabel = tk.Label(
    entry_window, text=f'Your total Expense to date: {spentAmount()}', font=f)
spentLabel.pack()
mostExpensiveItem = tk.Label(
    entry_window, text=f'Your Most Expensive item was: {getMostExpensiveItem()[0][0]} Rs.{getMostExpensiveItem()[0][1]}', font=f)
mostExpensiveItem.pack()
button = tk.Button(entry_window, text="Start Adding Entries", font=f,
                   bg="red", borderwidth=0, fg='white', command=startMainWindow)
button.pack()


# Frame widget
f2 = Frame(ws)
f2.pack()

f1 = Frame(
    ws,
    padx=10,
    pady=10,
)
f1.pack(expand=True, fill=BOTH)


# Label widget
Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)

# Entry widgets
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))


# Action buttons
cur_date = Button(
    f1,
    text='Current Date',
    font=f,
    bg='#85C1E9',
    command=setDate,
    width=15,
    borderwidth=0
)

submit_btn = Button(
    f1,
    text='Save Record',
    font=f,
    command=saveRecord,
    bg='#239B56',
    fg='white',
    borderwidth=0
)

clr_btn = Button(
    f1,
    text='Clear Entry',
    font=f,
    command=clearEntries,
    bg='#D4AC0D',
    fg='white',
    borderwidth=0
)

quit_btn = Button(
    f1,
    text='Exit',
    font=f,
    command=lambda: ws.destroy(),
    bg='#CB4335',
    fg='white',
    borderwidth=0
)

total_bal = Button(
    f1,
    text='Total Balance',
    font=f,
    bg='#85929E',
    command=totalBalance,
    borderwidth=0
)

total_spent = Button(
    f1,
    text='Total Spent',
    font=f,
    command=lambda: data.fetchRecord('select sum(ite)'),
    borderwidth=0
)

update_btn = Button(
    f1,
    text='Update',
    bg='#F4D03F',
    command=update_record,
    font=f,
    borderwidth=0
)

del_btn = Button(
    f1,
    text='Delete',
    bg='#922B21',
    command=deleteRow,
    font=f,
    borderwidth=0,
)

# grid placement
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0), pady=6)
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

# Treeview widget
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side="left")

# add heading to treeview
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name", )
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# binding treeview
tv.bind("<ButtonRelease-1>", select_record)

# style for treeview
style = ttk.Style()
style.theme_use("clam")
style.map("Treeview")

# Vertical scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# calling function
fetch_records()

# infinite loop
ws.mainloop()

import customtkinter as ctk
from tkinter import ttk
import csv
import os

CSV_FILE = "expenses.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["Date","Category","Amount","Description"])

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

total_amount = 0

def add_expense():
    global total_amount
    date = date_entry.get().strip()
    category = category_entry.get().strip()
    amount = amount_entry.get().strip()
    description = description_entry.get().strip()

    if not date or not category or not amount:
        return

    try:
        amt = float(amount)
    except ValueError:
        return

    expense_table.insert("", "end", values=(date, category, amt, description))

    with open(CSV_FILE,"a",newline="") as f:
        csv.writer(f).writerow([date,category,amt,description])

    total_amount += amt
    total_label.configure(text=f"Total Expense : ₹{total_amount:.2f}")

    for e in (date_entry,category_entry,amount_entry,description_entry):
        e.delete(0,"end")

def load_expenses():
    global total_amount
    with open(CSV_FILE,"r",newline="") as f:
        reader=csv.reader(f)
        next(reader,None)
        for row in reader:
            if len(row)!=4:
                continue
            expense_table.insert("", "end", values=row)
            try:
                total_amount += float(row[2])
            except:
                pass
    total_label.configure(text=f"Total Expense : ₹{total_amount:.2f}")


def delete_expense():
    global total_amount
    selected = expense_table.selection()
    if not selected:
        return
    item = selected[0]
    values = expense_table.item(item, "values")
    try:
        total_amount -= float(values[2])
    except:
        pass
    total_label.configure(text=f"Total Expense : ₹{total_amount:.2f}")
    expense_table.delete(item)
    rows=[]
    for i in expense_table.get_children():
        rows.append(expense_table.item(i)["values"])
    with open(CSV_FILE,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["Date","Category","Amount","Description"])
        w.writerows(rows)


window=ctk.CTk()
window.title("Expense Tracker")
window.geometry("950x650")

title=ctk.CTkLabel(window,text="💰 Expense Tracker",font=("Arial",28,"bold"))
title.pack(pady=20)

input_frame=ctk.CTkFrame(window)
input_frame.pack(fill="x",padx=20,pady=10)

ctk.CTkLabel(input_frame,text="Date").grid(row=0,column=0,padx=10,pady=10,sticky="w")
date_entry=ctk.CTkEntry(input_frame,width=220)
date_entry.grid(row=0,column=1)

ctk.CTkLabel(input_frame,text="Category").grid(row=1,column=0,padx=10,pady=10,sticky="w")
category_entry=ctk.CTkEntry(input_frame,width=220)
category_entry.grid(row=1,column=1)

ctk.CTkLabel(input_frame,text="Amount").grid(row=2,column=0,padx=10,pady=10,sticky="w")
amount_entry=ctk.CTkEntry(input_frame,width=220)
amount_entry.grid(row=2,column=1)

ctk.CTkLabel(input_frame,text="Description").grid(row=3,column=0,padx=10,pady=10,sticky="w")
description_entry=ctk.CTkEntry(input_frame,width=220)
description_entry.grid(row=3,column=1)

btn_frame=ctk.CTkFrame(window)
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame,text="Add Expense",command=add_expense).grid(row=0,column=0,padx=8)
ctk.CTkButton(btn_frame,text="Update").grid(row=0,column=1,padx=8)
ctk.CTkButton(btn_frame,text="Delete",command=delete_expense).grid(row=0,column=2,padx=8)
ctk.CTkButton(btn_frame,text="Search").grid(row=0,column=3,padx=8)
ctk.CTkButton(btn_frame,text="Clear").grid(row=0,column=4,padx=8)

table_frame=ctk.CTkFrame(window)
table_frame.pack(fill="both",expand=True,padx=20,pady=20)

cols=("Date","Category","Amount","Description")
expense_table=ttk.Treeview(table_frame,columns=cols,show="headings",height=12)
for c in cols:
    expense_table.heading(c,text=c)
    expense_table.column(c,width=180)
expense_table.pack(fill="both",expand=True)

total_label=ctk.CTkLabel(window,text="Total Expense : ₹0",font=("Arial",18,"bold"))
total_label.pack(pady=10)

bottom=ctk.CTkFrame(window)
bottom.pack(pady=10)
ctk.CTkButton(bottom,text="Pie Chart").grid(row=0,column=0,padx=8)
ctk.CTkButton(bottom,text="Bar Chart").grid(row=0,column=1,padx=8)
ctk.CTkButton(bottom,text="Exit",command=window.destroy).grid(row=0,column=2,padx=8)

load_expenses()
window.mainloop()

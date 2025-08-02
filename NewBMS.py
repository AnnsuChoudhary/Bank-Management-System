import tkinter as tk
from tkinter import ttk, messagebox
from tabulate import tabulate
import mysql.connector

# Database connection and setup
con = mysql.connector.connect(host='localhost', username='root', password='A@nn#5u')
cur = con.cursor()
cur.execute("create database if not exists ALLINDIABANK")
cur.execute("use ALLINDIABANK")
cur.execute("""
    create table if not exists ACCOUNT_REGISTRY(
        accno int primary key not null,
        name char(15) not null,
        username varchar(10) not null,
        acctype varchar(10) not null,
        balance int,
        age int,
        kyc varchar(20)
    )
""")

# GUI Setup
root = tk.Tk()
root.title("ALL INDIA BANK MANAGEMENT SYSTEM")
root.geometry("950x600")
root.configure(bg="#e6f0ff")

style = ttk.Style()
style.configure('TNotebook', background='#cce0ff', padding=5)
style.configure('TNotebook.Tab', background='#cce0ff', font=('Arial', 11))
style.map("TNotebook.Tab", background=[("selected", "#99ccff")])

header = tk.Label(root, text="ALL INDIA BANK", font=("Helvetica", 20, "bold"), bg="#003366", fg="white", pady=10)
header.pack(fill='x')

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill='both')

# Frames for each tab
frame_register = tk.Frame(notebook, bg="#e6f0ff")
frame_kyc = tk.Frame(notebook, bg="#e6f0ff")
frame_modify = tk.Frame(notebook, bg="#e6f0ff")
frame_search = tk.Frame(notebook, bg="#e6f0ff")

notebook.add(frame_register, text='Create Account')
notebook.add(frame_modify, text='Modify Info')
notebook.add(frame_kyc, text='KYC Update')
notebook.add(frame_search, text='Search Account')

# Create Account Tab
labels = ["Account No", "Name", "Username", "Account Type", "Balance", "Age"]
entries = []
for idx, label in enumerate(labels):
    tk.Label(frame_register, text=label, font=("Arial", 12), bg="#e6f0ff").grid(row=idx, column=0, padx=10, pady=5, sticky='w')
    entry = tk.Entry(frame_register, width=30)
    entry.grid(row=idx, column=1, padx=10, pady=5)
    entries.append(entry)

def create_account():
    try:
        accno = int(entries[0].get())
        name = entries[1].get()
        username = entries[2].get()
        acctype = entries[3].get()
        balance = int(entries[4].get())
        age = int(entries[5].get())
        kyc = "not done"
        query = "INSERT INTO ACCOUNT_REGISTRY VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (accno, name, username, acctype, balance, age, kyc))
        con.commit()
        messagebox.showinfo("Success", "Account created successfully!")
        for entry in entries:
            entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Error creating account: {e}")

btn_create = tk.Button(frame_register, text="Create Account", command=create_account, bg="#0066cc", fg="white", font=("Arial", 12, "bold"))
btn_create.grid(row=len(labels), columnspan=2, pady=20)

# KYC Update Tab
tk.Label(frame_kyc, text="Enter Account Number for KYC", font=("Arial", 12), bg="#e6f0ff").pack(pady=10)
kyc_entry = tk.Entry(frame_kyc, width=30)
kyc_entry.pack(pady=5)

kyc_var = tk.StringVar()
kyc_choices = ["Aadhar", "Voter ID", "PAN", "Driving License"]
kyc_dropdown = ttk.Combobox(frame_kyc, textvariable=kyc_var, values=kyc_choices)
kyc_dropdown.pack(pady=5)

def update_kyc():
    try:
        accno = kyc_entry.get()
        kyc_type = kyc_var.get()
        if not accno or not kyc_type:
            raise ValueError("All fields required")
        cur.execute(f"UPDATE ACCOUNT_REGISTRY SET kyc=%s WHERE accno=%s", (kyc_type, accno))
        con.commit()
        messagebox.showinfo("Success", "KYC updated successfully")
    except Exception as e:
        messagebox.showerror("Error", f"KYC update failed: {e}")

tk.Button(frame_kyc, text="Update KYC", command=update_kyc, bg="#0066cc", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

# Modify Info Tab (basic placeholder)
tk.Label(frame_modify, text="Feature under development.", font=("Arial", 12), bg="#e6f0ff").pack(pady=20)

# Search Tab
tk.Label(frame_search, text="Enter Account Number to Search", font=("Arial", 12), bg="#e6f0ff").pack(pady=10)
search_entry = tk.Entry(frame_search, width=30)
search_entry.pack(pady=5)

search_result = tk.Text(frame_search, height=8, width=70)
search_result.pack(pady=10)


def search_account():
    try:
        accno = search_entry.get()
        cur.execute("SELECT * FROM ACCOUNT_REGISTRY WHERE accno=%s", (accno,))
        record = cur.fetchone()
        search_result.delete('1.0', tk.END)
        if record:
            output = tabulate([record], headers=["AccNo", "Name", "Username", "Type", "Balance", "Age", "KYC"], tablefmt="grid")
            search_result.insert(tk.END, output)
        else:
            search_result.insert(tk.END, "No account found.")
    except Exception as e:
        messagebox.showerror("Error", f"Search failed: {e}")

btn_search = tk.Button(frame_search, text="Search", command=search_account, bg="#0066cc", fg="white", font=("Arial", 12, "bold"))
btn_search.pack(pady=5)

root.mainloop()

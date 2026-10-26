import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re

# Connect to MySQL
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="contact_db"
    )
    cur = db.cursor()
except mysql.connector.Error as e:
    print("Database connection error:", e)
    raise SystemExit

root = tk.Tk()
root.title("Contact Manager")
root.geometry("1000x650")

selected_id = None

# Heading
tk.Label(
    root, text="CONTACT MANAGER",
    font=("Arial", 22, "bold")
).pack(pady=10)

# Contact form
form = tk.Frame(root)
form.pack(pady=5)

tk.Label(form, text="Name").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(form, width=35)
name_entry.grid(row=0, column=1, padx=5, pady=4)

tk.Label(form, text="Email").grid(row=1, column=0, sticky="w")
email_entry = tk.Entry(form, width=35)
email_entry.grid(row=1, column=1, padx=5, pady=4)

tk.Label(form, text="Phone").grid(row=2, column=0, sticky="w")
phone_entry = tk.Entry(form, width=35)
phone_entry.grid(row=2, column=1, padx=5, pady=4)

tk.Label(form, text="Category").grid(row=3, column=0, sticky="w")
category_box = ttk.Combobox(
    form,
    values=["Faculty", "Student", "Friend", "Family", "Other"],
    width=32,
    state="readonly"
)
category_box.grid(row=3, column=1, padx=5, pady=4)
category_box.set("Student")

tk.Label(form, text="Notes").grid(row=4, column=0, sticky="w")
notes_entry = tk.Text(form, width=26, height=3)
notes_entry.grid(row=4, column=1, padx=5, pady=4)

# Search
search_entry = tk.Entry(root, width=35)
search_entry.pack(pady=5)

# Contact table
columns = ("ID", "Name", "Email", "Phone", "Category", "Notes")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=140)

table.pack(fill="both", expand=True, padx=10, pady=10)


def clear_fields():
    global selected_id
    selected_id = None

    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    category_box.set("Student")
    notes_entry.delete("1.0", tk.END)


def show_contacts():
    table.delete(*table.get_children())

    sort_column = sort_by.get()
    cur.execute(
        f"SELECT id, name, email, phone, category, notes "
        f"FROM Contact ORDER BY {sort_column}"
    )

    for contact in cur.fetchall():
        table.insert("", tk.END, values=contact)


def save_contact():
    global selected_id

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    category = category_box.get()
    notes = notes_entry.get("1.0", tk.END).strip()

    if not name or not email:
        messagebox.showerror("Error", "Name and email are required")
        return

    if not re.fullmatch(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        email
    ):
        messagebox.showerror("Error", "Invalid email format")
        return

    try:
        cur.execute(
            "SELECT id FROM Contact WHERE email=%s",
            (email,)
        )
        existing = cur.fetchone()

        if existing and existing[0] != selected_id:
            messagebox.showerror(
                "Error", "This email already exists"
            )
            return

        if selected_id is None:
            cur.execute(
                "INSERT INTO Contact "
                "(name, email, phone, category, notes) "
                "VALUES (%s, %s, %s, %s, %s)",
                (name, email, phone, category, notes)
            )
            messagebox.showinfo("Success", "Contact added")
        else:
            cur.execute(
                "UPDATE Contact SET name=%s, email=%s, "
                "phone=%s, category=%s, notes=%s WHERE id=%s",
                (name, email, phone, category, notes, selected_id)
            )
            messagebox.showinfo("Success", "Contact updated")

        db.commit()
        clear_fields()
        show_contacts()

    except mysql.connector.Error as e:
        db.rollback()
        messagebox.showerror("Database Error", str(e))


def select_contact(event):
    global selected_id

    selected = table.selection()
    if not selected:
        return

    values = table.item(selected[0], "values")
    selected_id = int(values[0])

    clear_fields()
    selected_id = int(values[0])

    name_entry.insert(0, values[1])
    email_entry.insert(0, values[2])
    phone_entry.insert(0, values[3] or "")
    category_box.set(values[4] or "Other")
    notes_entry.insert("1.0", values[5] or "")


def delete_contact():
    selected = table.selection()

    if not selected:
        messagebox.showerror("Error", "Select a contact first")
        return

    contact_id = table.item(selected[0], "values")[0]

    if messagebox.askyesno("Confirm", "Delete this contact?"):
        cur.execute("DELETE FROM Contact WHERE id=%s", (contact_id,))
        db.commit()
        clear_fields()
        show_contacts()
        messagebox.showinfo("Success", "Contact deleted")


def search_contact():
    keyword = search_entry.get().strip()

    table.delete(*table.get_children())

    cur.execute(
        "SELECT id, name, email, phone, category, notes "
        "FROM Contact "
        "WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s "
        "ORDER BY name",
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
    )

    for contact in cur.fetchall():
        table.insert("", tk.END, values=contact)


# Buttons
buttons = tk.Frame(root)
buttons.pack(pady=5)

tk.Button(
    buttons, text="Add / Update", command=save_contact
).grid(row=0, column=0, padx=5)

tk.Button(
    buttons, text="Delete", command=delete_contact
).grid(row=0, column=1, padx=5)

tk.Button(
    buttons, text="Clear", command=clear_fields
).grid(row=0, column=2, padx=5)

tk.Button(
    buttons, text="Search", command=search_contact
).grid(row=0, column=3, padx=5)

tk.Button(
    buttons, text="Show All", command=show_contacts
).grid(row=0, column=4, padx=5)

# Sorting
sort_by = tk.StringVar(value="name")

tk.Label(buttons, text="Sort by:").grid(row=0, column=5, padx=5)

ttk.Combobox(
    buttons,
    textvariable=sort_by,
    values=["name", "email"],
    width=10,
    state="readonly"
).grid(row=0, column=6, padx=5)

tk.Button(
    buttons, text="Sort", command=show_contacts
).grid(row=0, column=7, padx=5)

table.bind("<<TreeviewSelect>>", select_contact)

show_contacts()
root.mainloop()

cur.close()
db.close()

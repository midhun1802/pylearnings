import sqlite3, hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial

# DB Code
with sqlite3.connect("Password_vault.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")
print('Tables created')


# create popup
def popup(text):
    answer = simpledialog.askstring("input string", text)

    return answer


# Intial Window
window = Tk()

window.title("Password Vault For Krishna")


def hashPassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    return hash


def firstscreen():
    window.geometry("250x200")

    lbl = Label(window, text="Please Create a Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl1 = Label(window, text="Re-Enter the Password")
    lbl1.pack()

    txt1 = Entry(window, width=20, show="*")
    txt1.pack()
    txt1.focus()

    lbl2 = Label(window)
    lbl2.pack()

    def savePassword():
        if txt.get() == txt1.get():
            hashedPassword = hashPassword(txt.get().encode("utf-8"))

            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?) """
            cursor.execute(insert_password, [(hashedPassword)])
            db.commit()

            passwordvault()

        else:
            lbl2.config(text="Password do not match")

    btn = Button(window, text="Save", command=savePassword)
    btn.pack(pady=15)


def loginscreen():
    window.geometry("450x300")

    lbl = Label(window, text="Please Enter Master KeyPass")
    lbl.config(anchor=CENTER)
    lbl.pack()

    lbl1 = Label(window)
    lbl1.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl1 = Label(window)
    lbl1.pack()

    def getMaserPassword():
        checkHashedPassword = hashPassword(txt.get().encode("utf-8"))
        # we can use the below function to check the decrypted passoword
        # print(checkHashedPassword)
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkHashedPassword)])
        return cursor.fetchall()

    def checkpassword():
        match = getMaserPassword()

        # we can use the below function to check the decrypted passoword
        # print(match)

        if match:
            passwordvault()
        else:
            txt.delete(0, 'end')
            lbl1.config(text="Wrong Password")

    btn = Button(window, text="Submit", command=checkpassword)
    btn.pack(pady=10)


def passwordvault():
    for widget in window.winfo_children():
        widget.destroy()

    def addEntry():
        text1 = "website"
        text2 = "username"
        text3 = "password"

        website = popup(text1)
        username = popup(text2)
        password = popup(text3)

        insert_fields = """INSERT INTO vault(website,username,Password)
        VALUES(?, ?, ?)"""

        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        passwordvault()

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()

        passwordvault()

    window.geometry("1000x450")
    # popup("whats your name")

    lbl = Label(window, text="Password Vault")
    lbl.grid(column=1)
    # If we are using the config we need to use that for all the labels that we are going to use
    # lbl.config(anchor=CENTER)
    # lbl.pack()

    btn = Button(window, text="+", command=addEntry)
    btn.grid(column=1, pady=10)

    lbl = Label(window, text="website")
    lbl.grid(row=2, column=0, padx=80)
    lbl = Label(window, text="username")
    lbl.grid(row=2, column=1, padx=80)
    lbl = Label(window, text="password")
    lbl.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM vault")
    if cursor.fetchall() is not None:
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()

            lbl1 = Label(window, text=(array[i][1]), font=("Helvetica", 12))
            lbl1.grid(column=0, row=i + 3)
            lbl1 = Label(window, text=(array[i][2]), font=("Helvetica", 12))
            lbl1.grid(column=1, row=i + 3)
            lbl1 = Label(window, text=(array[i][3]), font=("Helvetica", 12))
            lbl1.grid(column=2, row=i + 3)

            btn = Button(window, text="Delete", command=partial(removeEntry, array[i][0]))
            btn.grid(column=3, row=i + 3, pady=10)

            i = i + 1

            cursor.execute("SELECT * FROM vault")
            if len(cursor.fetchall()) <= i:
                break


cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginscreen()
else:
    firstscreen()
window.mainloop()

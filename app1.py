from tkinter import Tk
from tkinter import Label
import sys
import time

master = Tk()
master.title("Clock")

def get_time():
    timeVar = time.strftime("%I:%M:%S  %p")
    clock.config(text=timeVar)
    clock.after(200, get_time)

Label(master, font=("Arial", 30), text="Digitalclock", bg="gray", fg="black").pack()
clock = Label(master, font=("Calibri", 90), bg="black", fg="white")
clock.pack()


get_time()


master.mainloop()

#second methode
'''
import time
import tkinter as ui

window = ui.Tk()

def update_clock():
    hours = time.strftime("%I")
    minutes = time.strftime("%M")
    seconds = time.strftime("%S")
    am_or_pm = time.strftime("%p")
    time_text = hours + ":" + minutes + ":" + seconds + "" + am_or_pm
    digital_clock_lbl.config(text=time_text)
    digital_clock_lbl.after(1000, update_clock)

digital_clock_lbl = ui.Label(window, text="00:00:00",
                             font= "Helvetica 72 bold")

digital_clock_lbl.pack()

update_clock()
window.mainloop()
'''
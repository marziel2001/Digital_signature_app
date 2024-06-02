import tkinter as tk
from tkinter.constants import *

window = tk.Tk()

window.rowconfigure([0,1], weight=1 ,minsize=50)
window.columnconfigure([0, 1], weight=1, minsize=50)

frame2 = tk.Frame(master=window,bg='green')
frame2.grid(column=0, row=0, padx=10, pady=10, sticky="ns")

greeting = tk.Label(text="Hello World!", master=frame2, bg='white', font=("Arial"))
greeting.pack(padx=5, pady=5)



frame3 = tk.Frame(master=window, bg='yellow')
frame3.grid(column=1, row=1, padx=10, pady=10, sticky="ns")

greeting2 = tk.Label(text="Hello World2!", master=frame3, bg='white', font=("Arial"))
greeting2.pack(padx=5, pady=5)

# btn1 = tk.Button(text="click-me")
# btn1.pack()
#
# ent1 = tk.Entry()
# ent1.pack()
#
# text1 = tk.Text()
# text1.pack()

tk.mainloop()

#window.destroy()
import tkinter as tk
from src.tKot import TopEntry


def cb(desc, value: str):
    if value != "test":
        raise ValueError("not test")
    print(desc, value)


root = tk.Tk()
TopEntry(
    master=root,
    w=200,
    h=20,
    x=100,
    y=200,
    desc=['1.2.3.4.5.6', '1'],
    value="test",
    callback=cb)
root.mainloop()

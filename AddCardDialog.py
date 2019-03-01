__author__ = "Rick Myers"

import tkinter as tk
from SimpleDialog_Grid import SimpleDialog_Grid


class AddCardDialog(SimpleDialog_Grid):
    def body(self, master):
        tk.Label(master, text="Name:", anchor=tk.W).grid(row=0, sticky='news')
        tk.Label(master, text="Balance:", anchor=tk.W).grid(row=1, sticky='news')
        tk.Label(master, text="Number:", anchor=tk.W).grid(row=2, sticky='news')

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e3 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        return self.e1

    def apply(self):
        name = str(self.e1.get())
        balance = float(self.e2.get())
        number = int(self.e3.get())
        self.result = (name, balance, number)

__author__ = "Rick Myers"

import tkinter as tk
from SimpleDialog_Grid import SimpleDialog_Grid


class AddCardDialog(SimpleDialog_Grid):

    """
    Uses SimpleDialog_Grid instead of tk.simpledialog because tk's version uses the pack manager.
    All of the widgets within this app use the grid manager. Three labels, three entries are
    created to form a simple dialog.  The dialog retrieves data from the user to create a new
    card in the db.
    """

    def body(self, master):
        """
        The dialog requires three valid inputs in order to create a gift card. The labels and
        text entries are then placed into a frame.

        :param master: (tk) parent that opened this dialog window.
        :return:
        """
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
        """
        Closes the window and returns the card data which is then used to create, display,
        and save a gift card to the db.

        :return: (tuple) containing the name, balance, and number to be used to create
        and save a new gift card.
        """
        name = str(self.e1.get())
        balance = float(self.e2.get())
        number = int(self.e3.get())
        self.result = (name, balance, number)

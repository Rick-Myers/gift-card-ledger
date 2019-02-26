__author__ = "Rick Myers"

import tkinter as tk
from GiftCard import GiftCard


class AddCardDialogueWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        self.title("Add Card")
        self.columnconfigure(0, {'minsize': 150, 'pad': 10}, weight=1,)
        self.rowconfigure(0, weight=1)

        card_name = tk.Label(self, text="Card Name: ").grid(sticky='W')
        balance = tk.Label(self, text="Balance: ").grid(row=1, stick="W")
        # card_name_entry = tk.Entry()
        # balance_entry = tk.Entry()
        #
        # card_name_entry.grid(row=0, column=1)
        # balance_entry.grid(row=1, column=1)

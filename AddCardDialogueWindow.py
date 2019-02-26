__author__ = "Rick Myers"

import tkinter as tk
from GiftCard import GiftCard


class AddCardDialogueWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        top = self.top = tk.Toplevel(master)
        self.geometry("100x100")
        self.title("Gift Card Ledger - Add Card")

        card_name = tk.Label(self, text="Card Name: ").grid(sticky='W')
        balance = tk.Label(self, text="Balance: ").grid(row=1, stick="W")
        card_name_entry = tk.Entry()
        balance_entry = tk.Entry()

        card_name_entry.grid(row=0, column=1)
        balance_entry.grid(row=1, column=1)

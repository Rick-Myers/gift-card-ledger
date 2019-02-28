__author__ = "Rick Myers"

import tkinter as tk


class GiftCard(tk.Label):
    """A gift card. For now it only stores the name of the card
       and the balance. It provides a function to update the balance
       if supplied with an amount of money to deduct from its current
       balance."""
    # todo try using args and kwargs. Is this just a wrapper?
    def __init__(self, master, name, balance, bg, fg, pady, anchor):
        self.name = name
        self.balance = balance
        super().__init__(master, text=name, bg=bg, fg=fg, pady=pady, anchor=anchor)

    def update_balance(self, deduction):
        """Updates the balance by reducing the deduction from the current balance."""
        self.balance = float(self.balance) - deduction

    def get_balance(self):
        """Returns the current balance in a money format."""
        formatted_balance = '${:,.2f}'.format(float(self.balance))
        return str(formatted_balance)

    def edit_name(self, new_name):
        self.name = new_name
        self.configure(text=self.name)



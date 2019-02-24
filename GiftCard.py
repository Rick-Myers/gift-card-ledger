__author__ = "Rick Myers"

import tkinter as tk


class GiftCard(tk.Label):
    """A gift card. For now it only stores the name of the card
       and the balance. It provides a function to update the balance
       if supplied with an amount of money to deduct from its current
       balance."""

    def __init__(self, master, name, balance, bg, fg, pady):
        self.name = name
        self.balance = balance
        super().__init__(master, text=self.details(), bg=bg, fg=fg, pady=pady)

    def update_balance(self, deduction):
        """Updates the balance by reducing the deduction from the current balance."""
        self.balance = float(self.balance) - deduction

    def details(self):
        """Returns the current balance in a money format."""
        formatted_balance = '${:,.2f}'.format(float(self.balance))
        return self.name + ": " + str(formatted_balance)



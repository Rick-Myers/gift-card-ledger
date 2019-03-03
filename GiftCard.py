__author__ = "Rick Myers"

import tkinter as tk

# todo start using date to record history.


class GiftCard(tk.Label):
    """A gift card. For now it only stores the name of the card
       and the balance. It provides a function to update the balance
       if supplied with an amount of money to deduct from its current
       balance."""
    # todo start here and change parameters to (name, balance, number) -> then the restg
    def __init__(self, master, name, balance, number, history, starting_balance):
        self.master = master
        self.name = name
        self.balance = balance
        self.starting_balance = starting_balance
        self.balance_label = self._create_label()
        self.number = number
        self.history = history
        super().__init__(master, text=name, bg="lightgrey", fg="black", pady=10, anchor=tk.W)

    def _create_label(self):
        return tk.Label(self.master, text=self.formatted_balance(), anchor='e')

    def update_balance(self, new_balance):
        """Updates the balance by given balance and updated associated balance label."""
        self.balance = new_balance
        self.balance_label.configure(text=self.formatted_balance())

    def formatted_balance(self):
        """Returns the current balance in a money format."""
        formatted_balance = '${:,.2f}'.format(float(self.balance))
        return str(formatted_balance)

    @staticmethod
    def format_balance(balance):
        """Returns the current balance in a money format."""
        formatted_balance = '${:,.2f}'.format(float(balance))
        return str(formatted_balance)

    def destroy(self):
        self.balance_label.destroy()
        super().destroy()

    def edit_name(self, new_name):
        self.name = new_name
        self.configure(text=self.name)

    def update_the_balance(self, new_balance):
        self.balance = new_balance
        self.balance_label.configure(text=self.balance)

__author__ = "Rick Myers"

import tkinter as tk


class GiftCard(tk.Label):
    """The gift card is a label. It keeps track of gift card related data such as
    the starting balance. It also keeps track of two tkinter labels. The balance
     label is used to display the gift cards balance in a separate column.
    """
    def __init__(self, master, name, balance, number, history, starting_balance):
        """
        parameter: master (TK) - the window that called this window
        parameter: name (str) - gift card company name
        parameter: balance (float) - gift card current balance
        parameter: number (int) - the number used to identify the card with the company that it belongs too
        parameter: history (str) - history of all transactions
        parameter: starting_balance (float) 
        """
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
        """Updates the balance by given balance and updated associated balance label.
        This will update the cards balance (and its associated label) and the balance
        label.
        parameter: new_balance (float)"""
        self.balance = new_balance
        self.balance_label.configure(text=self.formatted_balance())

    def formatted_balance(self):
        """Returns the current balance in a string that is formatted for printing as currency.
        return: string
        example: if self.balance == 3.0 then format_balance() == $3.00"""
        formatted_balance = '${:,.2f}'.format(float(self.balance))
        return str(formatted_balance)

    @staticmethod
    def format_balance(balance):
        """This function will convert a given float/integer into a string that is
        formatted for printing as currency.
        parameter: balance (float)
        return: string
        example: format_balance(3.0) == $3.00"""
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

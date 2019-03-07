__author__ = "Rick Myers"

import tkinter as tk


class GiftCard(tk.Label):

    """

    The gift card is a label. It keeps track of gift card related data such as
    the starting balance. It also keeps track of two tkinter labels. The balance
    label is used to display the gift cards balance in a separate column. The gift
    cards label is used to display the name of the gift card and is used as an
    event listener.

    """

    def __init__(self, master, name, balance, number, history, starting_balance):
        """
        :param master: (tkinter) The window that this widget will be displayed in.
        :param name: (str) The name of the company that the gift card belongs too.
        :param balance: (float) Current balance.
        :param number: (int) Identification number found on the front of the card.
        :param history: (str) History of all transactions.
        :param starting_balance: (float) Stores starting balance so that it does not need to be calculated.
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
        """Return a label that will be used to display the current balance.

        :return: (Label) formatted to display the current balance of the gift card.
        """
        return tk.Label(self.master, text=self.formatted_balance(), anchor='e')

    def update_balance(self, new_balance):
        """Update the card's balance and label to be equal to the given balance.

        :param new_balance: (float) representing the new balance to be set.
        """
        self.balance = new_balance
        self.balance_label.configure(text=self.formatted_balance())

    def formatted_balance(self):
        """Return a string representation of the current balance.

        :return: (str) formatted for printing as currency.
        """
        formatted_balance = '${:,.2f}'.format(float(self.balance))
        return str(formatted_balance)

    def destroy(self):
        """This is called to remove a gift card from view. The gift card label is destroyed
        and the gift card's balance label is also destroyed.
        """
        self.balance_label.destroy()
        super().destroy()

    @staticmethod
    def format_balance(balance):
        """Convert a given float/integer into a string and format for printing as currency.

        :param balance: (float) The balance to be formatted.
        :return: A string representing the balance formatted to a standard US currency. For example, "$3.00".
        """
        formatted_balance = '${:,.2f}'.format(float(balance))
        return str(formatted_balance)



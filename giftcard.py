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

    def __init__(self, master: tk, name: str, balance: float, number: int, history: str, starting_balance: float):
        """
        :param master: The window that this widget will be displayed in.
        :param name: The name of the company that the gift card belongs too.
        :param balance: Current balance.
        :param number: Identification number found on the front of the card.
        :param history: History of all transactions.
        :param starting_balance: Stores starting balance so that it does not need to be calculated.
        """
        self.master = master
        self.name = name
        self.balance = balance
        self.starting_balance = starting_balance
        self.number = number
        self.history = history
        super().__init__(master, text=name, bg="lightgrey", fg="black", pady=10, anchor=tk.W)

    def update_balance(self, new_balance: float):
        """Update the card's balance and label to be equal to the given balance.

        :param new_balance: Representing the new balance to be set.
        """
        self.balance = new_balance

    def formatted_balance(self) -> str:
        """Return a string representation of the current balance.

        :return: Formatted for printing as currency.
        """
        formatted_balance = '${:,.2f}'.format(float(self.balance))
        return str(formatted_balance)

    def destroy(self):
        """This is called to remove a gift card from view. The gift card label is destroyed
        and the gift card's balance label is also destroyed.
        """
        super().destroy()

    def set_card_color(self, color: dict):
        """
        Sets the color of the label.

        :param color: A dictionary containing the background and foreground color to be set.
        """
        self.configure(bg=color["bg"], fg=color["fg"])

    @staticmethod
    def format_balance(balance: float) -> str:
        """Convert a given float/integer into a string and format for printing as currency.

        :param balance: The balance to be formatted.
        :return: Balance formatted to a standard US currency. For example, "$3.00".
        """
        formatted_balance = '${:,.2f}'.format(float(balance))
        return str(formatted_balance)



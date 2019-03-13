__author__ = "Rick Myers"

import tkinter as tk
import tkinter.messagebox as mbox
import typing

from simple_dialog import SimpleDialogGrid


class AddCardDialog(SimpleDialogGrid):

    """

    Uses SimpleDialog_Grid instead of tk.simpledialog for inheritance because tk's version uses
    the pack manager. All of the widgets within this app use the grid manager. Three labels,
    three entries are created to form a simple dialog.  The dialog retrieves data from the user
    to create a new card in the db.

    """

    def body(self, master: tk) -> tk.Entry:
        """
        Build the body for the window. The dialog requires three valid inputs in
        order to create a gift card. The labels and text entries are then placed into a frame.

        :param master: Parent that opened this dialog window."""
        tk.Label(master, text="Name:", anchor=tk.W, bg="Light Blue").grid(row=0, sticky=tk.NSEW)
        tk.Label(master, text="Balance:", anchor=tk.W, bg="Light Blue").grid(row=1, sticky=tk.NSEW)
        tk.Label(master, text="Number:", anchor=tk.W, bg="Light Blue").grid(row=2, sticky=tk.NSEW)

        self.name_entry = tk.Entry(master)
        self.balance_entry = tk.Entry(master)
        self.number_entry = tk.Entry(master)

        self.name_entry.grid(row=0, column=1)
        self.balance_entry.grid(row=1, column=1)
        self.number_entry.grid(row=2, column=1)

        self.new_name = None
        self.new_balance = None
        self.new_number = None

        return self.name_entry

    def apply(self):
        """
        Close the window and save the card data which is then used to create, display,
        and save a gift card to the db.

        self.result is set to the name, balance, and number to be used to create
        and save a new gift card.
        """
        self.result = (self.new_name, self.new_balance, self.new_number)

    def validate(self) -> bool:
        """
        Validate user input before allowing to return to the previous window.

        :return: True if all user input is valid, false otherwise.
        """
        self.new_name = self._validate_name()
        if not self.new_name:
            return False

        self.new_balance = self._validate_balance()
        if not self.new_balance:
            return False

        self.new_number = self._validate_number()
        if not self.new_number:
            return False

        return True

    def _validate_name(self) -> typing.Union[bool, str]:
        """
        Validate the input of the name entry.

        :return: False if incorrect name submitted, str otherwise.
        """
        name = str(self.name_entry.get())
        if not name:
            mbox.showerror("Error", "Enter a card name.")
            self.name_entry.delete(0, tk.END)
            return False
        else:
            return name

    def _validate_balance(self) -> typing.Union[bool, float]:
        """
        Validate the input of the balance entry.

        :return: False if incorrect balance submitted, float otherwise.
        """
        try:
            balance = float(self.balance_entry.get())
        except ValueError:
            mbox.showerror("Error", "Invalid balance.")
            return False
        return balance

    def _validate_number(self) -> typing.Union[bool, int]:
        """
        Validate the input of the number entry.

        :return: False if incorrect number submitted, int otherwise.
        """
        try:
            number = int(self.number_entry.get())
        except ValueError:
            mbox.showerror("Error", "Invalid card number.")
            return False
        return number


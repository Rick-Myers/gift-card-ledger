#!/usr/bin/env python3

__author__ = "Rick Myers"

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mbox
import os
import sqlite3
import typing
import itertools
from datetime import date

from giftcard import GiftCard
from add_dialog import AddCardDialog
from edit_dialog import EditCardDialog


class GiftCardLedger(tk.Tk):
    """

    This is the main window for this application and the first window
    presented to the user. A list of gift cards will display on this
    window. Right clicking on a gift card will trigger the edit card
    dialog. Left clicking on a gift card will trigger the delete card
    dialog. Gift cards are stored and retrieved from a sqlite database.

    """
    def __init__(self, *args, **kwargs):
        """Initialize the root window and create card list view of
        all cards within db. If this is the first time launching,
        a blank list will be displayed.
        """
        super().__init__(*args, **kwargs)

        self.title("Gift Card Ledger")
        self.configure(background="Gray")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.cards_list = []
        self.color_gen = itertools.cycle([{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}])

        # Create main window frame
        main_frame = tk.Frame(self, bg="Light Blue", bd=3, relief=tk.RIDGE)
        main_frame.grid(sticky=tk.NSEW)
        main_frame.columnconfigure(0, weight=1)

        # Create label that appears at the top. It displays what screen is currently active.
        # todo remove and use simple menu... maybe... I kinda like it.
        top_label_var = tk.StringVar(main_frame)
        top_label = tk.Label(main_frame, textvar=top_label_var, fg="black", bg="Light Blue", font=('Terminal', 20))
        top_label.grid(row=0, column=0, pady=5, sticky=tk.NW)
        top_label_var.set("Gift Card Ledger")

        # Create a frame for the canvas and scrollbar.
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.grid(row=2, column=0, sticky=tk.NW)

        # Add a canvas into the canvas frame.
        self.card_list_canvas = tk.Canvas(canvas_frame)
        self.card_list_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.card_list_canvas.grid(row=0, column=0)

        # Create a vertical scrollbar linked to the canvas.
        scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.card_list_canvas.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.card_list_canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame on the canvas to contain the list of cards.
        self.cards_list_frame = tk.Frame(self.card_list_canvas, bd=2)
        self.cards_list_frame.columnconfigure(0, {'minsize': 200, 'pad': 10})

        # Add cards to the frame from database
        for card in self.load():
            self.add_card(card, True)

        # Create canvas window after cards have been added.
        self.card_list_canvas.create_window((0, 0), window=self.cards_list_frame, anchor=tk.NW)

        # Redraws widgets within frame and creates bounding box access.
        self.cards_list_frame.update_idletasks()
        # Get bounding box of canvas with the cards list.
        cards_list_bbox = self.card_list_canvas.bbox(tk.ALL)

        # Set the scrollable region to the height of the cards list canvas bounding box
        # Reconfigure the card list canvas to be the same size as the bounding box
        w, _ = cards_list_bbox[2], cards_list_bbox[3]
        if w <= 243:
            w = 243
        self.card_list_canvas.configure(scrollregion=cards_list_bbox, width=w, height=120)

        # Button for adding a new card and the frame it is in.
        buttons_frame = tk.Frame(main_frame, bd=2, relief=tk.GROOVE)
        buttons_frame.grid(row=5, column=0, pady=5, sticky=tk.SE)
        add_card_button = ttk.Button(buttons_frame, text="Add Card", command=self.add_card_dialog)
        add_card_button.grid(row=0, column=0)

        # root window binds
        self.bind("<Configure>", self.scroll_region_resize)

        self.resizable(False, False)

    def remove_card(self, event: typing.Optional[tk.Event] = None):
        """
        Remove the card from view and delete from database.

        :param event: Triggered when a card is deleted.
        """
        card = event.widget
        if mbox.askyesno("Are you sure?", "Delete " + card.name + "?"):
            # remove from list
            self.cards_list.remove(card)
            # remove from canvas frame
            card.destroy()
            # remove from db
            sql_remove_card = """DELETE FROM gift_cards
                                 WHERE name=? AND number=?
                                 """
            card_data = (card.name, card.number)
            self.run_query(sql_remove_card, card_data)
            # update card grid positions and colors
            self.update_rows()
            self.recolor_cards()

    def add_card(self, card_data: tuple, from_db: typing.Optional[bool] = False):
        """
        Create and display a gift card. This will create cards that are read in
        during load, or when a new card is created.

        :param card_data: Either length three or five. Three if new, five
        loaded from db. (name, balance, number, history, starting balance)
        :param from_db: True if from db, false otherwise.
        """
        # the row index is the number of widgets within the first column of the frame
        row_index = len(self.cards_list_frame.grid_slaves(column=0))

        name, balance, number = (card_data[0], card_data[1], card_data[2])
        # if the cards re from the db, we load their data. If not, we have to create a history and starting balance.
        if from_db:
            history, starting_balance = (card_data[3], card_data[4])
        else:
            starting_balance = balance
            history = "{} -> {}\n".format(date.today(), GiftCard.format_balance(starting_balance))
        # create gift card
        card = GiftCard(self.cards_list_frame, name, balance, number, history, starting_balance)
        # bind gift card actions
        card.bind("<Button-1>", self.remove_card)
        card.bind("<Button-3>", self.edit_card_dialog)
        # add gift card and label to grid
        self.set_card_color(card)
        card.grid(row=row_index, column=0, sticky=tk.NSEW)
        card.balance_label.grid(row=row_index, column=1, sticky='nws')
        # add to gift card list
        self.cards_list.append(card)
        # insert into db if card didn't come from db
        if not from_db:
            self.save(card)

    def save(self, card: GiftCard):
        """
        Save the newly added gift card to the database.

        :param card: New data to be saved.
        """
        sql_add_card = """INSERT INTO gift_cards
                          VALUES (?, ?, ?, ?, ?)
                          """
        card_data = (card.name, card.balance, card.number, card.history, card.starting_balance)
        self.run_query(sql_add_card, card_data)

    def load(self) -> list:
        """
        Load gift card data from sql database.

        :return: A list of GiftCard data.
        """
        sql_load_cards = """SELECT name, balance, number, history, starting_balance
                            FROM gift_cards
                            """
        return self.run_query(sql_load_cards, receive=True)

    def scroll_region_resize(self, event: typing.Optional[tk.Event] = None):
        """
        Configure scrolling region to accommodate adding and removing labels to the canvas.
        :param event: Triggered when labels are added or removed.
        """
        self.card_list_canvas.configure(scrollregion=self.card_list_canvas.bbox(tk.ALL))

    def add_card_dialog(self):
        """Open the add card dialog and save results to the database if a card is added that doesn't exist."""
        dialog = AddCardDialog(self)
        # start new window and wait for it to return before allowing user to edit previous window
        self.wait_window(dialog)
        # Save card to db if it doesn't already exist, otherwise do nothing.
        if dialog.result:
            sql_check_exists = """SELECT * FROM gift_cards
                                  WHERE name = ? AND number = ?
                                  """
            data = (dialog.result[0], dialog.result[2])
            exists = GiftCardLedger.run_query(sql_check_exists, data, receive=True)
            # Check if card exists in DB
            if not exists:
                self.add_card(dialog.result)

    def edit_card_dialog(self, event: tk.Event):
        """
        Open the edit card dialog window and save the results to the database if any changes
        are made. The window will display the view to allow the user to edit the balance of
        a gift card. The main window will be inactive until the dialog window is closed.

        :param event: Triggered by right clicking on a gift card.
        """
        card = event.widget
        dialog = EditCardDialog(self, card)
        self.wait_window(dialog)
        # Update card in db, otherwise do nothing.
        if dialog.result:
            self._update_card_db(card, dialog.result[0], dialog.result[1])

    def _update_card_db(self, card: tk.Label, new_balance: float, new_history: str):
        """
        Update the card's balance and history, then save changes to db.

        :param card: GiftCard's label.
        :param new_balance: New balance that was set in edit card dialog.
        :param new_history: New history pertaining to card balance changes.
        """
        card.update_balance(new_balance)
        card.history = new_history

        sql_update_balance = """UPDATE gift_cards 
                                SET balance = ?,
                                    history = ? 
                                WHERE name = ? AND number = ?
                                """
        data = (new_balance, new_history, card.name, card.number)
        self.run_query(sql_update_balance, data)

    def update_rows(self):
        """Iterate through card list and adjust row indices to insure
        there are no empty spaces."""
        # todo only update rows underneath the deleted row
        for row_index, card in enumerate(self.cards_list):
            card.grid(row=row_index)
            card.balance_label.grid(row=row_index)

    def recolor_cards(self):
        """Iterate through card list and recolor all labels"""
        for card in self.cards_list:
            self.set_card_color(card)

    def _on_mousewheel(self, event: tk.Event):
        """
        Scroll the canvas up or down by 1 unit when the mouse wheel is scrolled.

        :param event: Triggered when scrolling the mouse wheel.
        """
        self.card_list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def set_card_color(self, card: GiftCard):
        """
        Sets the color of the label and maintains that the colors
        of the listed labels alternate.

        :param card: GiftCard's label.
        """
        color = next(self.color_gen)

        card.configure(bg=color["bg"], fg=color["fg"])
        card.balance_label.configure(bg=color["bg"], fg=color["fg"])

    @staticmethod
    def run_query(sql: str, data: typing.Optional[str] = None, receive: typing.Optional[bool] = None) -> list:
        """Run all DML components of SQL language.

        :param sql: An SQL query string.
        :param data: Data needed to complete the SQL query.
        :param receive: True if query will produce results, false otherwise.
        :return: Results of the query.
        """
        db_conn = sqlite3.connect('gift_cards.db')
        db_cursor = db_conn.cursor()

        # if data is supplied, it is inserted. If not, only the command is executed
        if data:
            db_cursor.execute(sql, data)
        else:
            db_cursor.execute(sql)
        # if is true, return the requested rows. If not, commit to database.
        if receive:
            return db_cursor.fetchall()
        else:
            db_conn.commit()
        db_conn.close()

    @staticmethod
    def initialize_db():
        """Initialize SQLite3 database if no database named gift_cards is found."""
        sql_create_table = """CREATE TABLE gift_cards (
                                name TEXT, 
                                balance REAL, 
                                number INTEGER, 
                                history DATE, 
                                starting_balance REAL)
                                """
        GiftCardLedger.run_query(sql_create_table)

        sql_insert_card = """INSERT INTO gift_cards
                                VALUES (?, ?, ?, ?, ?)
                                """
        initial_date = "{} -> {}".format(date.today(), "$77.77\n")
        card = ("Delete Me", 77.77, 7777777, initial_date, 77.77)
        GiftCardLedger.run_query(sql_insert_card, card)


if __name__ == "__main__":
    if not os.path.isfile('gift_cards.db'):
        GiftCardLedger.initialize_db()
    gift_card_ledger = GiftCardLedger()
    gift_card_ledger.mainloop()

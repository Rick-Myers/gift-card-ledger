__author__ = "Rick Myers"

import tkinter as tk
import tkinter.messagebox as mbox
import os
import sqlite3
from GiftCard import GiftCard
from AddCardDialog import AddCardDialog
from EditCardDialog import EditCardDialog
from datetime import date


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
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Gift Card Ledger")
        self.configure(background="Gray")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.cards_list = []
        self.color_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

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
        # todo set without using hard numbers, height is currently manually set
        w, _ = cards_list_bbox[2], cards_list_bbox[3]
        if w <= 243:
            w = 243
        self.card_list_canvas.configure(scrollregion=cards_list_bbox, width=w, height=120)

        # Button for adding a new card and the frame it is in.
        buttons_frame = tk.Frame(main_frame, bd=2, relief=tk.GROOVE)
        buttons_frame.grid(row=5, column=0, pady=5, sticky=tk.SE)
        add_card_button = tk.Button(buttons_frame, text="Add Card", command=self.add_card_dialog)
        add_card_button.grid(row=0, column=0)

        # root window binds
        self.bind("<Configure>", self.scroll_region_resize)

    def remove_card(self, event=None):
        """
        Remove the card from view and delete from database.

        :param event: (tkinter.Event) Triggered when a card is deleted.
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

    def add_card(self, card_data, from_db=False):
        """
        Create and display a gift card. This will create cards that are read in
        during load, or when a new card is created.

        :param card_data: (tuple) Either length three or five. Three if new, five
        loaded from db. (name, balance, number, history, starting balance)
        :param from_db: (bool) True if from db, false otherwise.
        """
        # the row index is the number of widgets within the first column of the frame
        row_index = len(self.cards_list_frame.grid_slaves(column=0))

        name, balance, number = (card_data[0], card_data[1], card_data[2])
        # if the cards re from the db, we load their data. If not, we have to create a history and starting balance.
        if from_db:
            history, starting_balance = (card_data[3], card_data[4])
        else:
            starting_balance = balance
            history = str(date.today()) + " -> {}{}".format(GiftCard.format_balance(starting_balance), "\n")
        # create gift card
        card = GiftCard(self.cards_list_frame, name, balance, number, history, starting_balance)
        # bind gift card actions
        card.bind("<Button-1>", self.remove_card)
        card.bind("<Button-3>", self.edit_card_dialog)
        # add gift card and label to grid
        self.set_card_color(len(self.cards_list), card)
        card.grid(row=row_index, column=0, sticky=tk.NSEW)
        card.balance_label.grid(row=row_index, column=1, sticky='nws')
        # add to gift card list
        self.cards_list.append(card)
        # insert into db if card didn't come from db
        if not from_db:
            self.save(card)

    def save(self, card):
        """
        Save the newly added gift card to the database.

        :param card: (GiftCard) New data to be saved.
        """
        sql_add_card = """INSERT INTO gift_cards
                          VALUES (?, ?, ?, ?, ?)
                          """
        card_data = (card.name, card.balance, card.number, card.history, card.starting_balance)
        self.run_query(sql_add_card, card_data)

    def load(self):
        """
        Load gift card data from sql database.

        :return: (list) A list of GiftCard objects.
        """
        sql_load_cards = """SELECT name, balance, number, history, starting_balance
                            FROM gift_cards
                            """
        return self.run_query(sql_load_cards, receive=True)

    def scroll_region_resize(self, event=None):
        """
        Configure scrolling region to accommodate adding and removing labels to the canvas.
        :param event: (tkinter.Event) Triggered when labels are added or removed.
        """
        self.card_list_canvas.configure(scrollregion=self.card_list_canvas.bbox(tk.ALL))

    def add_card_dialog(self):
        """Open the add card dialog and save results to the database if a card is added."""
        dialog = AddCardDialog(self)
        # start new window and wait for it to return before allowing user to edit previous window
        self.wait_window(dialog)
        # Save card to db, otherwise do nothing.
        if dialog.result:
            self.add_card(dialog.result)

    def edit_card_dialog(self, event):
        """
        Open the edit card dialog window and save the results to the database if any changes
        are made. The window will display the view to allow the user to edit the balance of
        a gift card. The main window will be inactive until the dialog window is closed.

        :param event: (tkinter.Event) The event triggered by right clicking on a gift card.
        """
        card = event.widget
        dialog = EditCardDialog(self, card)
        self.wait_window(dialog)
        # Update card in db, otherwise do nothing.
        if dialog.result:
            self._update_card_db(card, dialog.result[0], dialog.result[1])

    def _update_card_db(self, card, new_balance, new_history):
        """
        Update the card's balance and history, then save changes to db.

        :param card: (Label) GiftCard's label.
        :param new_balance: (float) New balance that was set in edit card dialog.
        :param new_history: (str) New history pertaining to card balance changes.
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
        for index, card in enumerate(self.cards_list):
            self.set_card_color(index, card)

    def set_card_color(self, index, card):
        """
        Sets the color of the label and maintains that the colors
        of the listed labels alternate.

        :param index: (int) Current row index.
        :param card: (Label) GiftCard's label.
        """
        _, card_style_choice = divmod(index, 2)

        my_scheme_choice = self.color_schemes[card_style_choice]

        card.configure(bg=my_scheme_choice["bg"])
        card.configure(fg=my_scheme_choice["fg"])
        card.balance_label.configure(bg=my_scheme_choice["bg"])
        card.balance_label.configure(fg=my_scheme_choice["fg"])

    @staticmethod
    def run_query(sql, data=None, receive=None):
        """Run all DML components of SQL language.

        :param sql: (str) An SQL query string.
        :param data: (str) Data needed to complete the SQL query.
        :param receive: (bool) True if query will produce results, false otherwise.
        :return: (list) Results of the query.
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
        initial_date = str(date.today()) + " -> {}".format("$77.77\n")
        card = ("Delete Me", 77.77, 7777777, initial_date, 77.77)
        GiftCardLedger.run_query(sql_insert_card, card)


if __name__ == "__main__":
    if not os.path.isfile('gift_cards.db'):
        GiftCardLedger.initialize_db()
    gift_card_ledger = GiftCardLedger()
    gift_card_ledger.mainloop()

'''
#used to print a list of font families available on the system.
from tkinter import Tk, font
root = Tk()
print(font.families())

#used to print current bounding box of frame
print('canvas.cards_list_bbox(tk.ALL): {}'.format(cards_list_bbox))

#used to print column names of specific table
connection = sqlite3.connect('gift_cards.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info(gift_cards)")
    print(cursor.fetchall())
    connection.close()
'''
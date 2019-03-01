__author__ = "Rick Myers"

import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import PhotoImage
import os
import sqlite3
from GiftCard import GiftCard
from AddCardDialog import AddCardDialog


class GiftCardLedger(tk.Tk):
    # todo adjust widget bg= colors after layout is complete
    def __init__(self, cards_list=None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        if not cards_list:
            self.cards_list = []
        else:
            self.cards_list = cards_list

        self.title("Gift Card Ledger")
        self.configure(background="Gray")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        main_frame = tk.Frame(self, bg="Light Blue", bd=3, relief=tk.RIDGE)
        main_frame.grid(sticky=tk.NSEW)
        main_frame.columnconfigure(0, weight=1)

        # Screen label that appears at the top. It displays what screen is currently active.
        # todo remove and use simple menu
        top_label_var = tk.StringVar(main_frame)
        top_label = tk.Label(main_frame, textvar=top_label_var, fg="black", bg="white", font=('Terminal', 20))
        top_label.grid(row=0, column=0, pady=5, sticky=tk.NW)
        top_label_var.set("Gift Card Ledger")

        # Create a frame for the canvas and scrollbar.
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.grid(row=2, column=0, sticky=tk.NW)

        # Add a canvas into the canvas frame.
        self.card_list_canvas = tk.Canvas(canvas_frame, bg="Yellow")
        self.card_list_canvas.grid(row=0, column=0)

        # Create a vertical scrollbar linked to the canvas.
        scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.card_list_canvas.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.card_list_canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame on the canvas to contain the list of cards.
        self.cards_list_frame = tk.Frame(self.card_list_canvas, bg="Red", bd=2)
        self.cards_list_frame.columnconfigure(0, {'minsize': 200, 'pad': 10})

        # Add cards to the frame
        for card in self.load():
            self.add_card(card, True)

        # Create canvas window to hold the cards_list_frame.
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
        buttons_frame = tk.Frame(main_frame, bg="Blue", bd=2, relief=tk.GROOVE)
        buttons_frame.grid(row=5, column=0, pady=5, sticky=tk.SE)
        add_card_button = tk.Button(buttons_frame, text="Add Card", command=self.add_card_dialogue)
        add_card_button.grid(row=0, column=0, padx=2, pady=10)


        # root window binds
        self.bind("<Configure>", self.canvas_configure)
        # self.card_list_canvas.bind("<Configure>", self.card_width)

    def remove_card(self, event=None):
        card = event.widget
        if mbox.askyesno("Are you sure?", "Delete " + card.name + "?"):
            # remove from list
            self.cards_list.remove(card)
            # remove from canvas frame
            card.destroy()
            # todo remove from db
            sql_remove_card = "DELETE FROM gift_cards WHERE name=? AND balance=?"
            card_data = (card.name, card.balance)
            self.run_query(sql_remove_card, card_data)
            # update card grid positions.
            self.update_rows()
            # todo recolor

    def add_card(self, card_data, from_db=False):
        # the row index is the number of widgets within the first column of the frame
        row_index = len(self.cards_list_frame.grid_slaves(column=0))
        # create gift card
        card = GiftCard(self.cards_list_frame, card_data[0], card_data[1], "lightgrey", "black", 10, anchor='w')
        # bind card actions
        card.bind("<Button-1>", self.remove_card)
        # add to card and label to grid
        # todo overload grid() to add balance label when card is added to grid
        card.grid(row=row_index, column=0, sticky='news')
        card.balance_label.grid(row=row_index, column=1, sticky='nws')
        # add to gift card list
        self.cards_list.append(card)
        if not from_db:
            self.save(card)

    def card_width(self, event):
        frame_width = event.width
        self.card_list_canvas.itemconfig(self.cards_frame, width=frame_width)

    def save(self, card):
        sql_add_card = "INSERT INTO gift_cards VALUES (?, ?)"
        card_data = (card.name, card.balance)
        self.run_query(sql_add_card, card_data)

    def load(self):
        sql_load_cards = "SELECT * FROM gift_cards"
        return self.run_query(sql_load_cards, receive=True)

    @staticmethod
    def run_query(sql, data=None, receive=None):
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
        sql_create_table = "CREATE TABLE gift_cards (name TEXT, balance REAL)"
        GiftCardLedger.run_query(sql_create_table)

        sql_insert_card = "INSERT INTO gift_cards VALUES (?, ?)"
        card = ("Delete Me", 77.77)
        GiftCardLedger.run_query(sql_insert_card, card)


    def canvas_configure(self, event=None):
        self.card_list_canvas.configure(scrollregion=self.card_list_canvas.bbox(tk.ALL))


    def add_card_dialogue(self):
        # todo check if None before attempting to make a card... the user may have exited early
        dialog = AddCardDialog(self)
        self.wait_window(dialog)
        self.add_card(dialog.result)

    def update_rows(self):
        # todo only update rows underneath the deleted row
        for row_index, card in enumerate(self.cards_list):
            card.grid(row=row_index)
            card.balance_label.grid(row=row_index)

    def temp_card_list_maker(self):
        test_card = GiftCard(self.cards_list_frame, "Card A", 11.11, "lightgrey", "black", 5, anchor='w')
        test_card2 = GiftCard(self.cards_list_frame, "Card B", 22.22, "lightgrey", "black", 5, anchor='w')
        test_card3 = GiftCard(self.cards_list_frame, "Card C", 33.33, "lightgrey", "black", 10, anchor='w')
        test_card4 = GiftCard(self.cards_list_frame, "Card D", 44.44, "lightgrey", "black", 10, anchor='w')
        self.cards_list.append(test_card)
        self.cards_list.append(test_card2)
        self.cards_list.append(test_card3)
        self.cards_list.append(test_card4)


if __name__ == "__main__":
    if not os.path.isfile('gift_cards.db'):
        GiftCardLedger.initialize_db()
    gift_card_ledger = GiftCardLedger()
    gift_card_ledger.mainloop()

'''
used to print a list of font families available on the system.
rom tkinter import Tk, font
root = Tk()
print(font.families())
used to print current bounding box of frame
#print('canvas.cards_list_bbox(tk.ALL): {}'.format(cards_list_bbox))
'''
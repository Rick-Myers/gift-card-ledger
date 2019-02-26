__author__ = "Rick Myers"

import tkinter as tk
from tkinter import PhotoImage
from GiftCard import GiftCard
from AddCardDialogueWindow import AddCardDialogueWindow


class GiftCardLedger(tk.Tk):
    # todo adjust frame colors after layout is complete
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

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
        card_list_canvas = tk.Canvas(canvas_frame, bg="Yellow")
        card_list_canvas.grid(row=0, column=0)

        # Create a vertical scrollbar linked to the canvas.
        scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=card_list_canvas.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        card_list_canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame on the canvas to contain the list of cards.
        cards_list_frame = tk.Frame(card_list_canvas, bg="Red", bd=2)
        # todo add as global variables?
        cards_list_frame.columnconfigure(0, {'minsize': 200, 'pad': 10})

        # ------------------------------------------------------------------------------------------------------
        # Testing Data
        # Add cards to the frame
        # todo use list of cards to iterate through
        test_card = GiftCard(cards_list_frame, "Subway", 23.74, "lightgrey", "black", 5, anchor='w')
        test_card.bind("<Button-1>", self.remove_card)
        test_card.grid(row=0, column=0, sticky='news')
        test_label = tk.Label(cards_list_frame, text=test_card.get_balance(), anchor='e')
        test_label.grid(row=0, column=1, sticky='nws')

        test_card2 = GiftCard(cards_list_frame, "Test Card", 23.74, "lightgrey", "black", 5, anchor='w')
        test_card2.grid(row=1, column=0, sticky='news')
        test_card3 = GiftCard(cards_list_frame, "Test Card", 23.74, "lightgrey", "black", 10, anchor='w')
        test_card3.grid(row=2, column=0, sticky='news')
        test_card4 = GiftCard(cards_list_frame, "Test Card", 23.74, "lightgrey", "black", 10, anchor='w')
        test_card4.grid(row=3, column=0, sticky='news')
        # ------------------------------------------------------------------------------------------------------

        # Create canvas window to hold the cards_list_frame.
        card_list_canvas.create_window((0, 0), window=cards_list_frame, anchor=tk.NW)

        # Needed to make cards_list_bbox info available?
        cards_list_frame.update_idletasks()
        # Get bounding box of canvas with the cards list.
        cards_list_bbox = card_list_canvas.bbox(tk.ALL)
        # print('canvas.cards_list_bbox(tk.ALL): {}'.format(cards_list_bbox))

        # Set the scrollable region to the width of the cards list canvas bounding box
        # todo set without using hard numbers
        w, _ = cards_list_bbox[2], cards_list_bbox[3]
        card_list_canvas.configure(scrollregion=cards_list_bbox, width=w, height=121)

        buttons_frame = tk.Frame(main_frame, bg="Blue", bd=2, relief=tk.GROOVE)
        buttons_frame.grid(row=5, column=0, sticky=tk.SE)

        add_card_button = tk.Button(buttons_frame, text="Add Card")
        add_card_button.grid(row=0, column=0, padx=2, pady=10)

    def remove_card(self, event):
        print("Removing a card!")

    def add_card(self, event):
        print("Opening the add card screen!")

    def add_card_dialogue(self):
        dialogue = AddCardDialogueWindow(self)
        self.wait_window(dialogue)


if __name__ == "__main__":
    gift_card_ledger = GiftCardLedger()
    gift_card_ledger.mainloop()

'''
used to print a list of font families available on the system.
rom tkinter import Tk, font
root = Tk()
print(font.families())
'''
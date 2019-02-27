__author__ = "Rick Myers"

import tkinter as tk
from tkinter import PhotoImage
from GiftCard import GiftCard
from AddCardDialog import AddCardDialog


class GiftCardLedger(tk.Tk):
    # todo adjust frame colors after layout is complete
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
        # todo load cards from sql db
        self.card_list_maker()
        for row_index, card in enumerate(self.cards_list):
            card.bind("<Button-1>", self.remove_card)
            card.grid(row=row_index, sticky='news')
            print(card.name)

        # Create canvas window to hold the cards_list_frame.
        self.card_list_canvas.create_window((0, 0), window=self.cards_list_frame, anchor=tk.NW)

        # Redraws widgets within frame and creates bounding box access.
        self.cards_list_frame.update_idletasks()
        # Get bounding box of canvas with the cards list.
        cards_list_bbox = self.card_list_canvas.bbox(tk.ALL)
        #print('canvas.cards_list_bbox(tk.ALL): {}'.format(cards_list_bbox))

        # Set the scrollable region to the height of the cards list canvas bounding box
        # Reconfigure the card list canvas to be the same size as the bounding box
        # todo set without using hard numbers, height is currently manually set
        w, _ = cards_list_bbox[2], cards_list_bbox[3]
        self.card_list_canvas.configure(scrollregion=cards_list_bbox, width=w, height=120)

        # Button for adding a new card and the frame it is in.
        buttons_frame = tk.Frame(main_frame, bg="Blue", bd=2, relief=tk.GROOVE)
        buttons_frame.grid(row=5, column=0, sticky=tk.SE)
        add_card_button = tk.Button(buttons_frame, text="Add Card", command=self.add_card_dialogue)
        add_card_button.grid(row=0, column=0, padx=2, pady=10)

        #root window binds
        self.bind("<Configure>", self.canvas_configure)

    def remove_card(self, event):
        pass

    def add_card(self, event):
        pass
        
    def canvas_configure(self, event=None):
        self.card_list_canvas.configure(scrollregion=self.card_list_canvas.bbox(tk.ALL))

    def add_card_dialogue(self):
        dialog = AddCardDialog(self)
        self.wait_window(dialog)
        print(dialog.result)
        test_card4 = GiftCard(self.cards_list_frame, dialog.result[0], dialog.result[1], "lightgrey", "black", 10, anchor='w')
        test_card4.grid(row=5, column=0, sticky='news')
        self.cards_list.append(test_card4)

    def card_list_maker(self):
        test_card = GiftCard(self.cards_list_frame, "Subway", 23.74, "lightgrey", "black", 5, anchor='w')
        # todo balance not being printed in second column
        #test_card.bind("<Button-1>", self.remove_card)
        #test_label = tk.Label(self.cards_list_frame, text=test_card.get_balance(), anchor='e')
        #test_label.grid(row=0, column=1, sticky='nws')
        test_card2 = GiftCard(self.cards_list_frame, "Test Card", 23.74, "lightgrey", "black", 5, anchor='w')
        test_card3 = GiftCard(self.cards_list_frame, "Test Card", 23.74, "lightgrey", "black", 10, anchor='w')
        test_card4 = GiftCard(self.cards_list_frame, "Test Card", 23.74, "lightgrey", "black", 10, anchor='w')
        self.cards_list.append(test_card)
        self.cards_list.append(test_card2)
        self.cards_list.append(test_card3)
        self.cards_list.append(test_card4)

if __name__ == "__main__":
    gift_card_ledger = GiftCardLedger()
    gift_card_ledger.mainloop()

'''
used to print a list of font families available on the system.
rom tkinter import Tk, font
root = Tk()
print(font.families())
'''
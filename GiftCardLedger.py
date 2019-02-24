import tkinter as tk
from tkinter import PhotoImage
from GiftCard import GiftCard


class GiftCardLedger(tk.Tk):
    def __init__(self, cards=None):
        super().__init__()

        if not cards:
            self.cards = []
        else:
            self.cards = cards

        # Screen label that appears at the top. It displays what screen is currently active.
        self.top_label_var = tk.StringVar(self)
        self.top_label = tk.Label(self, textvar=self.top_label_var, fg="black", bg="white", font=('Terminal', 28))
        self.top_label.pack(side=tk.TOP, fill=tk.X)
        # todo set the label when the screen is selected?
        self.top_label_var.set("Gift Card Ledger")

        # Create a canvas
        self.cards_canvas = tk.Canvas(self)
        # Create a frame to hold the list of cards
        self.cards_list_frame = tk.Frame(self.cards_canvas)
        # The scrollbar will be used when the card list it too long to view on screen.
        self.scrollbar = tk.Scrollbar(self.cards_canvas, orient="vertical", command=self.cards_canvas.yview)
        self.cards_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.title("Gift Card Ledger")
        self.geometry("350x500")
        # The card canvas is packed to the top of the root window along with the scrollbar
        self.cards_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Draw a window within the canvas, this is where the card list frame will display
        self.canvas_frame = self.cards_canvas.create_window((0, 0), window=self.cards_list_frame, anchor="n")

        # Temporary value to add to the list of cards
        test_card = GiftCard(self.cards_list_frame, "Test Card", 23.74,
                             "lightgrey", "black", 10)
        self.cards.append(test_card)

        for card in self.cards:
            card.pack(side=tk.TOP, fill=tk.X)

        # set bounding box to be consisted with card frame within card canvas...more binds to comes
        self.bind("<Configure>", self.on_frame_configure)
        self.cards_canvas.bind("<Configure>", self.card_width)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.bind_all("<Button-4>", self.mouse_scroll)
        self.bind_all("<Button-5>", self.mouse_scroll)

        # button used to add cards to card list. will launch another window to prompt for data
        self.button_photo = PhotoImage(file="assets/add_symbol.png")
        self.add_card_button = tk.Button(self, image=self.button_photo, width=100, height=100,
                                         font='Terminal')
        self.add_card_button.pack()

        # alternating color scheme to allow labels to be more visible
        self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

    def on_frame_configure(self, event=None):
        '''Reconfigure the canvas scroll region when the window is configured
        or a new card is added to the card frame.'''
        self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all"))

    def card_width(self, event):
        '''Reconfigure the width of the canvas when the window is modified.'''
        canvas_width = event.width
        self.cards_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def add_card(self, name, balance, event=None, from_db=False):
        '''Add a new GiftCard to the card list.'''
        pass
        # todo finish add card
        #card = GiftCard(self.cards_list_frame, name, balance, bg, fg, pady)

    def mouse_scroll(self, event):
        '''Scrolls the card canvas'''
        if event.delta:
            self.cards_canvas.yview_scroll(-1*(event.delta/120), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            self.cards_canvas.yview_scroll(move, "units")


if __name__ == "__main__":
    gift_card_ledger = GiftCardLedger()
gift_card_ledger.mainloop()

'''
used to print a list of font families available on the system.
rom tkinter import Tk, font
root = Tk()
print(font.families())
'''
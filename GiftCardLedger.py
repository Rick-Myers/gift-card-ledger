import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msg


class GiftCardLedger(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gift Card Ledger")
        self.geometry("350x500")

        # Screen label that appears at the top. It displays what screen is currently active.
        self.top_label_var = tk.StringVar(self)
        self.top_label = tk.Label(self, textvar=self.top_label_var, fg="black", bg="white", font=('Terminal', 28))
        self.top_label.pack(side=tk.TOP, fill=tk.X)
        # todo set the label when the screen is selected?
        self.top_label_var.set("Gift Card Ledger")

        # todo add a frame for the listbox, listbox should allow access to card editing screen

        # todo add a frame for a button to add a gift card


if __name__ == "__main__":
    gift_card_tracker = GiftCardLedger()
gift_card_tracker.mainloop()

'''
used to print a list of font families available on the system.
rom tkinter import Tk, font
root = Tk()
print(font.families())
'''
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msg


class GiftCardLedger(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gift Card Ledger")
        self.geometry("400x600")


if __name__ == "__main__":
    gift_card_tracker = GiftCardLedger()
gift_card_tracker.mainloop()

import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
import tkinter.messagebox as msg


class GiftCardLedger(tk.Tk):
    def __init__(self):
        super().__init__()

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
        todo1 = tk.Label(self.cards_list_frame, text="Card A       $23.74", bg="lightgrey",
                         fg="black", pady=10)
        todo1.pack(side=tk.TOP, fill=tk.X)

        # set bounding box to be consisted with card frame within card canvas...more binds to comes
        self.bind("<Configure>", self.on_frame_configure)
        self.cards_canvas.bind("<Configure>", self.task_width)

        # button used to add cards to card list. will launch another window to prompt for data
        self.button_photo = PhotoImage(file="assets/add_symbol.png")
        self.add_card_button = tk.Button(self, image=self.button_photo, width=100, height=100,
                                         font='Terminal')
        self.add_card_button.pack()

        # alternating color scheme to allow labels to be more visible
        self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

    def on_frame_configure(self, event=None):
        self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all"))

    def task_width(self, event):
        canvas_width = event.width
        self.cards_canvas.itemconfig(self.canvas_frame, width=canvas_width)

if __name__ == "__main__":
    gift_card_ledger = GiftCardLedger()
gift_card_ledger.mainloop()

'''
used to print a list of font families available on the system.
rom tkinter import Tk, font
root = Tk()
print(font.families())
'''
__author__ = "Rick Myers"

import tkinter as tk
import tkinter.scrolledtext as tkscrolled

class EditCardDialog(tk.Toplevel):
    def __init__(self, parent, card, title=None):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        self.card = card
        self.result = None

        main_frame = tk.Frame(self)
        self.initial_focus = self.body(main_frame)
        main_frame.grid(sticky=tk.NSEW)
        main_frame.columnconfigure(0, weight=1)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))

        self.initial_focus.focus_set()

        #
        # construction hooks

    def body(self, master):
        # Top frame for label and card name
        label_frame = tk.Frame(self)
        label_frame.grid(sticky=tk.NSEW)

        top_label_var = tk.StringVar(master)
        top_label = tk.Label(label_frame, textvar=top_label_var, fg="black", bg="white", font=('Terminal', 20))
        top_label.grid(row=0, column=0, pady=5, sticky=tk.NSEW)
        top_label_var.set("Gift Card Ledger")

        card_label_var = tk.StringVar(master)
        card_label = tk.Label(label_frame, textvar=card_label_var, fg="black", bg="white", font=('Terminal', 20))
        card_label.grid(row=1, column=0, pady=5, sticky=tk.N)
        card_label_var.set(self.card.name)

        # Middle frame for balance information
        balance_frame = tk.Frame(self)
        balance_frame.grid(sticky=tk.NSEW)

        tk.Label(balance_frame, text="Current Balance: ", anchor=tk.W).grid(row=2, sticky=tk.NW)
        self.balance_entry = tk.Entry(balance_frame).grid(row=2, column=2, sticky=tk.NE)
        tk.Label(balance_frame, text="Starting Balance: ", anchor=tk.W).grid(row=3, sticky=tk.NW)
        tk.Label(balance_frame, text=self.card.get_balance(self.card.balance),
                 anchor=tk.W).grid(row=2, column=1, sticky=tk.NSEW)
        tk.Label(balance_frame, text=self.card.get_balance(self.card.starting_balance),
                 anchor=tk.W).grid(row=3, column=1, sticky=tk.NSEW)

        # Bottom frame to hold card history
        history_frame = tk.Frame(self)
        history_frame.grid(sticky=tk.NSEW)

        m = "11/11/1982 23.20\ndate 20.10\ndate 15.05\ndate 23.20\ndate 20.10\ndate 15.05\ndate 23.20\ndate 20.10\ndate 15.05\ndate 23.20\ndate 20.10\ndate 15.05"
        history_txt = tkscrolled.ScrolledText(history_frame, width=20, height=10)
        history_txt.insert(1.0, m)
        history_txt.config(state=tk.DISABLED)
        history_txt.grid(sticky=tk.NSEW)

        return self.balance_entry

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.grid(padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.grid(row=0, column=1, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.grid()

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        return 1  # override

    def apply(self):
        pass

__author__ = "Rick Myers"

import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import sqlite3
from datetime import date

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


        # Top frame for label and card name
        label_frame = tk.Frame(self)
        label_frame.grid(sticky=tk.NSEW)

        top_label_var = tk.StringVar(main_frame)
        top_label = tk.Label(label_frame, textvar=top_label_var, fg="black", bg="white", font=('Terminal', 20))
        top_label.grid(row=0, column=0, pady=5, sticky=tk.NSEW)
        top_label_var.set("Gift Card Ledger")

        card_label_var = tk.StringVar(main_frame)
        card_label = tk.Label(label_frame, textvar=card_label_var, fg="black", bg="white", font=('Terminal', 20))
        card_label.grid(row=1, column=0, pady=5, sticky=tk.N)
        card_label_var.set(self.card.name)

        # Middle frame for balance information
        balance_frame = tk.Frame(self)
        balance_frame.grid(sticky=tk.NSEW)

        tk.Label(balance_frame, text="Current Balance: ", anchor=tk.W).grid(sticky=tk.NW)
        self.balance_entry = tk.Entry(balance_frame)
        self.balance_entry.bind("<Return>", self._update_balance)
        self.balance_entry.grid(row=0, column=2, sticky=tk.NE)
        tk.Label(balance_frame, text="Starting Balance: ", anchor=tk.W).grid(row=1, sticky=tk.NW)
        self.balance_label = tk.Label(balance_frame, text=self.card.get_balance(self.card.balance),
                                      anchor=tk.W)
        self.balance_label.grid(row=0, column=1, sticky=tk.N)
        tk.Label(balance_frame, text=self.card.get_balance(self.card.starting_balance),
                 anchor=tk.W).grid(row=1, column=1, sticky=tk.N)

        # Bottom frame to hold card history
        history_frame = tk.Frame(self)
        history_frame.grid(sticky=tk.NSEW)

        m = "11/11/1982 23.20\ndate 20.10\ndate 15.05\ndate 23.20\ndate 20.10\ndate 15.05\ndate 23.20\ndate 20.10\ndate 15.05\ndate 23.20\ndate 20.10\ndate 15.05"
        history_txt = tkscrolled.ScrolledText(history_frame, width=20, height=10)
        history_txt.insert(1.0, m)
        history_txt.config(state=tk.DISABLED)

        history_txt.grid(sticky=tk.NSEW)

        # Main frame setup
        main_frame.grid(sticky=tk.NSEW)
        main_frame.columnconfigure(0, weight=1)

        self.buttonbox()

        self.grab_set()
        self.initial_focus = self.balance_entry
        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))

        self.initial_focus.focus_set()

        self.result = None

        #
        # construction hooks

    def body(self, master):
        return self.balance_entry

    # todo currently the method will perform the subtraction but the printed result isn't pretty.
    # todo also these changes are not
    def _update_balance(self, event=None):
        self.card.balance -= float(self.balance_entry.get())
        self.balance_label.configure(text=str(self.card.balance))
        print(self.card.balance)
        self.balance_entry.delete(0, tk.END)

        # this works and will update the card. use it to insert real data
        sql_update_balance = "UPDATE gift_cards SET balance = ? WHERE name = ?"
        data = (50.00, "Delete Me")
        self.run_query(sql_update_balance, data)




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

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.grid(padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.grid(row=0, column=1, padx=5, pady=5)

        #self.bind("<Return>", self.ok)
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
        self.result = self.card.get_balance(self.card.balance)
        return self.result
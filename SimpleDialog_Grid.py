__author__ = "Rick Myers"

import tkinter as tk


class SimpleDialog_Grid(tk.Toplevel):
    """This formatted version of tkSimpleDialog, but it uses
    Grid Manager instead of Pack."""
    def __init__(self, parent, title = None):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        self.result = None

        main_frame = tk.Frame(self, bg="Light Blue")
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
        self.resizable(False, False)

        #
        # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        box = tk.Frame(self, bg="Light Blue")

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.grid(padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.grid(row=0, column=1, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.grid(row=2, column=0)

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

        pass  # override
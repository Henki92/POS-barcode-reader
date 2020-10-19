try:
    import tkinter as tk  # python 3
    from tkinter import messagebox
except ModuleNotFoundError:
    pass


# Centers all pop ups to center of screen
def center(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class AddRepair:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win_frame = tk.Frame(self.win)
        self.win.wm_title("Lägg till reperation/service")
        self.win.minsize(500, 300)
        tk.Label(self.win_frame, text="Arbetskostnad service (inkl moms):", font="Helvetica 14").grid(column=0, row=0, sticky="E")
        self.repair_cost = tk.Entry(self.win_frame, font="Helvetica 14")
        self.repair_cost.grid(column=1, row=0, sticky="WE", padx=10)
        self.repair_cost.focus()
        self.add_btn = tk.Button(self.win_frame, text="Lägg Till", font="Helvetica 14")
        self.add_btn.grid(column=2, row=0, sticky="WE")
        self.win_frame.pack(padx=10, pady=30)
        center(self.win)


class AddRandomArticle:
    def __init__(self):
        self.win = tk.Toplevel()
        win_frame = tk.Frame(self.win)
        self.win.wm_title("Lägg till fri artikel")
        self.win.minsize(900, 300)
        tk.Label(win_frame, text="Beskrivning", font="Helvetica 14").grid(column=0, row=0, sticky="N")
        self.description_entry = tk.Entry(win_frame, font="Helvetica 14")
        self.description_entry.grid(column=0, row=1, sticky="WE", padx=10)
        self.description_entry.focus()
        tk.Label(win_frame, text="Exkl. moms", font="Helvetica 14").grid(column=1, row=0, sticky="N")
        self.price_entry = tk.Entry(win_frame, font="Helvetica 14")
        self.price_entry.grid(column=1, row=1, sticky="WE", padx=10)
        tk.Label(win_frame, text="Inkl. moms", font="Helvetica 14").grid(column=2, row=0, sticky="N")
        self.price_entry_vat = tk.Entry(win_frame, font="Helvetica 14")
        self.price_entry_vat.grid(column=2, row=1, sticky="WE", padx=10)
        self.add_btn = tk.Button(win_frame, text="Lägg Till", font="Helvetica 14")
        self.add_btn.grid(column=3, row=1, sticky="WE")
        center(self.win)
        win_frame.pack(padx=10, pady=30)


class PrintRecipt:
    def __init__(self):
        self.win = tk.Toplevel()
        win_frame = tk.Frame(self.win)
        self.win.wm_title("Skriv ut")
        self.win.minsize(500, 300)
        tk.Label(win_frame, text="Namn:", font="Helvetica 14").grid(column=0, row=0, sticky="N")
        self.name_entry = tk.Entry(win_frame, font="Helvetica 14")
        self.name_entry.grid(column=1, row=0, sticky="WE", padx=10)
        self.name_entry.focus()
        tk.Label(win_frame, text="Telefon:", font="Helvetica 14").grid(column=0, row=1, sticky="N")
        self.phone_entry = tk.Entry(win_frame, font="Helvetica 14")
        self.phone_entry.grid(column=1, row=1, sticky="WE", padx=10)
        self.add_btn = tk.Button(win_frame, text="Skriv ut", font="Helvetica 14")
        self.add_btn.grid(column=1, row=2, sticky="WE")
        win_frame.pack(padx=10, pady=30)
        self.add_btn.configure(command=dummyViewPippa)
        center(self.win)


class AddArticleToDB:
    def __init__(self):
        self.win = tk.Toplevel()
        win_frame = tk.Frame(self.win)
        self.win.wm_title("Lägg till artikel i databas")
        self.win.minsize(500, 300)
        tk.Label(win_frame, text="Streckkod", font="Helvetica 14").grid(column=0, row=0, sticky="N")
        self.EAN = tk.Entry(win_frame, font="Helvetica 14")
        self.EAN.grid(column=0, row=1, sticky="WE", padx=10)
        self.EAN.focus()
        tk.Label(win_frame, text="ArtNr", font="Helvetica 14").grid(column=1, row=0, sticky="N")
        self.artnr = tk.Entry(win_frame, font="Helvetica 14")
        self.artnr.grid(column=1, row=1, sticky="WE", padx=10)
        tk.Label(win_frame, text="Beskrivning", font="Helvetica 14").grid(column=2, row=0, sticky="N")
        self.description = tk.Entry(win_frame, font="Helvetica 14")
        self.description.grid(column=2, row=1, sticky="WE", padx=10)
        tk.Label(win_frame, text="Kostnad inkl. moms", font="Helvetica 14").grid(column=3, row=0, sticky="N")
        self.price = tk.Entry(win_frame, font="Helvetica 14")
        self.price.grid(column=3, row=1, sticky="WE", padx=10)
        self.add_btn = tk.Button(win_frame, text="Lägg Till", font="Helvetica 14")
        self.add_btn.grid(column=4, row=1, sticky="WE")
        win_frame.pack(padx=10, pady=30)
        center(self.win)


class ErrorShow:
    def __init__(self, string):
        messagebox.showwarning("NU HÄNDE NÅGOT?", string)

try:
    import tkinter as tk # python 3
except ModuleNotFoundError:
    pass


class Col:
    ArtNr = 0
    Beskrivning = 1
    Pris = 2
    EAN = 3
    Antal = 4


class GUISearchArea:
    def __init__(self, root):
        frame = tk.Frame(root, width=430, height=80)
        frame.grid_propagate(0)
        frame.grid(row=0, column=0, sticky="N")
        search_label = tk.Label(frame, text="ArtNr / Streckkod(EAN):")
        search_label.grid(column=0, row=0, pady=40)
        self.search_entry = tk.Entry(frame, width=20, font="Helvetica 14")
        self.search_entry.grid(column=1, row=0, pady=40, padx=3)
        self.search_entry.focus_set()
        self.search_button = tk.Button(frame, text="Sök", width=8)
        self.search_button.grid(column=2, row=0, pady=40)


class GUIMenuArea:
    def __init__(self, root):
        frame = tk.Frame(root, width=350, height=600)
        frame.grid_propagate(0)
        frame.grid(row=1, column=0, sticky="NESW")
        self.btn_repair = tk.Button(frame, text="Lägg till service/reperation", width=50, height=2, padx=5, pady=5)
        self.btn_repair.pack(side="top", expand="yes", padx=10, pady=10)
        self.btn_repair.configure(borderwidth=2, relief="raised", bg="snow3")
        self.btn_add_random_article = tk.Button(frame, text="Lägg till fri artikel", width=50, height=2, padx=5, pady=5)
        self.btn_add_random_article.pack(side="top", expand="yes", padx=10, pady=10)
        self.btn_add_random_article.configure(borderwidth=2, relief="raised", bg="snow3")
        self.btn_print = tk.Button(frame, text="Skriv ut kvitto", width=50, height=2, padx=5, pady=5)
        self.btn_print.pack(side="top", expand="yes", padx=10, pady=10)
        self.btn_print.configure(borderwidth=2, relief="raised", bg="snow3")
        self.btn_clear_all = tk.Button(frame, text="Rensa rutan med artiklar", width=50, height=2, padx=5, pady=5)
        self.btn_clear_all.pack(side="top", expand="yes", padx=10, pady=10)
        self.btn_clear_all.configure(borderwidth=2, relief="raised", bg="snow3")
        self.btn_add_to_db = tk.Button(frame, text="Lägg till artikel i databas", width=50, height=2, padx=5, pady=5)
        self.btn_add_to_db.pack(side="top", expand="yes", padx=10, pady=10)
        self.btn_add_to_db.configure(borderwidth=2, relief="raised", bg="snow3")


class GUIArticleArea:
    def __init__(self, root):
        frame = tk.Frame(root, width=480, borderwidth=2, relief="groove")
        frame.grid_propagate(0)
        frame.grid(row=0, column=1, rowspan=2, sticky="NESW")
        small_overhead_frame = tk.Frame(frame, bg="gray", width=400)
        small_overhead_frame.grid(row=0, column=0)
        tk.Label(small_overhead_frame, bg="gray", text="Artikelnummer", width=13).grid(column=0, row=1, padx=5)
        tk.Label(small_overhead_frame, bg="gray", text="Beskrivning", width=28).grid(column=1, row=1, padx=5)
        tk.Label(small_overhead_frame, bg="gray", text="Pris exkl.", width=8).grid(column=2, row=0, padx=5)
        tk.Label(small_overhead_frame, bg="gray", text="moms", width=8).grid(column=2, row=1, padx=5)
        tk.Label(small_overhead_frame, bg="gray", text="Pris inkl.", width=8).grid(column=3, row=0, padx=5)
        tk.Label(small_overhead_frame, bg="gray", text="moms", width=8).grid(column=3, row=1, padx=5)
        tk.Label(small_overhead_frame, bg="gray", text="Antal", width=5).grid(column=4, row=1, padx=5)
        tk.Label(small_overhead_frame, bg="gray", text="", width=12).grid(column=5, row=0)
        self.article_frame = tk.Frame(frame)
        self.article_frame.grid(row=1, column=0)


class GUITotalPrice:
    def __init__(self, root):
        frame = tk.Frame(root, width=480, height=150)
        frame.grid_propagate(0)
        frame.grid(row=3, column=1, sticky="NESW")
        tk.Label(frame, text="Total pris exkl. moms:",
                 font="Helvetica 12 bold").grid(column=0, row=0, sticky="NEWS", padx=2, pady=10)
        tk.Label(frame, text="Total pris inkl. moms:",
                 font="Helvetica 24 bold").grid(column=0, row=1, sticky="NEWS", padx=2, pady=10)
        self.excl_vat = tk.Label(frame, text="0", width=5, font="Helvetica 12 bold")
        self.excl_vat.grid(column=1, row=0, sticky="NEWS", padx=2, pady=10)
        self.incl_vat = tk.Label(frame, text="0", font="Helvetica 24 bold")
        self.incl_vat.grid(column=1, row=1, sticky="NEWS", padx=2, pady=10)
        tk.Label(frame, text="Kr",
                 font="Helvetica 12 bold").grid(column=2, row=0, sticky="NEWS", padx=2, pady=10)
        tk.Label(frame, text="Kr",
                 font="Helvetica 24 bold").grid(column=2, row=1, sticky="NEWS", padx=2, pady=10)

    def update_total(self, total_price):
        self.excl_vat.config(text=total_price)
        self.incl_vat.config(text=(round(total_price * 1.25, 2)))


class GUIitems:
    def __init__(self, frame, basket):
        self.button_list = []
        self.temp_frame_list = []
        for rows, item in enumerate(basket):
            temp_frame = tk.Frame(frame,  borderwidth=2, relief="groove", width=400)
            temp_frame.grid(row=rows, column=2)
            tk.Label(temp_frame, text=item[Col.ArtNr], width=13).grid(row=0, column=0, padx=5)
            tk.Label(temp_frame, text=item[Col.Beskrivning], width=28).grid(row=0, column=1, padx=5)
            tk.Label(temp_frame, text=item[Col.Pris], width=8).grid(row=0, column=2, padx=5)
            tk.Label(temp_frame, text=round(float(item[Col.Pris])*1.25, 2), width=8).grid(row=0, column=3, padx=5)
            tk.Label(temp_frame, text=item[Col.Antal], font="Helvetica 12 bold").grid(row=0, column=4,  padx=5)
            remove_button = tk.Button(temp_frame, text="Ta bort artikel")
            remove_button.grid(row=0, column=5, padx=5)
            self.button_list.append(remove_button)
            self.temp_frame_list.append(temp_frame)



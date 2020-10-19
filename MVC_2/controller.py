from model import Model
from viewmain import *
from viewpopup import *
from functools import partial

from MVC_2.viewmain import GUIMenuArea, GUISearchArea, GUIArticleArea, GUITotalPrice, GUIitems
from MVC_2.viewpopup import ErrorShow, AddRepair, AddRandomArticle, PrintRecipt, AddArticleToDB
from MVC_2.print import print_function

from threading import Timer
try:
    import tkinter as tk
except ModuleNotFoundError:
    pass


class Cols:
    ArtNr = 0
    Beskrivning = 1
    Pris = 2
    EAN = 3
    Antal = 4


def center(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class Controller:
    def __init__(self):
        print("Creating controller object")
        self.timer = None
        self.article_frame_list = []
        self.model = Model()
        self.root = tk.Tk()
        self.root.minsize(1200, 600)
        center(self.root)
        self.popup = None
        self.GUIsearch = GUISearchArea(self.root)
        self.GUIsearch.search_button.configure(command=self.search_article_btn_psd)
        self.GUImenu = GUIMenuArea(self.root)
        self.GUImenu.btn_repair.configure(command=self.add_repair_btn_psd)
        self.GUImenu.btn_add_random_article.configure(command=self.add_random_article_btn_psd)
        self.GUImenu.btn_print.configure(command=self.print_btn_psd)
        self.GUImenu.btn_clear_all.configure(command=self.clear_all_btn_psd)
        self.GUImenu.btn_add_to_db.configure(command=self.add_article_to_DB_btn_psd)
        self.GUIarticle = GUIArticleArea(self.root)
        self.GUIprice = GUITotalPrice(self.root)
        self.GUIitemslist = GUIitems(self.GUIarticle.article_frame, self.model.basket)
        self.root.bind_all('<Any-KeyPress>', self.reset_timer)
        self.root.bind_all('<Any-ButtonPress>', self.reset_timer)
        self.root.bind('<Return>', self.search_article_btn_psd)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def run(self):
        self.GUIsearch.search_entry.focus()
        self.root.title("Streckkodsläsare")
        self.root.mainloop()

    def reset_timer(self, Event = None):
        if self.timer is not None:
            self.timer.cancel()
        self.timer = Timer(240.0, dummy_d)
        self.timer.start()

    def search_article_btn_psd(self, Event = None):   # Need Event=None for when using Return
        EAN = self.GUIsearch.search_entry.get()     # Get barcode
        self.GUIsearch.search_entry.delete(0, 50)   # Remove the barcode read
        if not len(EAN):
            return
        print("Searching article: ", EAN)
        article = self.model.get_article_from_db(EAN)
        if article is None:
            ErrorShow("Artikel " + str(EAN) + " hittades ej")
            return
        print("Found article:", article)
        self.model.add_article_and_update_price(article)
        self.update_view()

    def update_view(self):
        self.GUIprice.update_total(self.model.total_price)
        self.GUIarticle = GUIArticleArea(self.root)
        self.GUIitemslist = GUIitems(self.GUIarticle.article_frame, self.model.basket)
        for row, button in enumerate(self.GUIitemslist.button_list):
            button.configure(command=partial(self.remove_article_btn_psd, row))

    def remove_article_btn_psd(self, row):
        self.model.remove_article(row)
        self.update_view()

    def add_repair_btn_psd(self):
        self.popup = AddRepair()
        self.popup.add_btn.configure(command=self.add_repair)

    def add_repair(self):
        cost = self.popup.repair_cost.get()
        cost = round(float(cost) / 1.25, 2)
        self.popup.win.destroy()
        self.popup.win.update()
        self.model.add_anything_func("Reperation/Service", cost)
        self.update_view()

    def add_random_article_btn_psd(self):
        self.popup = AddRandomArticle()
        self.popup.add_btn.configure(command=self.add_random_article)

    def add_random_article(self):
        description = self.popup.description_entry.get()
        cost = 0
        if len(self.popup.price_entry.get()):
            cost = self.popup.price_entry.get()
        if len(self.popup.price_entry_vat.get()):
            cost = round(float(self.popup.price_entry_vat.get()) / 1.25, 2)
        self.popup.win.destroy()
        self.popup.win.update()
        self.model.add_anything_func(description, cost)
        self.update_view()

    def print_btn_psd(self):
        self.popup = PrintRecipt()
        self.popup.add_btn.configure(command=self.print_fun)

    def print_fun(self):
        name = self.popup.name_entry.get() if len(self.popup.name_entry.get()) else "Kund"
        phone = self.popup.phone_entry.get() if len(self.popup.phone_entry.get()) else "Telefon Nr"
        print_function(self.model, name, phone)
        self.popup.win.destroy()
        self.popup.win.update()

    def clear_all_btn_psd(self):
        self.model = Model()
        self.update_view()

    def add_article_to_DB_btn_psd(self):
        self.popup = AddArticleToDB()
        self.popup.add_btn.configure(command=self.add_article_to_DB)

    def add_article_to_DB(self):
        EAN = self.popup.EAN.get() if len(self.popup.EAN.get()) else None
        artnr = self.popup.artnr.get() if len(self.popup.artnr.get()) else " "
        description = self.popup.description.get() if len(self.popup.description.get()) else None
        price = self.popup.price.get() if len(self.popup.price.get()) else None
        if EAN is None or description is None or price is None:
            ErrorShow("Du måste ange streckkod/beskrivning och pris")
            self.popup.win.destroy()
            self.popup.win.update()
            return
        result = self.model.add_article_to_DB([artnr, description, round(float(price) / 1.25, 2), EAN])
        if result is 'Added':
            ErrorShow("Artikel tillagd")
        elif result is 'Existent':
            ErrorShow("Streckkoden finns redan i databasen! ", )
        self.popup.win.destroy()
        self.popup.win.update()



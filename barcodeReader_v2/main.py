# Use Tkinter for python 2, tkinter for python 3
import tkinter as tk
import csv
import os
from functools import partial
from tkinter.messagebox import showinfo
from threading import Timer
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib.units import cm
import time
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import psutil


class GUISearchArea:
    def __init__(self, parent):
        parent.bind('<Return>', self.search_article)
        self.frame = tk.Frame(parent, width=430, height=80)
        self.frame.grid_propagate(0)
        self.search_label = tk.Label(self.frame, text="ArtNr / Streckkod(EAN):")
        self.search_label.grid(column=0, row=0, pady=40)
        self.search_entry = tk.Entry(self.frame, width=20, font="Helvetica 14")
        self.search_entry.grid(column=1, row=0, pady=40, padx=3)
        self.search_entry.focus_set()
        self.search_button = tk.Button(self.frame, text="Sök", width=8)
        self.search_button.bind('<Button-1>', self.search_article)
        self.search_button.grid(column=2, row=0, pady=40)

    def search_article(self, Event):
        self.search_entry.focus()
        barcodelist = []
        if len(self.search_entry.get()) > 0:
            if 'paket' in self.search_entry.get():
                with open('databaspaket.csv', 'r', newline='', encoding='UTF8') as f:
                    reader = csv.reader(f, delimiter=";")
                    for row in reader:
                        if row[0] == self.search_entry.get():
                            for row in reader:
                                if row[0] == self.search_entry.get():
                                    break
                                barcodelist.append(row[0])
            else:
                barcodelist.append(self.search_entry.get())
            for barcode in barcodelist:
                article_info = []
                # Find the article in the database
                with open('databas.csv', 'r', newline='', encoding='UTF8') as f:
                    reader = csv.reader(f, delimiter=";")
                    listbase = list(reader)
                    for i, row in enumerate(listbase):
                        if not row == []:
                            if barcode == row[6] or barcode == row[0]:
                                article_info.append(row[0])
                                article_info.append(row[1])
                                article_info.append(float(row[4])*1.25)
                                break
                if not article_info == []:
                    article_frame.add_article_to_gui(article_info)
                    cost_frame.gui_update_total_cost()
                    self.search_entry.delete(0, 30)


class GUIMenuArea:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, width=350, height=600)
        self.frame.grid_propagate(0)
        self.button_service = tk.Button(self.frame, text="Lägg till service/reperation", width=50, height=2, padx=5, pady=5)#.grid(column=0, row=0, sticky="WE", padx=30, pady=10)
        self.button_service.pack(side="top", expand="yes", padx=10, pady=10)
        self.button_service.configure(command=self.service_window, borderwidth=2, relief="raised", bg="snow3")
        self.button_free_text = tk.Button(self.frame, text="Lägg till fri artikel", width=50, height=2, padx=5, pady=5)#.grid(column=0, row=1, sticky="WE", padx=30, pady=10)
        self.button_free_text.pack(side="top", expand="yes", padx=10, pady=10)
        self.button_free_text.configure(command=self.free_article_window, borderwidth=2, relief="raised", bg="snow3")
        self.button_print_receipt = tk.Button(self.frame, text="Skriv ut kvitto", width=50, height=2, padx=5, pady=5)#.grid(column=0, row=2, sticky="WE", padx=30, pady=10)
        self.button_print_receipt.pack(side="top", expand="yes", padx=10, pady=10)
        self.button_print_receipt.configure(command=self.print_receipt, borderwidth=2, relief="raised", bg="snow3")
        self.button_clear_all = tk.Button(self.frame, text="Rensa rutan med artiklar", width=50, height=2, padx=5, pady=5)#.grid(column=0, row=3, sticky="WE", padx=30, pady=10)
        self.button_clear_all.pack(side="top", expand="yes", padx=10, pady=10)
        self.button_clear_all.configure(command=self.remove_all_articles, borderwidth=2, relief="raised", bg="snow3")
        self.button_add_to_database = tk.Button(self.frame, text="Lägg till artikel i databas", width=50, height=2, padx=5, pady=5)#.grid(column=0, row=4, sticky="WE", padx=30, pady=10)
        self.button_add_to_database.pack(side="top", expand="yes", padx=10, pady=10)
        self.button_add_to_database.configure(command=self.add_func, borderwidth=2, relief="raised", bg="snow3")

    def service_window(self):
        win = tk.Toplevel()
        win_frame = tk.Frame(win)
        win.wm_title("Lägg till reperation/service")
        win.minsize(500, 300)
        tk.Label(win_frame, text="Arbetskostnad service:", font="Helvetica 14").grid(column=0, row=0, sticky="E")
        reapir_cost = tk.Entry(win_frame, font="Helvetica 14")
        reapir_cost.grid(column=1, row=0, sticky="WE", padx=10)
        reapir_cost.focus()
        add_reapir_cost = tk.Button(win_frame, text="Lägg Till", font="Helvetica 14")
        add_reapir_cost.grid(column=2, row=0, sticky="WE")
        win_frame.pack(padx=10, pady=30)
        center(win)

        def add_service(window):
            if len(reapir_cost.get()):
                article_frame.add_article_to_gui(["", "Reparation/Felsökning/Provkörning", reapir_cost.get()])
                cost_frame.gui_update_total_cost()
                window.destroy()

        add_reapir_cost.configure(command=partial(add_service, win))

    def free_article_window(self):
        win = tk.Toplevel()
        win_frame = tk.Frame(win)
        win.wm_title("Lägg till fri artikel")
        win.minsize(500, 300)
        tk.Label(win_frame, text="Beskrivning", font="Helvetica 14").grid(column=0, row=0, sticky="N")
        description_entry = tk.Entry(win_frame, font="Helvetica 14")
        description_entry.grid(column=0, row=1, sticky="WE", padx=10)
        description_entry.focus()
        tk.Label(win_frame, text="Exkl. moms", font="Helvetica 14").grid(column=1, row=0, sticky="N")
        price_entry = tk.Entry(win_frame, font="Helvetica 14")
        price_entry.grid(column=1, row=1, sticky="WE", padx=10)
        tk.Label(win_frame, text="Inkl. moms", font="Helvetica 14").grid(column=2, row=0, sticky="N")
        price_entry_vat = tk.Entry(win_frame, font="Helvetica 14")
        price_entry_vat.grid(column=2, row=1, sticky="WE", padx=10)
        add_article_button = tk.Button(win_frame, text="Lägg Till", font="Helvetica 14")
        add_article_button.grid(column=3, row=1, sticky="WE")
        win_frame.pack(padx=10, pady=30)
        center(win)

        def add_free_article(window):
            if len(description_entry.get()) or len(price_entry.get()) or len(price_entry_vat.get()):
                if price_entry_vat.get():
                    article_frame.add_article_to_gui(["", description_entry.get(), price_entry_vat.get()])
                if price_entry.get():
                    article_frame.add_article_to_gui(["", description_entry.get(), float(price_entry.get())*1.25])
                cost_frame.gui_update_total_cost()
                window.destroy()

        add_article_button.configure(command=partial(add_free_article, win))

    def print_receipt(self):
        win = tk.Toplevel()
        win_frame = tk.Frame(win)
        win.wm_title("Lägg till fri artikel")
        win.minsize(500, 300)
        tk.Label(win_frame, text="Namn:", font="Helvetica 14").grid(column=0, row=0, sticky="N")
        name_entry = tk.Entry(win_frame, font="Helvetica 14")
        name_entry.grid(column=1, row=0, sticky="WE", padx=10)
        name_entry.focus()
        tk.Label(win_frame, text="Telefon:", font="Helvetica 14").grid(column=0, row=1, sticky="N")
        phone_entry = tk.Entry(win_frame, font="Helvetica 14")
        phone_entry.grid(column=1, row=1, sticky="WE", padx=10)
        add_article_button = tk.Button(win_frame, text="Skriv ut", font="Helvetica 14")
        add_article_button.grid(column=1, row=2, sticky="WE")
        win_frame.pack(padx=10, pady=30)
        center(win)

        def print_button(window):
            if len(name_entry.get()):
                basket.print_function(name_entry.get(), phone_entry.get())
                window.destroy()
            else:
                basket.print_function("", "")
                window.destroy()

        add_article_button.configure(command=partial(print_button, win))

    def remove_all_articles(self):
        article_frame.frame.destroy()
        article_frame.reset(root)
        article_frame.frame.grid(row=0, column=1, rowspan=2, sticky="NESW")
        basket.reset()
        cost_frame.gui_update_total_cost()

    def add_func(self):
        temp = DatabaseAdding(root)
        del temp


class DatabaseAdding:
    def __init__(self, parent):
        self.win = tk.Toplevel()
        self.win_frame = tk.Frame(self.win)
        self.win.wm_title("Lägg till artikel i databas")
        self.win.minsize(500, 300)
        tk.Label(self.win_frame, text="Streckkod", font="Helvetica 14").grid(column=0, row=0, sticky="N")
        self.barcode = tk.Entry(self.win_frame, font="Helvetica 14")
        self.barcode.grid(column=0, row=1, sticky="WE", padx=10)
        self.barcode.focus()
        tk.Label(self.win_frame, text="ArtNr", font="Helvetica 14").grid(column=1, row=0, sticky="N")
        self.artnr = tk.Entry(self.win_frame, font="Helvetica 14")
        self.artnr.grid(column=1, row=1, sticky="WE", padx=10)
        tk.Label(self.win_frame, text="Beskrivning", font="Helvetica 14").grid(column=2, row=0, sticky="N")
        self.description_entry = tk.Entry(self.win_frame, font="Helvetica 14")
        self.description_entry.grid(column=2, row=1, sticky="WE", padx=10)
        tk.Label(self.win_frame, text="Kostnad inkl. moms", font="Helvetica 14").grid(column=3, row=0, sticky="N")
        self.price_entry = tk.Entry(self.win_frame, font="Helvetica 14")
        self.price_entry.grid(column=3, row=1, sticky="WE", padx=10)
        self.add_article_button = tk.Button(self.win_frame, text="Lägg Till", font="Helvetica 14")
        self.add_article_button.grid(column=4, row=1, sticky="WE")
        self.win_frame.pack(padx=10, pady=30)
        self.add_article_button.configure(command=partial(self.add_free_article, self.win))
        center(self.win)

    def add_free_article(self, window):
        if len(self.barcode.get()) > 0:
            barcode = self.barcode.get()
            article_info = []
            # Find the article in the database
            with open('databas.csv', 'r', newline='', encoding='UTF8') as f:
                reader = csv.reader(f, delimiter=";")
                listBase = list(reader)
                for i, row in enumerate(listBase):
                    if not row == []:
                        if barcode == row[6] or barcode == row[0]:
                            showinfo("Window", "Streckoden finns redan i databasen!")
                            window.destroy()
                            return
            with open('databas.csv', 'a', newline='', encoding='UTF8') as f:
                writer = csv.writer(f, delimiter=";")
                fields = [self.artnr.get(), str(self.description_entry.get()),
                          "", "",
                          float(self.price_entry.get()) / 1.25, "", self.barcode.get(), ""]
                writer.writerow(fields)
                showinfo("Window", "Artikel tillagd!")

            window.destroy()


class GUIArticleArea:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, width=480, borderwidth=2, relief="groove")
        self.frame.grid_propagate(0)
        self.small_overhead_frame = tk.Frame(self.frame, bg="gray", width=400)
        self.small_overhead_frame.grid(row=0, column=0)
        tk.Label(self.small_overhead_frame, bg="gray", text="Artikelnummer", width=13).grid(column=0, row=1, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="Beskrivning", width=28).grid(column=1, row=1, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="Pris exkl.", width=8).grid(column=2, row=0, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="moms", width=8).grid(column=2, row=1, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="Pris inkl.", width=8).grid(column=3, row=0, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="moms", width=8).grid(column=3, row=1, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="Antal", width=5).grid(column=4, row=1, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="", width=12).grid(column=5, row=0)
        self.article_frame = tk.Frame(self.frame)
        self.article_frame.grid(row=1, column=0)
        self.article_rows = 0

    def reset(self, parent):
        self.frame = tk.Frame(parent, width=480, borderwidth=2, relief="groove")
        self.frame.grid_propagate(0)
        self.small_overhead_frame = tk.Frame(self.frame, bg="gray", width=400)
        self.small_overhead_frame.grid(row=0, column=0)
        tk.Label(self.small_overhead_frame, bg="gray", text="Artikelnummer", width=13).grid(column=0, row=1, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="Beskrivning", width=28).grid(column=1, row=1, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="Pris exkl.", width=8).grid(column=2, row=0, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="moms", width=8).grid(column=2, row=1, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="Pris inkl.", width=8).grid(column=3, row=0, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="moms", width=8).grid(column=3, row=1, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="Antal", width=5).grid(column=4, row=1, padx=5)
        tk.Label(self.small_overhead_frame, bg="gray", text="", width=12).grid(column=5, row=0)
        self.article_frame = tk.Frame(self.frame)
        self.article_frame.grid(row=1, column=0)
        self.article_rows = 0

    def add_article_to_gui(self, article_info):
        self.article_rows += 1
        temp_frame = tk.Frame(self.article_frame,  borderwidth=2, relief="groove", width=400)
        num_box = tk.Spinbox(temp_frame, from_=1, to=20, width=3, font="Helvetica 12")

        def spin_box():
            value = num_box.get()
            basket.update_number_of_items(value, temp_frame)
            cost_frame.gui_update_total_cost()

        tk.Label(temp_frame, text=article_info[0], width=13).grid(row=0, column=0, padx=5)
        tk.Label(temp_frame, text=article_info[1], width=28).grid(row=0, column=1, padx=5)
        tk.Label(temp_frame, text=str(float(article_info[2])/1.25), width=8).grid(row=0, column=2, padx=5)
        tk.Label(temp_frame, text=article_info[2], width=8).grid(row=0, column=3, padx=5)
        num_box.configure(command=spin_box)
        num_box.grid(row=0, column=4, padx=5)
        tk.Button(temp_frame, text="Ta bort artikel", command=partial(self.remove_article, temp_frame)).grid(row=0, column=5, padx=5)
        temp_frame.grid(row=self.article_rows + 1, column=2)
        basket.append_item(article_info, temp_frame)

    def remove_article(self, row_to_remove):
        basket.remove_item(row_to_remove)
        cost_frame.gui_update_total_cost()
        self.article_rows -= 1
        row_to_remove.destroy()


class GUICostArea:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, width=480, height=150)
        self.frame.grid_propagate(0)
        tk.Label(self.frame, text="Total pris exkl. moms:",
                 font="Helvetica 12 bold").grid(column=0, row=0, sticky="NEWS", padx=2, pady=10)
        tk.Label(self.frame, text="Total pris inkl. moms:",
                 font="Helvetica 24 bold").grid(column=0, row=1, sticky="NEWS", padx=2, pady=10)
        self.excl_vat = tk.Label(self.frame, text="0", width=5, font="Helvetica 12 bold")
        self.excl_vat.grid(column=1, row=0, sticky="NEWS", padx=2, pady=10)
        self.incl_vat = tk.Label(self.frame, text="0", font="Helvetica 24 bold")
        self.incl_vat.grid(column=1, row=1, sticky="NEWS", padx=2, pady=10)
        tk.Label(self.frame, text="Kr",
                 font="Helvetica 12 bold").grid(column=2, row=0, sticky="NEWS", padx=2, pady=10)
        tk.Label(self.frame, text="Kr",
                 font="Helvetica 24 bold").grid(column=2, row=1, sticky="NEWS", padx=2, pady=10)

    def gui_update_total_cost(self):
        ShoppingBasket.get_cost(basket)
        self.excl_vat.config(text=str(basket.get_cost()/1.25))
        self.incl_vat.config(text=str(basket.get_cost()))


class ShoppingBasket:
    def __init__(self):
        self.article_number = []
        self.description = []
        self.price = []
        self.number_of_items = []
        self.total_cost = 0
        self.frames = []

    def reset(self):
        self.article_number = []
        self.description = []
        self.price = []
        self.number_of_items = []
        self.total_cost = 0
        self.frames = []

    def append_item(self, article_found, temp_frame):
        self.article_number.append(article_found[0])
        self.description.append(article_found[1])
        self.price.append(article_found[2])
        self.number_of_items.append(1)
        self.frames.append(temp_frame)
        self.update_total()

    def update_number_of_items(self, number, item_frame):
        for i, find_frame in enumerate(self.frames):
            if item_frame == find_frame:
                self.number_of_items[i] = number
        self.update_total()

    def remove_item(self, item_frame):
        for i, find_frame in enumerate(self.frames):
            if item_frame == find_frame:
                self.frames.remove(item_frame)
                del self.article_number[i]
                del self.price[i]
                del self.description[i]
                del self.number_of_items[i]
        self.update_total()

    def update_total(self):
        self.total_cost = 0
        for price, num in zip(self.price, self.number_of_items):
            print("Kostnad:", price, "Antal:", num)

            self.total_cost += float(price)*int(num)

    def get_cost(self):
        return self.total_cost

    def print_function(self, name_customer, phone_customer):
        os.system("TASKKILL /F /IM AcroRD32.exe")
        for i, desc in enumerate(self.description):
            if desc == "Reparation/Felsökning/Provkörning":
                self.description.append(self.description.pop(i))
                self.article_number.append(self.article_number.pop(i))
                self.price.append(self.price.pop(i))
                self.number_of_items.append(self.number_of_items.pop(i))
        self.update_recipt(name_customer, phone_customer)
        os.startfile('Kvitto.pdf')

    def update_recipt(self, name_customer, phone_customer):
        widthA4, heightA4 = A4
        c = canvas.Canvas("Kvitto.pdf", pagesize=A4)

        # Rubrik kvitto
        c.setFont('Helvetica', 28)
        c.setLineWidth(.8)
        # c.drawString(widthA4 / 2 - 1 * cm, heightA4 * 9 / 10, 'Kvitto')
        c.drawString(2.8 * cm, heightA4 * 9.2 / 10, 'Mullhyttans Cykel & Såg Service AB')

        # Över text
        c.setLineWidth(.3)
        c.setFont('Helvetica', 12)
        c.drawString(widthA4 * 4.21 / 10, heightA4 * 8.8 / 10, 'Varuspecifikation')
        c.drawString(widthA4 / 2 - 3.5 * cm, heightA4 * 9 / 10, 'Tack för ditt köp och välkommen åter')

        # Artiklar osv
        data = [['Artikelnummer:', 'Beskrivning:', 'Antal:', 'Pris/st exkl.moms:', 'Pris/st inkl.moms:'],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', ''],
                ['', '', '', '', '']
                ]

        for i in range(0, len(self.article_number)):
            data[i + 1][0] = self.article_number[i]
            data[i + 1][1] = self.description[i]
            data[i + 1][2] = int(self.number_of_items[i])
            data[i + 1][3] = "{:.2f} kr".format(float(self.price[i])/1.25)
            data[i + 1][4] = "{:.2f} kr".format(float(self.price[i]))

        if len(name_customer) > 0 and len(phone_customer) > 0:
            c.drawString(widthA4 * 0.8 / 10, heightA4 * 8.25 / 10, 'Namn:')
            c.drawString(widthA4 * 1.43 / 10, heightA4 * 8.25 / 10, '{}'.format(name_customer))
            c.drawString(widthA4 * 0.8 / 10, heightA4 * 8.1 / 10, 'Telefon:')
            c.drawString(widthA4 * 1.55 / 10, heightA4 * 8.1 / 10, '{}'.format(phone_customer))
        elif len(name_customer) > 0:
            c.drawString(widthA4 * 0.8 / 10, heightA4 * 8.1 / 10, 'Namn:')
            c.drawString(widthA4 * 1.4 / 10, heightA4 * 8.1 / 10, '{}'.format(name_customer))
        #datum
        c.drawString(widthA4 * 7.42 / 10, heightA4 * 8.1 / 10, "Datum:")
        c.drawString(widthA4 * 8.1 / 10, heightA4 * 8.1 / 10, '{}'.format(time.strftime("%Y-%m-%d")))

        f = Table(data, colWidths=(3.5 * cm, 6.2 * cm, 2 * cm, 3.1 * cm, 3 * cm),
                  style=[('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                         ('BOX', (0, 1), (0, -1), 0.5, colors.black),
                         ('BOX', (1, 1), (1, -1), 0.5, colors.black),
                         ('BOX', (2, 1), (2, -1), 0.5, colors.black),
                         ('BOX', (3, 1), (3, -1), 0.5, colors.black),
                         ('BOX', (4, 1), (4, -1), 0.5, colors.black),
                         ('GRID', (0, 0), (-1, 0), 0.25, colors.black),
                         # Botten rutorna kring total summa och moms
                         # ('GRID', (-2, -3), (-1, -2), 0.25, colors.black),
                         # Artikelnummer kolumnen
                         ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                         ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                         # Beskrivning kolumnen
                         ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                         # Antal kolumnen
                         ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                         # Pris kolumnen
                         ('ALIGN', (3, 0), (3, -1), 'CENTER'),
                         ('ALIGN', (4, 0), (4, -1), 'CENTER'),
                         ('TOPPADDING', (0, -1), (-1, -1), 15),

                         ])
        width = 6 * cm
        height = 4 * cm
        f.wrapOn(c, width, height)
        f.drawOn(c, widthA4 * 0.75 / 10, heightA4 * 4.5 / 10)

        c.drawString(widthA4 * 5.7 / 10, heightA4 * 4.25 / 10, "Total pris exkl. moms:")
        c.drawString(widthA4 * 7.75 / 10, heightA4 * 4.25 / 10, '{:.2f} kr'.format(self.total_cost))
        c.setFont('Helvetica', 24)
        c.drawString(widthA4 * 3.85 / 10, heightA4 * 3.95 / 10, "Total pris inkl. moms:")
        c.drawString(widthA4 * 7.76 / 10, heightA4 * 3.95 / 10, '{:.2f} kr'.format(self.total_cost / 1.25))
        c.setFont('Helvetica', 12)

        # Under text
        data = [['', 'Mullhyttans Cykel & Såg', '', ''],
                ['Org.nr:', '556229-3745', '', ''],
                ['Address:', 'Selhagsvägen 3', '', ''],
                ['', '716 94 Mullhyttan', '', ''],
                ['Telefon:', '0585-40338', '', ''],
                ['Email:', 'mullhyttanscykel@telia.com', '', ''],
                ['Facebook:', 'https://www.facebook.com/mullhyttans123/', '', ''],
                ['Blocket:', 'https://www.blocket.se/mullhyttanscykel-sagservice', '', '']
                ]

        width = 6 * cm
        height = 4 * cm
        d = Table(data, style=[  # ('BOX',(0,0),(-1,-1),0.5,colors.black),
            # ('GRID',(0,0),(-1,-1),0.25,colors.black),
            # Artikelnummer kolumnen
            ('RIGHTPADDING', (0, 0), (0, -1), 15),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            # Beskrivning kolumnen
            ('RIGHTPADDING', (1, 0), (1, -1), 50),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            # Antal kolumnen
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            # Pris kolumnen
            ('ALIGN', (3, 0), (3, -1), 'LEFT'),
        ])

        d.wrapOn(c, width, height)
        d.drawOn(c, widthA4 * 1.5 / 10, heightA4 * 1.9 / 10)

        c.save()


# Centers all pop ups to center of screen
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def user_is_inactive():
    menu_frame.remove_all_articles()
    print("Reseted all from timer")


def reset_timer(event=None):
    global timer
    # cancel the previous event
    if timer is not None:
        root.after_cancel(timer)
    print("Inside reset_timer")
    # create new timer
    timer = root.after(300000, user_is_inactive)
    print(timer)


if __name__ == "__main__":
    timer = None
    # Lets just make a global shopping basket
    basket = ShoppingBasket()
    # Configure GUI and start its main loop
    root = tk.Tk()
    root.title("Streckkodsläsare")
    root.minsize(1200, 600)
    center(root)
    search_frame = GUISearchArea(root)
    menu_frame = GUIMenuArea(root)
    article_frame = GUIArticleArea(root)
    cost_frame = GUICostArea(root)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    search_frame.frame.grid(row=0, column=0, sticky="N")
    menu_frame.frame.grid(row=1, column=0, sticky="NESW")
    article_frame.frame.grid(row=0, column=1, rowspan=2, sticky="NESW")
    cost_frame.frame.grid(row=3, column=1, sticky="NESW")
    root.bind_all('<Any-KeyPress>', reset_timer)
    root.bind_all('<Any-ButtonPress>', reset_timer)
    root.mainloop()



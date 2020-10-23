import os
import csv


class Col:
    ArtNr = 0
    Beskrivning = 1
    Pris = 2
    EAN = 3
    Antal = 4


class Model:
    def __init__(self):
        self.basket = []
        self.total_price = 0
        self.path = "\\\\kontoret\\delad_mapp"

    def get_article_from_db(self, barcode):
        article = None
        db_file_list = self.check_folder_for_files(self.path + "\\") # First check kontoret/delad_mapp
        db_file_list = db_file_list if len(db_file_list) else self.check_folder_for_files('.') # Else look in local folder
        print(db_file_list)
        for file in db_file_list:
            print("Opening file:", file)
            db_as_list = self.open_file_as_list(file)
            article = self.find_article_in_list(db_as_list, barcode)
            if article is not None:
                return article
        return article

    def check_folder_for_files(self, path):
        file_list = []
        print("Checking for files in: ", path)
        for file in os.listdir(path):
            print("Found file:", file)
            if file.endswith(".csv"):
                file_list.append(path + "\\" + file)
        return file_list

    def open_file_as_list(self, file_path):
        with open(file_path, encoding='UTF-8') as f:
            return list(csv.reader(f, delimiter=";"))

    def find_article_in_list(self, db_file_list, barcode):
        for row in db_file_list:
            if barcode in row[Col.ArtNr] or barcode in row[Col.EAN]:
                return row[0:4]

    def add_article_and_update_price(self, article):
        row = self.get_row_of_article_in_basket(article[Col.EAN])
        if row is None:
            article.append(1)
            self.basket.append(article)
        else:
            self.basket[row][Col.Antal] += 1
        print("Currently in basket: ", self.basket)
        self.update_basket_total()

    def add_anything_func(self, description, cost):
        self.basket.append([" ", description, cost, "Streckkod", 1])
        self.update_basket_total()

    def get_row_of_article_in_basket(self, EAN):
        result = None
        try:
            for row, article in enumerate(self.basket):
                if article[Col.EAN] == EAN:
                    result = row
        finally:
            return result

    def update_basket_total(self):
        self.total_price = 0
        for items in self.basket:
            self.total_price += round(float(items[Col.Pris]), 2) * int(items[Col.Antal])
        print("Total kostnad:", self.total_price)

    def remove_article(self, row):
        del self.basket[row]
        self.update_basket_total()

    def add_article_to_DB(self, article_info):
        # Find the article in the database
        filename = "tillagda_streckkoder.csv"
        file_exists = os.path.isfile(self.path + '\\' + filename)
        if file_exists:
            pass
        else:
            file = open(self.path + '\\' + filename, "w").close()
        file_list = self.open_file_as_list(self.path + '\\' + filename)
        for row in file_list:
            if article_info[Col.EAN] in row[Col.EAN]:
                return 'Existent'
        with open(self.path + '\\' + filename, 'a', newline='', encoding='UTF8') as f:
            writer = csv.writer(f, delimiter=";")
            fields = article_info
            writer.writerow(fields)
            return 'Added'




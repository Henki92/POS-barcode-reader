import csv

file_to_edit = "databas1.csv"
new_file = "databas_edit.csv"
row_to_move_to_new_file1 = 0
row_to_move_to_new_file2 = 1
row_to_move_to_new_file3 = 4
row_to_move_to_new_file4 = 6
with open(file_to_edit, 'r', newline='', encoding='UTF8') as f:
    with open(new_file, mode='w', newline='', encoding='utf-8') as f_edit:
        change_writer = csv.writer(f_edit, delimiter=';')

        reader = csv.reader(f, delimiter=';')
        listbase = list(reader)
        for i, row in enumerate(listbase):
            change_writer.writerow([row[row_to_move_to_new_file1], row[row_to_move_to_new_file2], row[row_to_move_to_new_file3], row[row_to_move_to_new_file4]])
            
            

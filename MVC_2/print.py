from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
import os
import time


class Col:
    ArtNr = 0
    Beskrivning = 1
    Pris = 2
    EAN = 3
    Antal = 4


def print_function(model, name_customer, phone_customer):
    os.system("TASKKILL /F /IM AcroRD32.exe")
    update_recipt(model, name_customer, phone_customer)
    os.startfile('Kvitto.pdf')


def update_recipt(model, name_customer, phone_customer):
    widthA4, heightA4 = A4
    c = canvas.Canvas("Kvitto.pdf", pagesize=A4)

    # Rubrik kvitto
    c.setFont('Helvetica', 28)
    c.setLineWidth(.8)
    str = 'Mullhyttans Cykel & Såg Service AB'
    strLen = stringWidth(str, 'Helvetica', 28)
    c.drawString(widthA4 / 2 - strLen / 2, heightA4 * 9.2 / 10, str)

    # Över text
    c.setLineWidth(.3)
    c.setFont('Helvetica', 12)
    str = 'Varuspecifikation'
    strLen = stringWidth(str, 'Helvetica', 12)
    c.drawString(widthA4 / 2 - strLen / 2, heightA4 * 8.8 / 10, str)
    str = 'Tack för ditt köp och välkommen åter'
    strLen = stringWidth(str, 'Helvetica', 12)
    c.drawString(widthA4 / 2 - strLen / 2, heightA4 * 9 / 10, str)

    col1 = 2.6
    col2 = 6.2
    col3 = 1.2
    col4 = 3.1
    col5 = 3
    tableWidth = col1 + col2 + col3 + col4 + col5

    # Artiklar osv
    data = [['Artikelnummer:', 'Beskrivning:', 'Antal:', 'Pris/st exkl.moms:', 'Summa:'],
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
    print(model.basket)
    for i, row in enumerate(model.basket):
        data[i + 1][0] = model.basket[i][Col.ArtNr]
        data[i + 1][1] = model.basket[i][Col.Beskrivning]
        data[i + 1][2] = model.basket[i][Col.Antal]
        data[i + 1][3] = "{:.2f} kr".format(float(model.basket[i][Col.Pris]))
        data[i + 1][4] = "{:.2f} kr".format(float(model.basket[i][Col.Pris]) * int(model.basket[i][Col.Antal]))

    if len(name_customer) > 0 and len(phone_customer) > 0:
        c.drawString(widthA4 / 2 - tableWidth * cm / 2, heightA4 * 8.1 / 10, 'Telefon: {}'.format(phone_customer))
        c.setFont('Helvetica', 24)
        c.drawString(widthA4 / 2 - tableWidth * cm / 2, heightA4 * 8.3 / 10, 'Namn: {}'.format(name_customer))
    elif len(name_customer) > 0:
        c.setFont('Helvetica', 24)
        c.drawString(widthA4 / 2 - tableWidth * cm / 2, heightA4 * 8.15 / 10, 'Namn: {}'.format(name_customer))
    # datum
    c.setFont('Helvetica', 12)
    str = "Datum: {}".format(time.strftime("%Y-%m-%d"))
    strLen = stringWidth(str, 'Helvetica', 12)
    c.drawString(widthA4 / 2 + tableWidth * cm / 2 - strLen, heightA4 * 8.1 / 10, str)

    f = Table(data, colWidths=(col1 * cm, col2 * cm, col3 * cm, col4 * cm, col5 * cm),
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
    f.wrapOn(c, tableWidth * cm, height)
    f.drawOn(c, widthA4 / 2 - tableWidth * cm / 2, heightA4 * 4.5 / 10)

    str = "Total pris exkl. moms: {:.2f} kr".format(model.total_price)
    strLen = stringWidth(str, 'Helvetica', 12)
    c.drawString(widthA4 / 2 + tableWidth * cm / 2 - strLen, heightA4 * 4.25 / 10, str)
    str = "Moms 25%: {:.2f} kr".format(model.total_price * 0.25)
    strLen = stringWidth(str, 'Helvetica', 12)
    c.drawString(widthA4 / 2 + tableWidth * cm / 2 - strLen, heightA4 * 4.05 / 10, str)
    c.setFont('Helvetica', 24)
    str = "Total pris inkl. moms: {:.2f} kr".format(model.total_price * 1.25)
    strLen = stringWidth(str, 'Helvetica', 24)
    c.drawString(widthA4 / 2 + tableWidth * cm / 2 - strLen, heightA4 * 3.75 / 10,
                 "Total pris inkl. moms: {:.2f} kr".format(model.total_price * 1.25))
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
    d.drawOn(c, widthA4 * 1.5 / 10, heightA4 * 1.5 / 10)

    c.save()

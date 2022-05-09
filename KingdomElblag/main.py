import random
import tkinter as tk
from bs4 import BeautifulSoup
from urllib import request
import numpy as np
import re
import datetime
import requests
import csv
from PIL import ImageTk,Image

def wyswietlOfertyMin():
    newWindow = tk.Toplevel(master)
    newWindow.title("Oferty skrócone")
    newWindow.geometry("800x500")
    scrollbar = tk.Scrollbar(newWindow)
    scrollbar.pack(side='right', fill='y')

    lista_ofert = tk.Listbox(newWindow, width=500, height=500, yscrollcommand=scrollbar.set)
    tab = []
    with open('Kingdom Elblag/final.csv', "rt", encoding="utf-8", newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            temp = "Oferta numer: " + row['numer oferty'] + ", Lokalizacja: "+row['lokalizacja']+", Typ: "+row['typ']+",cena: " + row['cena']
            tab.append(temp)
    for i in range(len(tab)):
        lista_ofert.insert(i, str(tab[i]))
    lista_ofert.pack()

def wyswietlOfertyMax():
    newWindow = tk.Toplevel(master)
    newWindow.title("Oferty Pełne")
    newWindow.geometry("500x500")
    scrollbar_Y = tk.Scrollbar(newWindow, orient='vertical')
    scrollbar_X = tk.Scrollbar(newWindow, orient='horizontal')
    scrollbar_Y.pack(side='right', fill='y')
    scrollbar_X.pack(side='bottom', fill='x')

    lista_ofert = tk.Listbox(newWindow, width=500, height=500, yscrollcommand=scrollbar_Y.set, xscrollcommand=scrollbar_X.set)
    tab = []
    with open('Kingdom Elblag/final.csv', "rt", encoding="utf-8", newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            temp = row
            tab.append(temp)
    for i in range(len(tab)):
        lista_ofert.insert(i, str(tab[i]))
    lista_ofert.pack()

def losowaOferta():
    newWindow = tk.Toplevel(master)
    newWindow.title("Losowa Oferta")
    newWindow.geometry("500x500")
    tab = []
    tab_zdj = []
    tab_opis = []
    with open('Kingdom Elblag/final.csv', "rt", encoding="utf-8", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            temp = "Oferta numer: " + row['numer oferty'] + ", Lokalizacja: "+row['lokalizacja']+", Typ: "+row['typ']+",cena: " + row['cena']
            tab.append(temp)
            tab_zdj.append("Kingdom Elblag/"+row['zdjecie_glowne'])
            tab_opis.append(row['opis'])

    rand_int = random.randint(0, len(tab))

    tk.Label(newWindow,text=tab[rand_int]).pack()

    load = Image.open(tab_zdj[rand_int])
    render = ImageTk.PhotoImage(load)
    image = tk.Label(newWindow, image=render)
    image.image = render
    image.pack()

    T = tk.Text(newWindow, wrap=tk.WORD)
    T.insert(tk.END, tab_opis[rand_int])
    T.pack()

def pobierzOferty():
    pageNum = 1
    temp = []
    link_html = request.urlopen("http://www.kingdomelblag.pl/oferty?page=" + str(pageNum))

    def findAllLinks(html):
        bsObj = BeautifulSoup(html, 'html.parser')
        for item in bsObj.find_all("ul", class_="pagination pull-right"):
            for x in item.find_all('li'):
                for y in x.find_all('a'):
                    temp.append(re.findall('\d', y.get('href')))

        pageNum = max(temp)
        return pageNum

    pageNum = findAllLinks(link_html)

    def maxPages(pageNum):
        link_html = request.urlopen("http://www.kingdomelblag.pl/oferty?page=" + str(pageNum))
        prev = int(pageNum)
        temp = findAllLinks(link_html)
        next = int(temp[0])
        while True:
            if (prev == next):
                break
            else:
                link_html = request.urlopen("http://www.kingdomelblag.pl/oferty?page=" + str(next))
                prev = next
                temp = findAllLinks(link_html)
                next = int(temp[0])
        return next

    LastPage = maxPages(pageNum[0])

    oferty_linki = []

    for i in range(LastPage):
        html = request.urlopen("http://www.kingdomelblag.pl/oferty?page=" + str(i + 1))
        bsObj1 = BeautifulSoup(html, 'html.parser')
        for item in bsObj1.find_all("div", class_="room_item-1"):
            oferty_linki.append(item.find_next('a').get('href'))

    #print(len(oferty_linki))

    np.savetxt('Kingdom Elblag/html_ofert.csv', oferty_linki, delimiter=',', fmt='%s')


    links = np.loadtxt('Kingdom Elblag/html_ofert.csv', dtype=str, delimiter=',')
    final_tab = []

    def createRecord(html):
        global lokalizacja, opis
        url = request.urlopen(html)
        bsObj = BeautifulSoup(url, 'html.parser')

        tab = []

    # DANE NIERUCHOMOSCI
        for item in bsObj.find_all("div", class_="property-detail"):
            for dane in item.find_all("div", class_="area"):
                tab.append(dane.get_text("-"))

        for i in range(len(tab)):
            tab[i] = tab[i].replace("m-2", "m2")

    # OPIS
        for item in bsObj.find_all("meta", property="og:description"):
            opis = item.get("content")

        # TELEFON&MAIL
        temp = []
        for item in bsObj.find_all("dd"):
            temp.append(item.find("a").get("href"))
        tel = temp[0].split(':')
        mail = temp[2].split(':')

    # ZDJECIA
        temp_img = []

        for item in bsObj.find_all("div", class_="room-detail_thumbs"):
            for x in item.find_all("img"):
                y = "https://www.kingdomelblag.pl" + x.get("src")
                temp_img.append(y)
        zdj = requests.get(temp_img[0], allow_redirects=False)
        nazwa: str = temp_img[0].split('/')[-1:][0]
        f = open(f'Kingdom Elblag/zdjecia/{nazwa}', 'wb')
        f.write(zdj.content)
        f.close()

    # LOKALIZACJA
        for item in bsObj.find_all("meta", property="og:title"):
            x = item.get("content")
            y = x.split(',')
            lokalizacja = y[0] + "," + y[1]

        data_skanowania = datetime.datetime.now()
        data_skanowania = data_skanowania.strftime("%x")

        numer_oferty = ''
        typ = ''
        cena = ''
        typ_transakcji = ''
        powierzchnia = ''
        rynek = ''
        piętro = ''
        budynek_pietra = ''
        cena_za_m2 = ''
        standard_wykończenia = ''
        rok_budowy = ''
        typ_balkonu = ''
        miejsce_parkingowe = ''
        stan_wykonczenia = ''
        kaucja = ''

        for i in range(len(tab)):
            temp50 = tab[i].split('-')
            if temp50[0] == 'Numer oferty':
                numer_oferty = temp50[1]
            elif temp50[0] == 'Typ budynku':
                typ = temp50[1]
            elif temp50[0] == 'Cena':
                cena = temp50[1]
            elif temp50[0] == 'Typ transakcji':
                typ_transakcji = temp50[1]
            elif temp50[0] == 'Powierzchnia':
                powierzchnia = temp50[1]
            elif temp50[0] == 'Rynek':
                rynek = temp50[1]
            elif temp50[0] == 'Piętro':
                piętro = temp50[1]
                budynek_pietra = temp50[1]
            elif temp50[0] == 'Cena za m2':
                cena_za_m2 = temp50[1]
            elif temp50[0] == 'Standard wykończenia':
                standard_wykończenia = temp50[1]
            elif temp50[0] == 'Rok budowy':
                rok_budowy = temp50[1]
            elif temp50[0] == 'Typ balkonu':
                typ_balkonu = temp50[1]
            elif temp50[0] == 'Parking':
                miejsce_parkingowe = temp50[1]
            elif temp50[0] == 'Standard wykończenia':
                stan_wykonczenia = temp50[1]
            elif temp50[0] == 'Kaucja':
                kaucja = temp50[1]

        if numer_oferty == '':
            numer_oferty = '-1'
        if typ == '':
            typ = '-1'
        if cena == '':
            cena = '-1'
        if typ_transakcji == '':
            typ_transakcji = '-1'
        if powierzchnia == '':
            powierzchnia = '-1'
        if rynek == '':
            rynek = '-1'
        if piętro == '':
            piętro = '-1'
        if budynek_pietra == '':
            budynek_pietra = '-1'
        if cena_za_m2 == '':
            cena_za_m2 = '-1'
        if standard_wykończenia == '':
            standard_wykończenia = '-1'
        if rok_budowy == '':
            rok_budowy = '-1'
        if typ_balkonu == '':
            typ_balkonu = '-1'
        if miejsce_parkingowe == '':
            miejsce_parkingowe = '-1'
        if stan_wykonczenia == '':
            stan_wykonczenia = '-1'
        if kaucja == '':
            kaucja = '-1'


        rows_def = {
            'data_skanowania': data_skanowania,
            'numer oferty': numer_oferty,
            'typ': typ,
            'cena': cena,
            'typ transakcji': typ_transakcji,
            'powierzchnia': powierzchnia,
            'rynek': rynek,
            'piętro': piętro,
            'budynek_pietra': budynek_pietra,
            'cena za m2': cena_za_m2,
            'standard wykończenia': standard_wykończenia,
            'rok budowy': rok_budowy,
            'typ balkonu': typ_balkonu,
            'miejsce parkingowe': miejsce_parkingowe,
            'stan_wykonczenia': stan_wykonczenia,
            'kaucja': kaucja,
            'link': html,
            'liczba_zdjec': str(len(temp_img)),
            'zdjecie_glowne': 'zdjecia/' + nazwa,
            'zdjecie_glowne_link': temp_img[0],
            'opis': opis,
            'lokalizacja': lokalizacja,
            'telefon': str(tel[1]),
            'email': str(mail[1]),
            'zdjecia_linki': temp_img,
            'dotepny': '-1',
            'powierzchnia dzialki': '-1',
            "liczba pomieszczen": '-1',
            'typ zabudowy': '-1',
            'winda': '-1',
            'piwnica': '-1',
            'umeblowanie': '-1',
            'liczba lazienek': '-1',
            'lokale uzytkowe': '-1',
            'oplaty': '-1',
            'wystawa okien': '-1',
            'dojazd': '-1',
            'stan prawny dzialki': '-1',
            'data_dodania_oferty': '-1',
            'nazwa_biura': 'Kingdom Nieruchomości'
        }

        return rows_def

    fieldnames = ['data_skanowania', 'numer oferty', 'typ', 'cena', 'typ transakcji', 'powierzchnia', 'rynek', 'piętro',
                    'budynek_pietra', 'cena za m2', 'standard wykończenia', 'rok budowy', 'typ balkonu',
                    'miejsce parkingowe', 'stan_wykonczenia', 'kaucja', 'link', 'liczba_zdjec', 'zdjecie_glowne',
                    'zdjecie_glowne_link', 'opis', 'lokalizacja', 'telefon', 'email', 'zdjecia_linki', 'dotepny',
                    'powierzchnia dzialki', 'liczba pomieszczen', 'typ zabudowy', 'winda', 'piwnica', 'umeblowanie',
                    'liczba lazienek', 'lokale uzytkowe', 'oplaty', 'wystawa okien', 'dojazd', 'stan prawny dzialki',
                    'data_dodania_oferty', 'nazwa_biura']

    rows = []
    for i in range(len(links)):
        rows.append(createRecord(links[i]))
        #print(i)

    with open('Kingdom Elblag/final.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    #print("DONE")
    data_skan = datetime.datetime.now()
    label_ostatnie_skanowanie = tk.Label(master, text=data_skan)
    label_ostatnie_skanowanie.grid(row=1, column=2, pady=2)
    liczb = str(len(oferty_linki))
    label_liczba_ofert = tk.Label(master, text=liczb)
    label_liczba_ofert.grid(row=2, column=3, pady=2)

master = tk.Tk()
master.title('Kingdom Elbląg')
master.geometry("800x800")

img = tk.PhotoImage(file="Kingdom Elblag/zdjecia/logo.png")
label_logo = tk.Label(master, image=img)
label_skan = tk.Label(master, text="Ostatnie skanowanie: ")
label_liczb = tk.Label(master, text="Liczba ofert: ")

button1 = tk.Button(master, text='Skanuj oferty', width=25, command=pobierzOferty)
button2 = tk.Button(master, text='Pokaż wszystkie oferty (skrócone)', width=25, command=wyswietlOfertyMin)
button3 = tk.Button(master, text='Pokaż wszystkie oferty (pełne)', width=25, command=wyswietlOfertyMax)
button4 = tk.Button(master, text='Pokaż losową ofertę', width=25, command=losowaOferta)


label_logo.grid(row=0, column=2, pady=2)
button1.grid(row=1, column=0, pady=2)
label_skan.grid(row=1, column=1, pady=2)
label_liczb.grid(row=2, column=1, pady=2)
button2.grid(row=2, column=0, pady=2)
button3.grid(row=3, column=0, pady=2)
button4.grid(row=4, column=0, pady=2)

master.mainloop()

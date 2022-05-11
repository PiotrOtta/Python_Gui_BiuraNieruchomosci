import random
import tkinter as tk
from bs4 import BeautifulSoup
from urllib import request
import numpy as np
import re
import datetime
import requests
import csv
import os

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
        print("findAllLinks")
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

    np.savetxt('KingdomElblag/html_ofert.csv', oferty_linki, delimiter=',', fmt='%s')


    links = np.loadtxt('KingdomElblag/html_ofert.csv', dtype=str, delimiter=',')
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
        
        # ZDJECIA
        temp_img = []

        for item in bsObj.find_all("div", class_="room-detail_thumbs"):
            for x in item.find_all("img"):
                y = "https://www.kingdomelblag.pl" + x.get("src")
                temp_img.append(y)
        zdj = requests.get(temp_img[0], allow_redirects=False)
        nazwa: str = temp_img[0].split('/')[-1:][0]
        dir_path = 'zdjecia/'+numer_oferty
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        f = open(f''+dir_path+f'/{nazwa}', 'wb') #ZROBIC FOLDER Z NUMEREM OFERTY
        f.write(zdj.content)
        f.close()

        cena = cena.replace(" ","").replace("PLN","")
        print(cena)
        cena_za_m2 = cena_za_m2.replace(" ","").replace("PLN/m2","")
        print(cena_za_m2)
        powierzchnia = powierzchnia.replace(" ","").replace("m2","")

        rows_def = {
            'balkon' : typ_balkonu,
            'budynek_pietra' : budynek_pietra,
            'cena' : cena,
            'cena_za_m2' : cena_za_m2,
            'data_dodania_oferty' : '-1',
            'data_skanowania' : data_skanowania,
            'dojazd' : '-1',
            'dostepny' : '1',
            'dzielnica' : '-1',
            'email' : str(mail[1]),
            'kaucja' : kaucja,
            'liczba_lazienek' : '-1',
            'liczba_pomieszczen' : '-1',
            'liczba_wyswietlen' : '-1',
            'liczba_zdjec' : str(len(temp_img)),
            'link' : html,
            'lokale_uzytkowe' : '-1',
            'lokalizacja' : lokalizacja,
            'miejsce_parkingowe' : miejsce_parkingowe,
            'miejscowosc' : '-1',
            'nazwa_biura' : 'Kingdom Nieruchomości',
            'numer_oferty' : numer_oferty,
            'ogrod' : '-1',
            'opis' : opis,
            'oplaty' : '-1',
            'pietro' : piętro,
            'piwnica' : '-1',
            'powierzchnia' : powierzchnia,
            'powierzchnia_dzialki' : '-1',
            'przeznaczenie' : '-1',
            'rok_budowy' : rok_budowy,
            'rynek' : rynek,
            'stan_prawny_dzialki' : '-1',
            'stan_wykonczenia' : stan_wykonczenia,
            'standard_wykonczenia' : standard_wykończenia,
            'telefon' : str(tel[1]),
            'typ' : typ,
            'typ_transakcji' : typ_transakcji,
            'typ_zabudowy' : '-1',
            'ulica' : '-1',
            'umeblowanie' : '-1',
            'winda' : '-1',
            'wojewodztwo' : '-1',
            'wystawa_okien' : '-1',
            'zdjecie_glowne' : 'zdjecia/' + nazwa,
            'zdjecie_glowne_link' : temp_img[0]
        }

        return rows_def


    fieldnames = [
        'balkon', 'budynek_pietra', 'cena', 'cena_za_m2', 'data_dodania_oferty', 'data_skanowania',
        'dojazd', 'dostepny', 'dzielnica', 'email', 'kaucja', 'liczba_lazienek', 'liczba_pomieszczen',
        'liczba_wyswietlen', 'liczba_zdjec', 'link', 'lokale_uzytkowe', 'lokalizacja', 'miejsce_parkingowe',
        'miejscowosc', 'nazwa_biura', 'numer_oferty', 'ogrod', 'opis', 'oplaty', 'pietro', 'piwnica',
        'powierzchnia', 'powierzchnia_dzialki', 'przeznaczenie', 'rok_budowy', 'rynek', 'stan_prawny_dzialki', 'stan_wykonczenia',
        'standard_wykonczenia', 'telefon', 'typ', 'typ_transakcji', 'typ_zabudowy', 'ulica', 'umeblowanie',
        'winda', 'wojewodztwo', 'wystawa_okien', 'zdjecie_glowne', 'zdjecie_glowne_link']


    rows = []
    for i in range(len(links)):
        rows.append(createRecord(links[i]))

    with open('KingdomElblag/KingdomElblag.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Create CSV")
if __name__ == "__main__":
    pobierzOferty()
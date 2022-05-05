import csv
import os
from datetime import datetime

from bs4 import BeautifulSoup
import requests
from csv import writer
from Cargos.actions import Actions
import ttkbootstrap as ttk

url = "https://cargos.com.pl/pl/oferty/page-{}/?go=1&city=0&type=0&ofert=0&start_end_price=0&room=0&query="
domain = "https://cargos.com.pl/"
limit = 10


class GenerateData:
    def __init__(self, ttkProgress: ttk.Progressbar = None, ttkLabel: ttk.Label = None, to_compare=None):
        if ttkProgress:
            ttkProgress['value'] = 0
            ttkProgress.grid(column=1, row=0, sticky='we', padx=5, pady=5)
            ttkLabel.configure(text='Pobieranie...', bootstyle="info")
            ttkProgress.configure(bootstyle="striped-info")
            ttkLabel.grid(column=2, row=0, sticky='nsw', padx=5, pady=5)

        pageNumber = 1
        if to_compare is not None:
            try:
                with open(str(to_compare), newline='') as f1:
                    data1 = list(csv.reader(f1))
                data1.pop(0)
            except:
                print("WRONG FILENAME")
                return 0
        # timestamp = str(datetime.timestamp(datetime.now()))
        # file = 'scan_' + timestamp + '.csv'
        file = "Cargos.csv"
        # print(file)

        with open(file, 'w', encoding='utf8', newline='') as f:
            data = writer(f)
            header = ["balkon", "budynek_pietra", "cena", "cena_za_m2", "data_dodania_oferty", "data_skanowania",
                      "dojazd",
                      "dostepny", "dzielnica", "email", "kaucja", "liczba_lazienek", "liczba_pomieszczen",
                      "liczba_wyswietlen", "liczba_zdjec", "link", "lokale_uzytkowe", "lokalizacja",
                      "miejsce_parkingowe",
                      "miejscowosc", "nazwa_biura", "numer_oferty", "ogrod", "opis", "oplaty", "pietro", "piwnica",
                      "powierzchnia", "powierzchnia_dzialki", "przeznaczenie", "rok_budowy", "rynek",
                      "stan_prawny_dzialki",
                      "stan_wykonczenia", "standard_wykonczenia", "telefon", "typ", "typ_transakcji", "typ_zabudowy",
                      "ulica", "umeblowanie", "winda", "wojewodztwo", "wystawa_okien", "zdjecie_glowne",
                      "zdjecie_glowne_link"]
            data.writerow(header)
            actions = Actions()
            counter = 0
            if ttkProgress:
                ttkProgress['maximum'] = limit
            while True:
                lists = self.getList(pageNumber)
                if not lists or counter == limit:
                    break
                for lista in lists:
                    data_skanowania = actions.data_skanowania()
                    typ = actions.typ(lista)
                    if not typ:
                        continue
                    cena = actions.cena(lista)
                    lokalizacja = actions.lokalizacja(lista)
                    powierzchnia = actions.powierzchnia(lista, typ)
                    liczba_pomieszczen = actions.liczba_pomieszczen(lista)
                    link = domain + lista.find("a", href=True)["href"]
                    offer = self.getOffer(link)
                    zdjecia_glowne_link = actions.zdjecia_glowne_link(lista)
                    dostepny = actions.dostepny(offer)
                    if link == -1 or not offer:
                        zdjecia_glowne = actions.zdjecia_glowne(lista, "zdjecia_Cargo", lokalizacja)
                        data.writerow(
                            [-1, -1, cena, -1, -1, data_skanowania, -1,
                             dostepny, -1, -1, -1, -1, liczba_pomieszczen, -1,
                             -1, link, -1, lokalizacja, -1, -1, -1,
                             -1, -1, -1, -1, -1, -1, powierzchnia, -1,
                             -1, -1, -1, -1, -1, -1,
                             -1, typ, -1, -1, -1, -1, -1, -1,
                             -1, zdjecia_glowne, zdjecia_glowne_link])

                        # print(typ)
                        continue
                    numer_oferty = actions.numer_oferty(offer)
                    zdjecia_glowne = actions.zdjecia_glowne(lista, "zdjecia_Cargo", numer_oferty)
                    if to_compare is not None:
                        toContinue = True
                        for line in data1:
                            if line[27] == numer_oferty:
                                toContinue = False
                                break
                        if not toContinue:
                            continue
                    # print(typ)
                    typ_transakcji = actions.typ_transakcji(offer)
                    powierzchnia_dzialki = actions.powierzchnia_dzialki(offer, typ)
                    liczba_zdjec = actions.liczba_zdjec(offer)
                    zdjecia_linki = actions.zdjecia_linki(offer)
                    opis = actions.opis(offer)
                    rynek = actions.rynek(offer)
                    pietro = actions.pietro(offer)
                    cena_za_m2 = actions.cena_za_m2(offer)
                    typ_zabudowy = actions.typ_zabudowy(offer)
                    standard_wykonczenia = actions.standard_wykonczenia(offer)
                    rok_budowy = actions.rok_budowy(offer)
                    balkon = actions.balkon(offer)
                    miejsce_parkingowe = actions.miejsce_parkingowe(offer)
                    winda = actions.winda(offer)
                    stan_wykonczenia = actions.stan_wykonczenia(offer)
                    piwnica = actions.piwnica(offer)
                    umeblowane = actions.umeblowane(offer)
                    liczba_lazienek = actions.liczba_lazienek(offer)
                    lokale_uzytkowe = actions.lokale_uzytkowe(offer)
                    oplaty = actions.oplaty(offer)
                    budynek_pietra = actions.budynek_pietra(offer)
                    kaucja = actions.kaucja(offer)
                    wystawa_okien = actions.wystawa_okien(offer)
                    dojazd = actions.dojazd(offer)
                    stan_prawny_dzialki = actions.stan_prawny_dzialki(offer)
                    telefon = str(actions.telefon(offer))
                    email = actions.email(offer)
                    nazwa_biura = actions.email(offer)
                    data_dodania_oferty = actions.data_dodania_oferty(offer)

                    info = [balkon, budynek_pietra, cena, cena_za_m2, data_dodania_oferty, data_skanowania, dojazd,
                            dostepny, -1, email, kaucja, liczba_lazienek, liczba_pomieszczen, -1,
                            liczba_zdjec, link, lokale_uzytkowe, lokalizacja, miejsce_parkingowe, -1, nazwa_biura,
                            numer_oferty, -1, opis, oplaty, pietro, piwnica, powierzchnia, powierzchnia_dzialki,
                            -1, rok_budowy, rynek, stan_prawny_dzialki, stan_wykonczenia, standard_wykonczenia,
                            telefon, typ, typ_transakcji, typ_zabudowy, -1, umeblowane, winda, -1,
                            wystawa_okien, zdjecia_glowne, zdjecia_glowne_link]
                    data.writerow(info)
                    counter += 1
                    if ttkProgress:
                        ttkProgress['value'] += 1
                    if counter == limit:
                        break
                pageNumber += 1
        if ttkProgress:
            ttkProgress['value'] += limit
            ttkProgress.configure(bootstyle='striped-success')
            ttkLabel.configure(text='Zakończono', bootstyle='Success')

    def getList(self, number):
        try:
            page = requests.get(url.format(number))
            soup = BeautifulSoup(page.content, 'html.parser')
            if "Brak wyników wyszukiwania" in soup.find('div', class_="span12").text:
                return False
            else:
                return soup.find_all('div', class_="row wyniki")
        except:
            return False

    def getOffer(self, link):
        try:
            offerPage = requests.get(link)
            soupOffer = BeautifulSoup(offerPage.content, 'html.parser')
            return soupOffer.find('div', {"id": "content"})
        except:
            return False

    def joinFiles(self, one, two, delete=False, name=None):
        if name is not None:
            file = name
        else:
            timestamp = str(datetime.timestamp(datetime.now()))
            file = 'joined_' + timestamp + '.csv'
        info1 = []
        with open(one, newline='') as f1:
            data1 = list(csv.reader(f1))
        data1.pop(0)
        with open(two, newline='') as f2:
            data2 = list(csv.reader(f2))
        data2.pop(0)
        newData = data1
        for index, line in enumerate(data1):
            for line2 in data2:
                if line[27] == line2[27]:
                    if line[-1] > line2[-1]:
                        pass
                    else:
                        newData[index] = line2
                    break
        tmp = newData
        for index, line in enumerate(data2):
            for line2 in tmp:
                notFound = True
                if line[27] == line2[27]:
                    notFound = False
                    break
            if notFound:
                newData.append(line)

        with open(file, 'w', encoding='utf8', newline='') as f:
            data = writer(f)
            header = ["balkon", "budynek_pietra", "cena", "cena_za_m2", "data_dodania_oferty", "data_skanowania",
                      "dojazd",
                      "dostepny", "dzielnica", "email", "kaucja", "liczba_lazienek", "liczba_pomieszczen",
                      "liczba_wyswietlen", "liczba_zdjec", "link", "lokale_uzytkowe", "lokalizacja",
                      "miejsce_parkingowe",
                      "miejscowosc", "nazwa_biura", "numer_oferty", "ogrod", "opis", "oplaty", "pietro", "piwnica",
                      "powierzchnia", "powierzchnia_dzialki", "przeznaczenie", "rok_budowy", "rynek",
                      "stan_prawny_dzialki",
                      "stan_wykonczenia", "standard_wykonczenia", "telefon", "typ", "typ_transakcji", "typ_zabudowy",
                      "ulica", "umeblowanie", "winda", "wojewodztwo", "wystawa_okien", "zdjecie_glowne",
                      "zdjecie_glowne_link"]
            data.writerow(header)
            for line in newData:
                data.writerow(line)
        if delete:
            os.remove(one)
            os.remove(two)
        print("CARGOS DONE")

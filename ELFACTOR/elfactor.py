import base64
import io
import re
import os
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile
from datetime import datetime

import numpy as np
from csv import writer
import requests
from bs4 import BeautifulSoup

def pobierz_aktualna_oferte():
    nieruchomosci = requests.get("https://elfactor.pl/?szukaj[]&szukaj[cenaod]=0&szukaj[cenado]=999999")
    nieruchomosci = BeautifulSoup(nieruchomosci.content, 'html5lib')

    csv = []

    with open("elfactor.csv", 'w', encoding='utf8', newline='') as f:
        dane = writer(f)
        dane.writerow(["balkon", "budynek_pietra", "cena", "cena_za_m2", "data_dodania_oferty", "data_skanowania", "dojazd",
                     "dostepny", "dzielnica", "email", "kaucja", "liczba_lazienek", "liczba_pomieszczen",
                     "liczba_wyswietlen", "liczba_zdjec", "link", "lokale_uzytkowe", "lokalizacja", "miejsce_parkingowe",
                     "miejscowosc", "nazwa_biura", "numer_oferty", "ogrod", "opis", "oplaty", "pietro", "piwnica",
                     "powierzchnia", "powierzchnia_dzialki", "przeznaczenie", "rok_budowy", "rynek", "stan_prawny_dzialki",
                     "stan_wykonczenia", "standard_wykonczenia", "telefon", "typ", "typ_transakcji", "typ_zabudowy",
                     "ulica", "umeblowanie", "winda", "wojewodztwo", "wystawa_okien", "zdjecie_glowne",
                     "zdjecie_glowne_link"])


        for nieruchomosc in nieruchomosci.findAll('a', href=True):
            if nieruchomosc['href'].startswith('/Oferta,') is False: continue

            oferta = requests.get("https://elfactor.pl" + nieruchomosc['href'])
            oferta = BeautifulSoup(oferta.content, 'html5lib')

            csv = []
            # balkon
            try:
                csv.append(oferta.find('td', text='Balkon:').findNext('td').getText() not in "Brak")
            except:
                csv.append(-1)
            # budynek pietra
            try:
                csv.append(
                    re.findall("\d+", oferta.find('td', text='Ilość pięter budynku:').findNext('td').getText())[0])
            except:
                csv.append(-1)
            # cena
            csv.append(re.findall("\d+", oferta.find('span', attrs={'class': 'price'}).getText().replace(" ", ""))[0])
            # cena za m2
            csv.append(-1)
            # data dodania oferty
            csv.append(oferta.find('span', attrs={'class': 'data'}).getText()[21:31])
            # data skanowania
            csv.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            # dojazd
            csv.append(-1)
            # dostepny
            csv.append(-1)
            #dzielnica
            csv.append(-1)
            #email
            csv.append(-1)
            #kaucja
            csv.append(-1)
            #liczba łazienek
            csv.append(-1)
            #liczba pomieszczeń
            try:
                csv.append(re.findall("\d+", oferta.find('td', text='Liczba pokoi:').findNext('td').getText())[0])
            except:
                csv.append(-1)
            #liczba wyświetleń
            csv.append(-1)
            zdjecia = oferta.findAll('a', attrs={'class': 'g_fancybox'})
            # liczba zdjec
            csv.append(len(zdjecia))
            # link
            csv.append("https://elfactor.pl" + nieruchomosc['href'])
            # lokale użytkowe
            csv.append(-1)
            # lokalizacja
            csv.append(oferta.find('td', text='Ulica:').findNext('td').getText())
            # miejsce parkingowe
            try:
                csv.append(oferta.find('td', text='Garaż:').findNext('td').getText() not in "Brak")
            except:
                csv.append(-1)
            #miejscowość
            csv.append(-1)
            # nazwa biura
            csv.append("EL-FACTOR")
            # numer oferty
            nrOferty = oferta.find('h1').getText()[14:21]
            csv.append(nrOferty)
            #ogrod
            csv.append(-1)
            pelnyopis = ""
            for opis in oferta.find('table').findAllNext('p'): pelnyopis += opis.getText()
            # opis
            csv.append(pelnyopis)
            # opłaty
            try:
                csv.append(
                    re.findall("\d+", oferta.find('td', text='Opłaty dodatkowe (wynajem):').findNext('td').getText())[0])
            except:
                csv.append(-1)
            # piętro
            try:
                csv.append(re.findall("\d+", oferta.find('td', text='Piętro:').findNext('td').getText())[0])
            except:
                csv.append(-1)
            # piwnica
            csv.append(oferta.find('td', text='Piwnica:').findNext('td').getText() in "Tak")
            # powierzchnia
            csv.append(
                re.findall("\d+", oferta.find('td', text='Powierzchnia:').findNext('td').getText().replace(" ", ""))[0])
            # powierzchnia działki
            csv.append(-1)
            #przeznaczenie
            csv.append(-1)
            # rok budowy
            csv.append(-1)
            # rynek
            csv.append(oferta.find('td', text='Rynek:').findNext('td').getText())
            # stan prawny działki
            csv.append(-1)
            # stan wykończenia
            try:
                csv.append(oferta.find('td', text='Stan techniczny:').findNext('td').getText())
            except:
                csv.append(-1)
            # standard wykończenia
            csv.append(-1)
            # telefon
            try:
                csv.append(oferta.find('span', attrs={'class': 'telefon'}).getText()[9:20])
            except:
                csv.append(-1)
            #typ nieruchomości
            csv.append(oferta.find('td', text='Typ nieruchomości:').findNext('td').getText())
            #typ transakcji
            csv.append(oferta.find('td', text='Typ Transakcji:').findNext('td').getText())
            # typ zabudowy
            csv.append(-1)
            #ulica
            csv.append(-1)
            # umeblowane
            try:
                csv.append(oferta.find('td', text='Umeblowane:').findNext('td').getText() in "Tak")
            except:
                csv.append(-1)
            # winda
            try:
                csv.append(oferta.find('td', text='Winda:').findNext('td').getText() in "Tak")
            except:
                csv.append(-1)
            #wojewodztwo
            csv.append(-1)
            # wystawa okien
            csv.append(-1)
            #zdjecie
            linki = ""
            for zdjecie in zdjecia:
                linki += "https://elfactor.pl" + zdjecie['href'] + " "
                try:
                    if not os.path.exists(f'zdjecia'):
                        os.mkdir(f'zdjecia')
                    if not os.path.exists(f'zdjecia/' + nrOferty):
                        os.mkdir(f'zdjecia/' + nrOferty)
                    img = requests.get("https://elfactor.pl" + zdjecie['href'], allow_redirects=False)

                    f = open(f'zdjecia/' + nrOferty + f"/{zdjecie['href'].split('/')[2]}", 'wb')
                    f.write(img.content)
                    f.close()

                except (AttributeError):
                   csv.append(-1)

            #zdjecia_linki
            csv.append(linki)

            # zdjecie_glowne_link
            try:
                csv.append("https://elfactor.pl" + zdjecia[0]['href'])
            except:
                csv.append(-1)
            # zdjęcia w formacie base64
            # try:
            #     csv.append(base64.b64encode(requests.get("https://elfactor.pl" + zdjecia[0]['href']).content))
            # except:
            #     csv.append(-1)
            #nr oferty
            # csv.append(oferta.find('h1').getText()[14:21])
            dane.writerow(csv)
    print('dane: ', dane)
    # zapisz_statyczny_csv(dane, "ELFACTOR/elfactor.csv")
    # zapisz_statyczny_csv(dane, "elfactor.csv")
    # x = io.BytesIO()
    # np.savetxt(x, np.array(dane, dtype=object), fmt='%s', encoding='utf-8', newline='_!_', delimiter='_;_')
    # return x.getvalue().decode("utf-8")

def zapisz_statyczny_csv(listacsv, nazwapliku):
    np.savetxt(nazwapliku, np.array(listacsv, dtype=object), fmt='%s', encoding='utf-8', newline='\n', delimiter=',')

if __name__ == "__main__":
    pobierz_aktualna_oferte()

# def aktualne():
#     tekst.delete(1.0, "end")
#     tekst.insert(1.0, pobierz_aktualna_oferte())
#     messagebox.showinfo("Ok", "Możesz przekopiować (zaznacz CTRL+A).")
# def porownaj():
#     tekst.delete(1.0, "end")
#     messagebox.showinfo("...", "Wybierz ostatnią ofertę, zostanie ona porównana z aktualną pobraną z serwera.")
#     plik_ostatnia = askopenfilename()
#
#     with open(plik_ostatnia, 'r', encoding='utf-8') as plik:
#         ostatnia = plik.read().replace('\n', '').strip().split('_!_')
#     aktualna = pobierz_aktualna_oferte().replace('\n', '').strip().split('_!_')
#
#     for n in aktualna:
#         if n not in ostatnia: tekst.insert(1.0, n + "_!_")
#     messagebox.showinfo("Ok", "Możesz przekopiować (zaznacz CTRL+A).")
# def polacz():
#     tekst.delete(1.0, "end")
#     messagebox.showinfo("...", "Wybierz plik 1.")
#     plik1 = askopenfilename()
#     messagebox.showinfo("...", "Wybierz plik 2.")
#     plik2 = askopenfilename()
#
#     with open(plik1, 'r', encoding='utf-8') as plik: plik1 = plik.read().replace('\n', '').strip().split('_!_')
#     with open(plik2, 'r', encoding='utf-8') as plik: plik2 = plik.read().replace('\n', '').strip().split('_!_')
#     polaczone = set(plik1 + plik2)
#
#     for n in polaczone:
#         tekst.insert(1.0, n + "_!_")
#
#     messagebox.showinfo("Ok", "Możesz przekopiować (zaznacz CTRL+A).")

# root = Tk()
# root.geometry("400x20")
# root.title("EL-FACTOR.pl")

# def zapisz():
#     plik = asksaveasfile(mode='w', defaultextension=".csv")
#     with open(plik.name, 'w', encoding='utf8') as p:
#         p.write(str(tekst.get("1.0",END)))

# menu = Menu(root)
# root.config(menu=menu)
# menu.add_cascade(label='🌎 Aktualne', command=aktualne)
# menu.add_cascade(label='🗃 Porównaj', command=porownaj)
# menu.add_cascade(label='📃 Połącz', command=polacz)
# menu.add_cascade(label='💾 Zapisz CSV', command=zapisz)

# scroll = Scrollbar(root)
# scroll.pack(side=RIGHT, fill=Y)
# tekst = Text(root, wrap=NONE, yscrollcommand=scroll.set)
# tekst.insert("1.0", "")
# tekst.pack(fill='both', expand=1)
# scroll.config(command=tekst.yview)

# root.mainloop()
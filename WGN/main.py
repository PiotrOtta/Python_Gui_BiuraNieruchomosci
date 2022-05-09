# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from os.path import exists

# import PySimpleGUI as sg
import csv
import urllib.request
import datetime
from bs4 import BeautifulSoup
import requests
import ttkbootstrap as ttk


def cleanText(text):
    text = text.replace('\n', '')
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip()
    return text


def joinFiles(path1, path2):
    joinedOfertas = []
    with open(path1, 'r', encoding="utf-8", newline='') as f1:
        with open(path2, 'r', encoding="utf-8", newline='') as f2:
            reader1 = csv.reader(f1)
            reader2 = csv.reader(f2)
            for row in reader1:
                joinedOfertas.append(row)
            f1.seek(0)
            for row2 in reader2:
                duplikat = False
                for row1 in reader1:
                    if row1[1] == row2[1] and row1[15] == row2[15] and row1[4] == row2[4]:
                        duplikat = True
                if (duplikat == False):
                    joinedOfertas.append(row2)
                f1.seek(0)

        f2.close()

        f = open('joinedOferty.csv', 'w', encoding="utf-8", newline='')
        writer = csv.writer(f)
        writer.writerows(joinedOfertas)
        f.close()


def downloadOfertas(limit, ttkProgress:ttk.Progressbar, ttkLabel:ttk.Label):
    keys = ['Balkon',
        'Ilość kondygnacji',
        'Cenazł€$',
        'Cena /m²',
        'data_dodania_oferty',
        'data_skanowania',
        'Dojazd',
        'dostepny',
        'dzielnica',
        'email',
        'kaucja',
        'liczba_lazienek',
        'Ilość pokoi',
        'liczba_wyswietlen',
        'liczba_zdjec',
        'link',
        'lokale_uzytkowe',
        'Lokalizacja:',
        'miejsce_parkingowe',
        'miejscowosc',
        'nazwa_biura',
        'numer_oferty',
        'ogrod',
        'opis',
        'opłaty',
        'Piętro',
        'piwnica',
        'Powierzchnia',
        'Powierzchnia działki',
        'przeznaczenie',
        'Rok budowy',
        'Rynek',
        'Stan prawny działki',
        'Stan techniczny',
        'standard_wykończenia',
        'telefon',
        'Rodzaj',
        'typ transakcji',
        'typ_zabudowy',
        'ulica',
        'umeblowanie',
        'winda',
        'wojewodztwo',
        'Wystawa Okien',
        'zdjecie_glowne',
        'zdjecie_glowne_link',

    ]

    if ttkProgress:
        ttkProgress['value'] = 0
        ttkProgress['value'] = 0
        ttkProgress.grid(column=1, row=0, sticky='we', padx=5, pady=5)
        ttkLabel.configure(text='Pobieranie...', bootstyle="info")
        ttkProgress.configure(bootstyle="striped-info")
        ttkLabel.grid(column=2, row=0, sticky='nsw', padx=5, pady=5)

    if ttkProgress:
        # ttkProgress['maximum']=len(allLinks)
        ttkProgress['maximum'] = 12 + 1


    oferty = []
    # newOferty = []
    ofertyLinki = []
    # previousLinks = []

    #file_exists = exists('wgnoferty.csv')

    # if file_exists:
    #     with open('wgnoferty.csv', 'r', encoding="utf-8", newline='') as f:
    #         reader = csv.reader(f)
    #         for rows in reader:
    #             if (rows == []):
    #                 continue
    #             previousLinks.append(rows[6])
    #         f.close()

    linkBaza = '-malbork.wgn.pl/?search%5Bdistance%5D=30'

    typy = ["mieszkanie", "dom", "dzialka", "lokal", "komercyjne", "garaz"]
    typy_transakcji = ['sprzedaz', 'wynajem']

    # SPRZEDAŻ
    for k in typy_transakcji:

        for i in typy:
            #print('https://' + k + '-' + i + linkBaza)
            page = urllib.request.urlopen('https://' + k + '-' + i + linkBaza)
            code = page.read().decode('utf-8')
            soup = BeautifulSoup(code, "html.parser")

            licznik = 0
            for j in soup.findAll("a"):

                if licznik > limit: break

                link = j.attrs.get("href")
                if "/oferta/" in str(link):
                    if link not in ofertyLinki:
                        ofertyLinki.append(link)
                        subpage = urllib.request.urlopen(link)
                        subcode = subpage.read().decode('utf-8')
                        subsoup = BeautifulSoup(subcode, "html.parser")

                        table = subsoup.select_one("table", class_="table")
                        rows = table.find_all("td")

                        item = dict.fromkeys(keys)

                        for z in range(0, len(rows), 2):
                            keyText = rows[z].text
                            keyText = cleanText(keyText)
                            if keyText in keys:
                                valueText = rows[z + 1].text
                                item[keyText] = cleanText(valueText)


                        item["typ transakcji"] = k
                        item["link"] = link
                        now = datetime.date.today()
                        item["data_skanowania"] = now.strftime("%d.%m.%Y")
                        date = subsoup.select_one("p", class_="date pull-right").text
                        item['data_dodania_oferty'] = date[8:]
                        item['opis'] = cleanText(subsoup.select_one("div", class_="col-md-12 no-padding content").text)
                        # item['liczba_zdjec'] = len(subsoup.find_all("img")) dziala zle
                        item['nazwa_biura'] = "WGN"

                        nrOferty = link.partition("oferta/")[2][0:6]

                        try:
                            imgLink = subsoup.find("a", class_="main-img").findChild('img').get('src')
                            item['zdjecie_glowne_link'] = imgLink

                            if not os.path.exists(f'zdjecia'):
                                os.mkdir(f'zdjecia')
                            if not os.path.exists(f'zdjecia/' + nrOferty):
                                os.mkdir(f'zdjecia/' + nrOferty)
                            img = requests.get(imgLink, allow_redirects=False)

                            f = open(f'zdjecia/' + nrOferty + '/main.jpg', 'wb')
                            f.write(img.content)
                            f.close()

                            item['zdjecie_glowne'] = os.path.abspath(f'zdjecia/' + nrOferty + '/main.jpg')
                        except (AttributeError):
                            item['zdjecie_glowne_link'] = -1
                            item['zdjecie_glowne'] = -1



                        item['numer_oferty'] = nrOferty




                        for key, value in item.items():
                            if value is None:
                                item[key] = -1

                        item["Cenazł€$"] = item["Cenazł€$"].replace("okazja!", "").replace(" ", "")
                        item["Cena /m²"] = item["Cena /m²"].replace(" ", "")
                        item["Powierzchnia"] = item["Powierzchnia"].replace(" m²", "")
                        if item["Powierzchnia działki"] != -1:
                            item["Powierzchnia działki"] = item["Powierzchnia działki"].replace(" m²", "")

                        oferty.append(item)

                       # if (link not in previousLinks):
                        #  newOferty.append(item)

                        licznik = licznik + 1

            with open('wgnoferty.csv', 'w', encoding="utf-8", newline='') as f:
                f.write("balkon,budynek_pietra,cena,cena_za_m2,data_dodania_oferty,data_skanowania,dojazd,dostepny,dzielnica,email,kaucja,liczba_lazienek,liczba_pomieszczen,liczba_wyswietlen,liczba_zdjec,link,lokale_uzytkowe,lokalizacja,miejsce_parkingowe,miejscowosc,nazwa_biura,numer_oferty,ogrod,opis,oplaty,pietro,piwnica,powierzchnia,powierzchnia_dzialki,przeznaczenie,rok_budowy,rynek,stan_prawny_dzialki,stan_wykonczenia,standard_wykonczenia,telefon,typ,typ_transakcji,typ_zabudowy,ulica,umeblowanie,winda,wojewodztwo,wystawa_okien,zdjecie_glowne,zdjecie_glowne_link\n")
                w = csv.DictWriter(f, keys)
                w.writerows(oferty)
                f.close()

            if ttkProgress:
                ttkProgress['value'] += 1



           # with open('wgnnewoferty.csv', 'w', encoding="utf-8", newline='') as f:
             #   w = csv.DictWriter(f, keys)
             #   w.writerows(newOferty)
              #  f.close()

    #print("WGN - FIN")
    if ttkProgress:
        ttkProgress['value'] += ttkProgress['maximum']
        ttkProgress.configure(bootstyle='striped-success')
        ttkLabel.configure(text='Zakończono', bootstyle='Success')


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     layout = [[sg.Text("Aplikacja do pobierania i scalania list nieruchomości")],
#               [sg.Button("Pobierz listę nieruchomości")], [sg.Text("Wybierz pliki do scalenia:")],
#               [sg.Input(key="-IN1-", change_submits=True), sg.FileBrowse(button_text="Przegladaj", key="-IN1-")],
#               [sg.Input(key="-IN1-", change_submits=True), sg.FileBrowse(button_text="Przegladaj", key="-IN2-")],
#               [sg.Button("Scal listy nieruchomości")]]
#
#     # Create the window
#     window = sg.Window("Aplikacja", layout)
#
#     # Create an event loop
#     while True:
#         event, values = window.read()
#         if event == "Pobierz listę nieruchomości":
#             window['Pobierz listę nieruchomości'].update(disabled=True)
#             window['Scal listy nieruchomości'].update(disabled=True)
#             window['-IN1-'].update(disabled=True)
#             window['-IN2-'].update(disabled=True)
#             downloadOfertas(5)
#             window['Pobierz listę nieruchomości'].update(disabled=False)
#             window['Scal listy nieruchomości'].update(disabled=False)
#             window['-IN1-'].update(disabled=False)
#             window['-IN2-'].update(disabled=False)
#
#         if event == "Scal listy nieruchomości":
#             joinFiles(values["-IN1-"], values["-IN2-"])
#         if event == sg.WIN_CLOSED:
#             break
#
#     window.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

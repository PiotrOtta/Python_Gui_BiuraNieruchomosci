import csv
from datetime import datetime
import inspect
import os
import re
import ttkbootstrap as ttk
from urllib import request
from bs4 import BeautifulSoup
from numpy import double, loadtxt 
from PepperHouse.Obiekt import Obiekt as Obiekt
import requests

class ParseInfoInLinks:
    def parseParameterInfo(self, obiekt:Obiekt, text:str, value:str):
        value = ' '.join(value.split(' ')[1:]) if value.startswith(' ') else value
        match text:
            case 'Miejscowość':
                obiekt.miejscowosc = value
                return
            case 'Dzielnica':
                obiekt.dzielnica = value
                return
            case 'Ulica':
                obiekt.ulica = value
                return
            case 'Rok budowy':
                obiekt.rok_budowy = int(value)
                return
            case 'Pokoje':
                obiekt.liczba_pomieszczen = int(value)
                return
            case 'Województwo':
                obiekt.wojewodztwo = value
                return
            case 'Liczba łazienek':
                obiekt.liczba_lazienek = int(value)
                return
            case 'Liczba toalet':
                obiekt.liczba_lazienek = obiekt.liczba_lazienek + int(value)
                return
            case 'Przeznaczenie':
                obiekt.przeznaczenie = value
                return
            case 'Powierzchnia całkowita':
                value = double(value.split(' ')[0])
                if obiekt.typ == "Działka":
                    obiekt.powierzchnia_dzialki = value
                else:
                    obiekt.powierzchnia = value
                return

    def parseAtributes(obiekt:Obiekt, text:str):
        match text.replace(' ',''):
            case 'Balkon/taras':
                obiekt.balkon = True
                return
            case 'Garaż/miejsceparkingowe':
                obiekt.miejsce_parkingowe = True
                return
            case 'Ogródek':
                obiekt.ogrod = True
                return

    def getInformation(self, tablica:list = [], url:str = ''):
        obiekt = Obiekt()
        html:request.urlopen = request.urlopen(url)
        parsedHTML = BeautifulSoup(html, "html.parser")

        _date:BeautifulSoup = parsedHTML.find('meta', {'property': 'article:modified_time'})
        if _date:
            obiekt.data_dodania_oferty = datetime.fromisoformat(_date.get('content')).strftime("%d/%m/%Y %H:%M:%S")
        
        obiekt.nazwa_biura = "PepperHouse"
        obiekt.cena = int(parsedHTML.find("p", {"class": "property-full-card_price"}).text.replace('zł','').replace(' ','')) or -1

        obiekt.numer_oferty = str(parsedHTML.find("div", {"class": "meta-header"}).find("ul").findAll("li")[0].find('strong').next_sibling.replace(' ', '')) or None

        obiekt.liczba_wyswietlen = int(parsedHTML.find("div", {"class": "meta-header"}).find("ul").findAll("li")[1].find('strong').next_sibling.replace(' ', '')) or None

        obiekt.cena_za_m2 = int(parsedHTML.find("p", {"class": "property-full-card_subprice"}).find('strong').next_element.text.replace('zł/m²','').replace(' ','')) or None

        _parametry:BeautifulSoup = parsedHTML.findAll("div", {"class": "parameters-list"})
        for parametry in _parametry:
            items = parametry.findAll('strong')
            for item in items:
                if not item:
                    continue
                self.parseParameterInfo(obiekt, item.text, item.next_sibling.text)

        obiekt.opis = " ".join([text.text for text in parsedHTML.find('div', {'class': 'property-full-card-description'}).find('div').findAll('p')]) or None

        obiekt.telefon = parsedHTML.find('div', {'class':'contact-bar'}).findAll('a')[0].get('href').replace('tel:','') or None
        obiekt.email = parsedHTML.find('div', {'class':'contact-bar'}).findAll('a')[1].get('href').replace('mailto:','') or None

        _typTransakcji = parsedHTML.find('p', {'class': 'property-full-card_subline'}).text
        if re.search('.*(wynaj).*', _typTransakcji):
            obiekt.typ_transakcji = 'Wynajem'
        else:
            obiekt.typ_transakcji = 'Sprzedaż'

        obiekt.balkon = False
        obiekt.miejsce_parkingowe = False
        obiekt.ogrod = False
        try:
            _atrybuty:BeautifulSoup = parsedHTML.find('div', {'class': 'property-full-card_attributes'}).find('ul').findAll('li')

            for atrybut in _atrybuty:
                if not atrybut:
                    continue
                _text = atrybut.find('i').next_sibling.text
                if not _text:
                    continue
                self.parseAtributes(obiekt, _text)
        except:
            pass
        
        # ściąganie fotek
        fotki:list = []
        _zdjeciaCarousel:BeautifulSoup = parsedHTML.find('div', {'class': 'carousel_viewport'}).findAll('div', {'class': 'carousel_item'})
        for zdjecie in _zdjeciaCarousel:
            linkDoFotki:str = zdjecie.find('a').get('href')
            fotki.append(linkDoFotki)

        obiekt.liczba_zdjec = len(fotki)
        obiekt.zdjecie_glowne_link = fotki[0]
        if not os.path.exists(f'zdjecia'):
            os.mkdir(f'zdjecia')
        if not os.path.exists(f'zdjecia/{obiekt.numer_oferty}'):
            os.mkdir(f'zdjecia/{obiekt.numer_oferty}')
        # nie mam miejsca na dysku C przez co nie mogę ściągnąć wszystkich zdjęć do każdej oferty
        # for i in range (0, len(fotki)):
        for i in range (0, 1):
            fota = requests.get(fotki[i], allow_redirects=False)
            nazwa:str = (fotki[i].split('/')[-1:])[0]
            f = open(f'zdjecia/{obiekt.numer_oferty}/{nazwa}','wb')
            f.write(fota.content)
            f.close()
            if i == 0:
                obiekt.zdjecie_glowne = os.path.abspath(f'zdjecia/{obiekt.numer_oferty}/{nazwa}')

        obiekt.defineLocalization()
        obiekt.fillEmpty()
        tablica.append(obiekt)

    def __init__(self, ttkProgress:ttk.Progressbar = None, ttkLabel:ttk.Label = None, labelAfterParse:ttk.Label = None):
        if ttkProgress:
            ttkProgress['value'] = 0
            if labelAfterParse:
                ttkProgress.grid(column=1, row=1, sticky='we', padx=5, pady=5)
            ttkLabel.configure(text='Analizowanie...', bootstyle="warning")
            ttkProgress.configure(bootstyle="warning-info")
            if labelAfterParse: 
                ttkLabel.grid(column=2, row=1, sticky='nsw', padx=5, pady=5)
                labelAfterParse.configure(text='')
        # pobieram wszystkie możliwe atrybuty mojej klasy obiektu do tablicy
        _nullObject = Obiekt()
        atrybutyKlasyObiekt = inspect.getmembers(_nullObject, lambda a:not(inspect.isroutine(a)))
        atrybuty:list = [atrybut[0] for atrybut in atrybutyKlasyObiekt if not(atrybut[0].startswith('__') and atrybut[0].endswith('__'))]

        allLinks = loadtxt('linkiDoOfert.csv', dtype=str)
        _maxAmmount = 10 # bo nie mam miejsca :C
        if ttkProgress:
            # ttkProgress['maximum']=len(allLinks)
            ttkProgress['maximum']=_maxAmmount+1
        tablicaObiektowOfert:list = []
        _i = 0
        for link in allLinks:
            self.getInformation(tablicaObiektowOfert, link)
            if ttkProgress:
                ttkProgress['value'] += 1
            if _i == _maxAmmount:
                break
            _i = _i + 1
        
        # zapis danych do pliku csv
        nazwapliku = f'PepperHouse.csv'
        with open (nazwapliku,'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=atrybuty)
            writer.writeheader()
            for obiekt in tablicaObiektowOfert:
                writer.writerow(obiekt.__dict__)
        if ttkProgress:
            ttkProgress['value']+=ttkProgress['maximum']
            ttkProgress.configure(bootstyle='striped-success')
            ttkLabel.configure(text='Zakończono',bootstyle='Success')
            if labelAfterParse:
                labelAfterParse.configure(text=f'Przeanalizowany wyniki zapisano jako: {nazwapliku}')

if __name__ == "__main__":
    ParseInfoInLinks()
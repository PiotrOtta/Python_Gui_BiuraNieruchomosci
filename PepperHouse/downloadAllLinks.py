from datetime import datetime
from tkinter import Label
from urllib import request
from bs4 import BeautifulSoup
from numpy import savetxt
import ttkbootstrap as ttk

class DownloadAllLinks:
    def __init__(self, ttkProgress:ttk.Progressbar = None, ttkLabel:ttk.Label = None):
        if ttkProgress:
            ttkProgress['value'] = 0
            ttkProgress.grid(column=1, row=0, sticky='we', padx=5, pady=5)
            ttkLabel.configure(text='Pobieranie...', bootstyle="info")
            ttkProgress.configure(bootstyle="striped-info")
            ttkLabel.grid(column=2, row=0, sticky='nsw', padx=5, pady=5)
        # wyszukanie wszystkich linków do stron z ogłoszeniami
        allPageLinks = ['https://www.pepperhouse.pl/wyszukiwarka']
        html:request.urlopen = request.urlopen(allPageLinks[0])
        parsedHTML = BeautifulSoup(html, "html.parser")
        _tempLinks:list = parsedHTML.find("div",{"class":"listing_pagination"}).find("nav",{"class":"pagination"}).find("ul").findAll("a")
        _maxNumber = 1
        for link in _tempLinks:
            link = link.get('href')
            _max = [int(liczba) for liczba in link.split('/') if liczba.isdigit()] or [0]
            _maxNumber = _max[0] if _maxNumber < _max[0] else _maxNumber
            _link = link.split(str(_maxNumber))
        if ttkProgress:
            ttkProgress['maximum']=800
        _i = 2
        while _i <= _maxNumber:
            allPageLinks.append(f'https://www.pepperhouse.pl/wyszukiwarka/strona/{_i}')
            _i = _i+1
            if ttkProgress:
                ttkProgress['value']+=1

        # pobranie wszystkich możliwych linków do ogłoszeń z każdej strony w tablicy allPageLinks
        allLinksToOffers:list = []
        for link in allPageLinks:
            html:request.urlopen = request.urlopen(link)
            parsedHTML = BeautifulSoup(html, "html.parser")
            _tempLinks:list = parsedHTML.findAll("article",{"class":"property-card"})
            for offer in _tempLinks:
                allLinksToOffers.append(offer.a.get('href'))
                if ttkProgress:
                    ttkProgress['value']+=1

        # zapis uzyskanych linków do pliku csv
        savetxt(f'linkiDoOfert.csv', allLinksToOffers, delimiter=' ', newline='\n', fmt='%s')
        if ttkProgress:
            ttkProgress['value']+=800
            ttkProgress.configure(bootstyle='striped-success')
            ttkLabel.configure(text='Zakończono',bootstyle='Success')

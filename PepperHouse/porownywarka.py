import csv
import os

from numpy import savetxt
from Obiekt import Obiekt
import ttkbootstrap as ttk

class Porownywarka:
    def importObjectsFromCSV(self, name:str, headers:bool = False) -> list:
        if len(name.split("/")) > 1:
            path = name;
        else:
            path = os.path.abspath(f'{name}')
        if not path.endswith('.csv'):
            path = f'{path}.csv'
        with open(path, mode='r', encoding="utf8") as file:
            reader = csv.reader(file)
            atrybuty:list = []
            atrybuty = next(reader)
            rows = []
            for row in reader:
                rows.append(row)
            if headers:
                return atrybuty
            else:
                return rows
    textLabel:str = ''
    noweElementy:list = []
    zmodyfikowaneElementy:list = []
    def compareCSV(self, rows1, rows2, headers:list):
        self.noweElementy:list = []
        self.zmodyfikowaneElementy:list = []
        for row2 in rows2:
            _newState = True
            _modifiedState = False
            _whatModified = []
            for item in rows1:
                if row2[21] == item[21]:
                    _newState = False
                    for i in range (0, 45):
                        if i == 21:
                            continue
                        if not row2[i] == item[i]:
                            _whatModified.append({headers[i]: row2[i]})
                            _modifiedState = True
                    break
            if _newState or _modifiedState:
                if _newState:
                    self.noweElementy.append(row2)
                if _modifiedState:
                    self.zmodyfikowaneElementy.append({row2[21]: _whatModified})

        listaNoweObiekty:list = []
        for row in self.noweElementy:
            _obiektPolaczony:Obiekt = Obiekt()
            _obiektPolaczony.fromList(headers, row)
            _obiektPolaczony.fillEmpty()
            self.textLabel.join(f'Nowy element {_obiektPolaczony.numer_oferty}\n')
            listaNoweObiekty.append(_obiektPolaczony)

        if self.noweElementy:
            self.textLabel = f'Plik nowych elementów został utworzony: \"Nowe Elementy.csv\" {self.textLabel}'
            savetxt(f'Nowe Elementy.csv', self.noweElementy, delimiter=' ', newline='\n', fmt='%s')
        if self.zmodyfikowaneElementy:
            self.textLabel = f'Plik zmodyfikowanych elementów został utworzony: \"Zmodyfikowane Elementy.csv\" {self.textLabel}'
            savetxt(f'Zmodyfikowane Elementy.csv', self.zmodyfikowaneElementy, delimiter=' ', newline='\n', fmt='%s')
        # print(noweElementy)
        # print(zmodyfikowaneElementy)
        # listaZmodyfikowaneObiekty:list = []
        # for row in zmodyfikowaneElementy:
        #     _obiektPolaczony:Obiekt = Obiekt()
        #     _obiektPolaczony.fromList(headers, row)
        #     _obiektPolaczony.fillEmpty()
        #     print(f'Zmodyfikowany element {_obiektPolaczony.numer_oferty}')
        #     listaZmodyfikowaneObiekty.append(_obiektPolaczony)

    def __init__(self, nazwa1:str, nazwa2:str, labelAfterCompare:ttk.Label = None):
        try:
            headers = self.importObjectsFromCSV(nazwa1, True)
            rows1 = self.importObjectsFromCSV(nazwa1)
            rows2 = self.importObjectsFromCSV(nazwa2)
            self.compareCSV(rows1, rows2, headers)
            if labelAfterCompare:
                labelAfterCompare.configure(text=f'Ukończono porównywanie.\n{self.textLabel}')
        except:
            if labelAfterCompare:
                labelAfterCompare.configure(text=f'Nie znaleziono podanego pliku lub podanych plików!', bootstyle='danger')

if __name__ == "__main__":
    Porownywarka('oferty22_03_2022__22_47_28', 'oferty22_03_2022__22_59_36')
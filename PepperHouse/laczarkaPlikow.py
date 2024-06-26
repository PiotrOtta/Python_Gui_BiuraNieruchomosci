import csv
import os
from PepperHouse.Obiekt import Obiekt as Obiekt
import ttkbootstrap as ttk


class LaczarkaPlikow:
    def importObjectsFromCSV(self, name: str, headers: bool = False) -> list:
        if len(name.split("/")) > 1:
            path = name;
        else:
            path = os.path.abspath(f'{name}')
        if not path.endswith('.csv'):
            path = f'{path}.csv'
            print('jop')
        with open(path, mode='r', encoding="utf8") as file:
            reader = csv.reader(file)
            atrybuty: list = []
            if headers:
                atrybuty = next(reader)
            rows = []
            indeks: int = 0
            for row in reader:
                indeks += 1
                if indeks == 1: continue
                rows.append(row)
            if headers:
                return atrybuty
            else:
                return rows

    def evalutateDifferences(self, lista, row2):
        for item in lista:
            sameChance = 0
            if row2[21] == item[21]:
                sameChance += 100
            # importantFieldIndexes = [0, 2, 9, 12, 25, 27, 35]
            importantFieldIndexes = [0, 2, 12, 25, 27]

            for i in importantFieldIndexes:
                if item[i] == -1: continue
                if row2[i] == item[i]: sameChance += 1
            if (row2[17] == item[17]) and (item[17] != -1):
                sameChance *= 3
            if sameChance >= 10:
                return False
        return True

    def joinFiles(self, rows1, rows2, name: str, headers: list):
        lista: list = rows2
        kopiaListy = lista
        for row2 in rows1:
            _state = self.evalutateDifferences(lista, row2)
            if _state:
                kopiaListy.append(row2)
            else:
                try:
                    kopiaListy.remove(row2)
                except:
                    print(row2)
        listaObiektow: list = []
        for row in kopiaListy:
            obiektPolaczony: Obiekt = Obiekt()
            obiektPolaczony.fromList(headers, row)
            obiektPolaczony.fillEmpty()
            listaObiektow.append(obiektPolaczony)
        if not name.endswith('.csv'):
            name = f'{name}.csv'
        with open(f'{name}', 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for obiekt in listaObiektow:
                writer.writerow(obiekt.__dict__)
        self.textLabel = f'Arkusz połączony to: \"{name}\"'

    def __init__(self, nazwa1: str, nazwa2: str, nazwaPolaczenia: str = 'polaczenie', labelAfterJoin: ttk.Label = None):
        headers = self.importObjectsFromCSV(nazwa1, True)
        rows1 = self.importObjectsFromCSV(nazwa1)
        rows2 = self.importObjectsFromCSV(nazwa2)
        self.joinFiles(rows1, rows2, nazwaPolaczenia, headers)
        try:

            if labelAfterJoin:
                labelAfterJoin.configure(text=f'Ukończono połączenie.\n{self.textLabel}')
        except:
            if labelAfterJoin:
                labelAfterJoin.configure(text=f'Nie znaleziono podanego pliku lub podanych plików!', bootstyle='danger')


if __name__ == "__main__":
    LaczarkaPlikow('oferty22_03_2022__22_34_14', 'oferty22_03_2022__22_47_28')

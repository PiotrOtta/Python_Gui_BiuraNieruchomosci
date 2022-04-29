

from datetime import datetime
import inspect
from numpy import double


class Obiekt:
    typ:str = None
    cena:int = None
    typ_transakcji:str = None
    przeznaczenie:str = None
    dostepny:bool = None
    powierzchnia:double = None
    powierzchnia_dzialki:double = None
    link:str = None
    liczba_zdjec:int = None
    zdjecie_glowne = None #typ
    zdjecie_glowne_link:str = None
    opis:str = None
    rynek:str = None
    liczba_pomieszczen:int = None
    pietro:int = None
    lokalizacja:str = None
    wojewodztwo:str = None
    miejscowosc:str = None
    dzielnica:str = None
    ulica:str = None
    cena_za_m2:double = None
    typ_zabudowy:str = None
    standard_wykonczenia:str = None
    rok_budowy:int = None
    balkon:bool = None
    miejsce_parkingowe:bool = None
    ogrod:bool = None
    winda:bool = None
    stan_wykonczenia:str = None
    piwnica:bool = None
    umeblowanie:bool = None
    liczba_lazienek:int = None
    numer_oferty:str = None
    lokale_uzytkowe:str = None
    oplaty:str = None
    budynek_pietra:int = None
    kaucja:int = None
    wystawa_okien:str = None
    dojazd:str = None
    stan_prawny_dzialki:str = None
    telefon:str = None
    email:str = None
    liczba_wyswietlen:int = None
    nazwa_biura:str = None
    data_dodania_oferty:datetime = None
    data_skanowania:datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def fillEmpty(self):
        atrybutyKlasyObiekt = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        atrybuty:list = [atrybut[0] for atrybut in atrybutyKlasyObiekt if not(atrybut[0].startswith('__') and atrybut[0].endswith('__'))]
        for i in range(len(atrybuty)):
            if getattr(self, atrybuty[i]):
                continue
            setattr(self, atrybuty[i], '-1')

    def fromList(self, headers:list, values:list):
        for i in range(len(headers)):
            setattr(self, headers[i], values[i])
    
    def defineLocalization(self):
        self.lokalizacja = f"{self.miejscowosc}, {self.dzielnica}, {self.ulica}"

if __name__ == "__main__":
    obiekt = Obiekt()
    obiekt.balkon = True
    print(obiekt.balkon)
    print(obiekt.budynek_pietra)
    obiekt.fillEmpty()
    print(obiekt.balkon)
    print(obiekt.budynek_pietra)
    

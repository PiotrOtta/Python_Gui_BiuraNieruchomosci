from datetime import datetime
import inspect
from numpy import double

class Obiekt:
    balkon:bool = None
    budynek_pietra:int = None
    cena:int = None
    cena_za_m2:double = None
    data_dodania_oferty:datetime = None
    data_skanowania:datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dojazd:str = None
    dostepny:bool = None
    dzielnica:str = None
    email:str = None
    kaucja:int = None
    liczba_lazienek:int = None
    liczba_pomieszczen:int = None
    liczba_wyswietlen:int = None
    liczba_zdjec:int = None
    link:str = None
    lokale_uzytkowe:str = None
    lokalizacja:str = None
    miejsce_parkingowe:bool = None
    miejscowosc:str = None
    nazwa_biura:str = None
    numer_oferty:str = None
    ogrod:bool = None
    opis:str = None
    oplaty:str = None
    pietro:int = None
    piwnica:bool = None
    powierzchnia:double = None
    powierzchnia_dzialki:double = None
    przeznaczenie:str = None
    rok_budowy:int = None
    rynek:str = None
    stan_prawny_dzialki:str = None
    stan_wykonczenia:str = None
    standard_wykonczenia:str = None
    telefon:str = None
    typ:str = None
    typ_transakcji:str = None
    typ_zabudowy:str = None
    ulica:str = None
    umeblowanie:bool = None
    winda:bool = None
    wojewodztwo:str = None
    wystawa_okien:str = None
    zdjecie_glowne = None #typ
    zdjecie_glowne_link:str = None

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
    

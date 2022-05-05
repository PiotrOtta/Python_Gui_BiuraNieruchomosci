import os
import shutil
import urllib
from datetime import datetime
from urllib.parse import urlparse

import re


class Actions:
    def __init__(self):
        pass

    def typ(self, location):
        try:
            return re.sub(' +', ' ',
                          location.find('div', class_="features").find("p").contents[0].text.replace('\n', '').strip())
        except:
            return False

    def cena(self, location):
        try:
            return ''.join(filter(str.isdigit, re.sub(' +', '', location.find('div', class_="price")
                                                      .text.replace('\n', '').strip())))
        except:
            return -1

    def typ_transakcji(self, location):
        try:
            tmp = location.find('div', class_='offer_box').findAll('div', class_='row')[1].text
            if "sprzed" in tmp:
                return "sprzedaz"
            elif "wynaj" in tmp:
                return "wynajem"
            else:
                return -1
        except:
            return -1

    def dostepny(self, location):
        try:
            if location:
                return True
            else:
                return False
        except:
            return -1

    def powierzchnia(self, location, typ):
        try:
            if "działka" in typ.lower():
                return -1
            tmp = location.find('div', class_="features").text.replace('\n', '').strip()
            size = ''.join(
                filter(str.isdigit, re.sub(' +', ' ', re.findall('[\d]+', tmp)[0].replace('\n', '').strip())))
            if any(char.isdigit() for char in size):
                return size
            else:
                return -1
        except:
            return -1

    def powierzchnia_dzialki(self, location, typ):
        try:
            tmpTab = location.find('table', class_="table").findAll('tr')
            size = ""
            for row in tmpTab:
                if "powierzchnia działki:" in row.text.lower():
                    size = row.findAll('td')[1].text
                    break
                elif "działka" in typ.lower():
                    if "powierzchnia:" in row.text.lower():
                        size = row.findAll('td')[1].text

            if any(char.isdigit() for char in size):
                return re.findall('[\d]+', size)[0]
            else:
                return -1
        except:
            return -1

    def link(self, location):
        try:
            return domain + location.find("a", href=True)["href"]
        except:
            return -1

    def liczba_zdjec(self, location):
        try:
            return len(location.find('div', {"id": "photo-group"}).findAll('a'))
        except:
            return -1

    def zdjecia_linki(self, location):
        try:
            tmp = location.find('div', {"id": "photo-group"}).findAll('a', href=True)
            photoArray = []
            for photo in tmp:
                photoArray.append(photo["href"])
            return photoArray
        except:
            return -1

    def zdjecia_glowne(self, location, folder, nr):
        try:
            tmpUrl = location.find('img', src=True)["src"]
            if not os.path.exists(folder):
                os.mkdir(folder)
            nr_path = os.path.join(folder, nr)
            if not os.path.exists(nr_path):
                os.mkdir(nr_path)
            else:
                shutil.rmtree(nr_path, ignore_errors=True)
            name = os.path.basename(urlparse(tmpUrl).path)
            # photo = os.path.join(os.path.dirname(__file__), timestamp + "/" + name)
            photo = os.path.join(nr_path, name)

            urllib.request.urlretrieve(tmpUrl, photo)
            return photo
        except:
            return -1

    def zdjecia_glowne_link(self, location):
        try:
            return location.find('img', src=True)["src"]
        except:
            return -1

    def opis(self, location):
        try:
            return re.sub(' +', ' ', location.find('div', class_='text-center').findAll()[-2].next.text
                          .replace('\n', ' ').replace('\r', ' ').strip())
        except:
            return -1

    def rynek(self, location):
        try:
            return -1
        except:
            return -1

    def liczba_pomieszczen(self, location):
        try:
            tmp = location.find('div', class_="features").text.replace('\n', '').strip()
            return re.sub(' +', ' ', re.findall('[\d]+', tmp)[2].replace('\n', '').strip())
        except:
            return -1

    def pietro(self, location):
        try:
            tmpTab = location.find('table', class_="table").findAll('tr')
            for row in tmpTab:
                if "piętro" in row.text.lower():
                    tmp = row.findAll('td')[1].text
                    return re.sub(' +', ' ', re.findall('[\d]+', tmp)[0].replace('\n', '').strip())

            return -1
        except:
            return -1

    def lokalizacja(self, location):
        try:
            return re.sub(' +', ' ',
                          location.find('div', class_="property-item").find('h3').text.replace('\n', '').strip())
        except:
            return -1

    def cena_za_m2(self, location):
        try:
            return ''.join(filter(str.isdigit, location.find('table', class_="table")
                                  .find('td', class_="zielony").text))
        except:
            return -1

    def typ_zabudowy(self, location):
        try:
            return -1
        except:
            return -1

    def standard_wykonczenia(self, location):
        try:
            return -1
        except:
            return -1

    def rok_budowy(self, location):
        try:
            return -1
        except:
            return -1

    def balkon(self, location):
        try:
            tmp = location.find('div', class_='text-center').findAll()[-2].next.text.lower()
            if "balkon" in tmp:
                if "brak balkon" in tmp or "bez balkon" in tmp or "nie posiada balkon" in tmp:
                    return False
                else:
                    return True
            else:
                return -1
        except:
            return -1

    def miejsce_parkingowe(self, location):
        try:
            tmp = location.find('div', class_='text-center').findAll()[-2].next.text.lower()
            if "garaż" in tmp or "parking" in tmp:
                if "bez miejsca parking" in tmp or "bez garaż" in tmp or "nie posiada miejsca park" in tmp:
                    return False
                else:
                    return True
            else:
                return -1
        except:
            return -1

    def winda(self, location):
        try:
            tmp = location.find('div', class_='text-center').findAll()[-2].next.text.lower()
            if "wind" in tmp:
                return True
            else:
                return False
        except:
            return -1

    def stan_wykonczenia(self, location):
        try:
            tmpTab = location.find('table', class_="table")
            return tmpTab.find('td', text="Stan techniczny:").find_next('td').text.strip()
        except:
            return -1

    def piwnica(self, location):
        try:
            tmp = location.find('div', class_='text-center').findAll()[-2].next.text.lower()
            if "piwni" in tmp:
                nots = ["niepodpiwniczony", "bez piwni", "brak piwni"]
                if any(item in tmp for item in nots):
                    return False
                else:
                    return True
            return -1
        except:
            return -1

    def umeblowane(self, location):
        try:
            tmp = location.find('div', class_='text-center').findAll()[-2].next.text.lower()
            if "mebl" in tmp:
                nots = ["nieumeblow", "nie umeblow", "brak mebl", "bez mebl"]
                if any(item in tmp for item in nots):
                    return False
                else:
                    return True
            return -1
        except:
            return -1

    def liczba_lazienek(self, location):
        try:
            tmp = location.find('div', class_='text-center').findAll()[-2].next.text.lower()
            if "łazien" in tmp:
                nots = ["brak łazienki", "bez łazienki"]
                if any(item in tmp for item in nots):
                    return 0
                elif "łazienka" in tmp:
                    return 1
                elif "łazienki" in tmp:
                    res = tmp.partition("łazienki")[0].split(" ")[-1]
                    return res
                elif "łazienek" in tmp:
                    res = tmp.partition("łazienek")[0].split(" ")[-1]
                    return res
            return -1
        except:
            return -1

    def numer_oferty(self, location):
        try:
            tmpTab = location.find('table', class_="table")
            return tmpTab.find('td', text="Numer oferty:").find_next('td').text.strip()
        except:
            return -1

    def lokale_uzytkowe(self, location):
        try:
            return -1
        except:
            return -1

    def oplaty(self, location):
        try:
            tmp = location.find('div', class_='text-center').findAll()[-2].next.text.lower()
            price = 0.0
            if "czynsz" in tmp:
                res = tmp.partition("czynsz")[1].split(" ")[0]
                try:
                    float(res)
                    price = price + float(res)
                except ValueError:
                    pass
            nots = ["opłaty za"]
            for cost in nots:
                if cost in tmp:

                    res = tmp.partition(cost)[0].split(" ")[-1]
                    try:
                        float(res)
                        price = price + float(res)
                    except ValueError:
                        pass
                    res = tmp.partition(cost)[1].split(" ")[1]
                    try:
                        float(res)
                        price = price + float(res)
                    except ValueError:
                        pass
                    res = tmp.partition(cost)[1].split(" ")[2]
                    try:
                        float(res)
                        price = price + float(res)
                    except ValueError:
                        pass
            if cost > 0:
                return cost
            else:
                return -1
        except:
            return -1

    def budynek_pietra(self, location):
        try:
            tmpTab = location.find('table', class_="table")
            tmp = tmpTab.find('td', text="Piętro / pięter:").find_next('td').text.strip()
            return re.sub(' +', ' ', re.findall('[\d]+', tmp)[1].replace('\n', '').strip())
        except:
            return -1

    def kaucja(self, location):
        try:
            tmp = location.find('div', class_='text-center').findAll()[-2].next.text.lower()
            if "kaucja" in tmp:
                res = tmp.partition("kaucja")[1].split(" ")[0]
                return float(''.join(filter(str.isdigit, res)))

            else:
                return -1
        except:
            return -1

    def wystawa_okien(self, location):
        try:
            return -1
        except:
            return -1

    def dojazd(self, location):
        try:
            return -1
        except:
            return -1

    def stan_prawny_dzialki(self, location):
        try:
            tmpTab = location.find('table', class_="table").findAll('tr')
            for row in tmpTab:
                if "rodzaj własności:" in row.text.lower():
                    return re.sub(' +', ' ', row.findAll('td')[1].text.replace('\n', '').strip())

            return -1
        except:
            return -1

    def telefon(self, location):
        try:
            tmp = location.find('h4', class_="h4title", text="Kontakt z nami").find_next('div', class_="row") \
                .findAll('span')
            phones = []
            for tel in tmp:
                phones.append(re.sub(' +', '', tel.text.strip()))
            return phones
        except:
            return -1

    def email(self, location):
        try:
            return location.find('h4', class_="h4title", text="Kontakt z nami").find_next('div', class_="row") \
                .find('a').text
        except:
            return -1

    def nazwa_biura(self, location):
        try:
            return location.find('h4', class_="h4title", text="Kontakt z nami").find_next('div', class_="row") \
                .find('b').text
        except:
            return -1

    def data_dodania_oferty(self, location):
        try:
            return -1
        except:
            return -1

    def data_skanowania(self):
        try:
            return datetime.now()
        except:
            return -1

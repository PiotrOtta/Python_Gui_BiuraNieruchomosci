import csv
import os
import re
import threading
from tkinter import BOTTOM, Toplevel, filedialog, messagebox
from PIL import ImageTk, Image, UnidentifiedImageError
import ttkbootstrap as ttk
# PepperHouse
import PepperHouse.downloadAllLinks as PepperHouse_DownloadAllLinks
import PepperHouse.laczarkaPlikow as PepperHouse_LaczarkaPlikow
import PepperHouse.parseInfoInLinks as PepperHouse_ParseInfoInLinks
import PepperHouse.porownywarka as PepperHouse_Porownywarka

# Cargos
import Cargos.generateData as Cargos_GenerateData

#Kingdom
import KingdomElblag.kingdom_csv as kingodmcsv

import WGN.main as WGN

import ELFACTOR.elfactor as Elfactor

wybraneBiuro = [True, False, False, False, False]
nazwyPrzeanalizowanychPlikow = ["PepperHouse.csv", "KingdomElblag/KingdomElblag.csv", "Cargos.csv", "wgnoferty.csv", "elfactor.csv"]

sortNazwy = ["Nazwa", "Cena", "Powierzchnia", "Numer oferty"]
sorty = [0] * len(sortNazwy)  # 0 - nie bierz pod uwagę, 1 - asc, 2 - desc
wybranySort = 0
nazwaPolaczonegoPliku = "Symbioza.csv"
officeButton = None
everyOffer = []
offersToShow = []


def handleOfficeButtonClick(button: ttk.Button, indeks: int):
    global wybraneBiuro
    wybraneBiuro = [False, False, False, False, False]
    for officebuttons in officeButton:
        officebuttons.configure(bootstyle="disabled")
    wybraneBiuro[indeks] = not wybraneBiuro[indeks]
    if wybraneBiuro[indeks]:
        button.configure(bootstyle="light")
    else:
        button.configure(bootstyle="disabled")


def PepperHouse(numerOperacji: int = None, progress=None, labelDownload=None):
    match numerOperacji:
        case 1:
            PepperHouse_DownloadAllLinks.DownloadAllLinks(progress, labelDownload)
        case 2:
            PepperHouse_ParseInfoInLinks.ParseInfoInLinks(progress, labelDownload)
        case 3:
            PepperHouse_Porownywarka.Porownywarka(),  # to raczej jest useless do tego projektu
        case 4:
            PepperHouse_LaczarkaPlikow.LaczarkaPlikow()


def Cargos(numerOperacji: int = None, progress=None, labelDownload=None):
    match numerOperacji:
        case 1: Cargos_GenerateData.GenerateData(progress, labelDownload)
        # case 2:
        # case 3:
        # case 4:

def Kingdom(numerOperacji:int = None):
    match numerOperacji:
        case 1: kingodmcsv.pobierzOferty()

absPath: str = os.path.abspath(os.getcwd())


def getFileName(Info: str = ""):
    name: str = filedialog.askopenfilename(
        title=f"Wybierz arkusz {Info}",
        # initialdir="/",
        filetypes=(
            ("Arkusze kalkulacyjne", "*.csv"),
            ("Wszystkie pliki", "*.*")
        )
    )
    # zamień znak / na \
    _changedName = os.path.abspath(name)
    _osName = os.path.basename(name)
    if _changedName == (absPath + "\\" + _osName):
        return _osName
    else:
        return _changedName


def projekt02_GUI():
    root = ttk.Window(themename="vapor")
    root.geometry('1700x400')
    root.minsize(700, 400)
    root.title("Projekt 2 - GUI pięciu biur nieruchomości")
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)
    root.grid_rowconfigure(0, weight=1)
    underRoot = ttk.Frame(root)
    underRoot.grid(column=0, row=0, sticky="nswe")
    underRoot.grid_columnconfigure(0, weight=1)
    underRoot.grid_rowconfigure(0, weight=1)

    # ikony użyte do przycisków
    findFileIcon = ttk.PhotoImage(file='PepperHouse/outline_find_in_page_white_24dp.png')
    pepperHouse = ttk.PhotoImage(file='PepperHouse/avatarPepper.png')
    pepperHouse = pepperHouse.subsample(2)
    kingdomElblag = ttk.PhotoImage(file='KingdomElblag/zdjecia/logo.png')
    cargos = ttk.PhotoImage(file='Cargos/avatarCargos.png')
    cargos = cargos.subsample(2)
    biuro4 = ttk.PhotoImage(file='WGN/wgn-biale.png')
    biuro4 = biuro4.subsample(2)
    elFactor = ttk.PhotoImage(file='ELFACTOR/avatarElfactor.png')
    elFactor = elFactor.subsample(2)

    textContainer = ttk.Frame(underRoot)
    textContainer.grid(column=0, row=0, sticky='nswe', pady=5)
    textContainer.grid_columnconfigure(0, weight=1)
    textContainer.grid_rowconfigure(0, weight=1)
    textContainer.grid_rowconfigure(1, weight=1)
    label1 = ttk.Label(textContainer, text='Projekt 2', bootstyle="default", font=(None, 30), anchor='center')
    label1.grid(column=0, row=0, sticky='nswe', padx=5, pady=5)

    officeButtonsContainer = ttk.Frame(textContainer)
    officeButtonsContainer.grid(column=0, row=1, pady=5)
    officeButtonsContainer.grid_rowconfigure(0, weight=1)

    office_1_button = ttk.Button(officeButtonsContainer, image=pepperHouse, bootstyle='light',
                                 command=lambda: handleOfficeButtonClick(office_1_button, 0))
    office_1_button.grid(column=0, row=1, padx=10, pady=20)
    office_2_button = ttk.Button(officeButtonsContainer, image=kingdomElblag, bootstyle='disabled',
                                 command=lambda: handleOfficeButtonClick(office_2_button, 1))
    office_2_button.grid(column=1, row=1, padx=10, pady=20)
    office_3_button = ttk.Button(officeButtonsContainer, image=cargos, bootstyle='disabled',
                                 command=lambda: handleOfficeButtonClick(office_3_button, 2))
    office_3_button.grid(column=2, row=1, padx=10, pady=20)
    office_4_button = ttk.Button(officeButtonsContainer, image=biuro4, bootstyle='disabled',
                                 command=lambda: handleOfficeButtonClick(office_4_button, 3))
    office_4_button.grid(column=3, row=1, padx=10, pady=20)
    office_5_button = ttk.Button(officeButtonsContainer, image=elFactor, bootstyle='disabled',
                                 command=lambda: handleOfficeButtonClick(office_5_button, 4))
    office_5_button.grid(column=4, row=1, padx=10, pady=20)
    global officeButton
    officeButton = [office_1_button, office_2_button, office_3_button, office_4_button, office_5_button]

    frame = ttk.Frame(underRoot)
    frame.grid(column=0, row=1, sticky='nswe', padx=5, pady=5)
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_columnconfigure(3, weight=0)

    def PobierzIPrzeanalizuj(progress, labelDownload):
        indeksAktywnegoBiura = [item for item, biuro in enumerate(wybraneBiuro) if biuro]
        match indeksAktywnegoBiura[0]:
            case 0:
                # PepperHouse
                PepperHouse(1, progress, labelDownload)
                PepperHouse(2, progress, labelDownload)
            case 1:
                # Kingdom Elblag
                print("Kingdom Elblag")
            case 2:
                # Cargos
                Cargos(1, progress, labelDownload)
                # print("Cargos")
            case 3:
                # biuro 4
                WGN.downloadOfertas(3, progress, labelDownload)
            case 4:
                Elfactor.pobierz_aktualna_oferte()
                print("Oferta elfactor")

    def manageStateDownload():
        threadDownload = threading.Thread(target=PobierzIPrzeanalizuj, args=(progress, labelDownload))
        threadDownload.start()

    b1 = ttk.Button(frame, text="Przeanalizuj oferty biura", bootstyle="info-outline",
                    command=lambda: manageStateDownload())
    b1.grid(column=0, row=0, sticky='nswe', padx=5, pady=5)
    progress = ttk.Progressbar(frame, orient=ttk.HORIZONTAL, bootstyle="info-info", length=100, mode='determinate')
    labelDownload = ttk.Label(frame, text='Pobieranie...', bootstyle="info", font=(None, 10))

    def manageStateJoin():
        threadJoin = threading.Thread(target=scal)
        threadJoin.start()

    def scal():
        if not os.path.exists(nazwaPolaczonegoPliku):
            with open(f'{nazwaPolaczonegoPliku}', 'w', encoding='utf-8', newline='') as file:
                print("Nowy plik csv")
        for nazwaPliku in nazwyPrzeanalizowanychPlikow:
            if os.path.exists(nazwaPliku):
                PepperHouse_LaczarkaPlikow.LaczarkaPlikow(
                    nazwa1=nazwaPliku,
                    nazwa2=nazwaPolaczonegoPliku, nazwaPolaczenia=nazwaPolaczonegoPliku)
            else:
                print(f"Nie można znaleźć pliku {nazwaPliku}")
        readOffersFromCSV()

    b4 = ttk.Button(frame, text="Scal oferty wszystkich biur", bootstyle="primary", command=lambda: manageStateJoin())
    b4.grid(column=0, row=8, columnspan=3, sticky='nswe', padx=5, pady=5)

    # oferty po prawej stronie aplikacji
    offers_frame = ttk.Frame(root)
    offers_frame.grid(column=1, row=0, sticky="nswe", padx=5, pady=5)

    def sortOffers():
        global offersToShow
        hold_tmp = offersToShow.pop(0)

        # To jakby się chciało zrobić dynamiczne dodawanie sorterów, ale trochę spowalnia ładowanie
        # ids = []
        # for sorter in sortNazwy:
        #     try:
        #         ids.append(hold_tmp.index(sorter.replace(" ", "_").lower()))
        #     except:
        #         ids.append(17)
        #
        # def sort_key(offer):
        #     match wybranySort:
        #         case 2:
        #             return offer[27] if offer[27] != -1 else offer[26]
        #         case _:
        #             return offer[ids[wybranySort]]

        def sort_key(offer):
            match wybranySort:
                case 1:
                    return offer[2]
                case 2:
                    return offer[27] if offer[27] != -1 else offer[26]
                case 3:
                    return offer[21]
                case _:
                    return offer[17]

        reverse = sorty[wybranySort] == 1
        offersToShow.sort(key=sort_key, reverse=reverse)
        offersToShow.insert(0, hold_tmp)

    def handleSortButtonClick(bujton: ttk.Button, indeks: int):
        global wybranySort
        prefix: str = sortNazwy[indeks]
        for nr, button in enumerate(sortButtonsList):
            if nr == indeks:
                wybranySort = indeks
                match sorty[indeks]:
                    case 1:
                        button.configure(text=f"{prefix} ASC", bootstyle="secondary")
                        sorty[indeks] = 2
                    case _:
                        button.configure(text=f"{prefix} DESC", bootstyle="primary")
                        sorty[indeks] = 1

                    # case 2:
                    #     button.configure(text=f"{prefix}", bootstyle="info-outline")
                    #     for counter in range(0, len(sorty)):
                    #         if counter == indeks:
                    #             sorty[counter] = 0
                    #     wybranySort = 0
            else:
                sorty[nr] = 0
                button.configure(text=f"{str(sortNazwy[nr])}", bootstyle="info-outline")
        showOffers()

    filtry_menu = Toplevel(root)
    filtry_menu.withdraw()
    def handleFiltrButtonClick():
        global offersToShow, filtry_menu
        try:
            filtry_menu.deiconify()
        except:
            filtry_menu = Toplevel(root)
            filtry_menu.title(f"Ustaw filtry")
            filtry_menu.geometry("450x560")
            filtry_menu.minsize(450, 420)
            filtry_menu.deiconify()

            filtersValuesFrame = ttk.Frame(filtry_menu)
            filtersValuesFrame.pack(fill=ttk.BOTH, pady=15, padx=15)

            filtryLista = ["Cena", "Typ", "Liczba pomieszczen", "Typ Transakcji", "Liczba pieter"]
            filtryChecked = [ttk.StringVar(), ttk.StringVar(), ttk.StringVar(), ttk.StringVar(), ttk.StringVar(), ttk.StringVar()]

            _indexFilter = 0
            _ids = 0
            for filterItem in filtryLista:
                filtersValuesFrame.columnconfigure(_indexFilter + 1, weight=1)
                check = ttk.Checkbutton(filtersValuesFrame, name=filterItem.lower(), variable=filtryChecked[_ids], onvalue=True, offvalue=False)
                check.grid(column=0, row=_indexFilter, sticky=ttk.EW, padx=5, ipady=10)
                label = ttk.Label(filtersValuesFrame, text=f"{filterItem}", bootstyle="info", width=20)
                label.grid(column=0, row=_indexFilter, sticky=ttk.EW, padx=30, ipady=10)
                spacer = ttk.Label(filtersValuesFrame, text="")
                spacer.grid(column=0, row=_indexFilter + 1, sticky=ttk.EW, columnspan=4, ipady=10)
                _ids += 1
                _indexFilter += 2

            _indexFilter = 0
            cenaMin = ttk.Entry(filtersValuesFrame, width=5)
            cenaMin.grid(column=1, row=_indexFilter, sticky=ttk.NSEW, padx=5, ipady=10)
            cenaSpace = ttk.Label(filtersValuesFrame, text=" DO ")
            cenaSpace.grid(column=2, row=_indexFilter, sticky=ttk.N, padx=10, ipady=14)
            cenaMax = ttk.Entry(filtersValuesFrame, width=5)
            cenaMax.grid(column=3, row=_indexFilter, sticky=ttk.NSEW, padx=5, ipady=10)
            _indexFilter += 2

            typ_box = ttk.Combobox(filtersValuesFrame, values=["Dom wolnostojący", "Mieszkanie", "Lokal użytkowy", "Inne"])
            typ_box.grid(column=1, row=_indexFilter, sticky=ttk.NSEW, padx=5, pady=2, columnspan=3)
            typ_box.current(1)
            _indexFilter += 2

            liczbaPokoiMin = ttk.Entry(filtersValuesFrame, width=5)
            liczbaPokoiMin.grid(column=1, row=_indexFilter, sticky=ttk.NSEW, padx=5, ipady=10)
            pokojeSpace = ttk.Label(filtersValuesFrame, text=" DO ")
            pokojeSpace.grid(column=2, row=_indexFilter, sticky=ttk.N, padx=10, ipady=14)
            liczbaPokoiMax = ttk.Entry(filtersValuesFrame, width=5)
            liczbaPokoiMax.grid(column=3, row=_indexFilter, sticky=ttk.NSEW, padx=5, ipady=10)
            _indexFilter += 2

            typ_transakcji_box = ttk.Combobox(filtersValuesFrame, values=["Sprzedaż", "Wynajem", "Inne"])
            typ_transakcji_box.grid(column=1, row=_indexFilter, sticky=ttk.NSEW, padx=5, pady=2, columnspan=3)
            typ_transakcji_box.current(1)
            _indexFilter += 2

            liczbaPieterMin = ttk.Entry(filtersValuesFrame, width=5)
            liczbaPieterMin.grid(column=1, row=_indexFilter, sticky=ttk.NSEW, padx=5, ipady=10)
            pietraSpace = ttk.Label(filtersValuesFrame, text=" DO ")
            pietraSpace.grid(column=2, row=_indexFilter, sticky=ttk.N, padx=10, ipady=14)
            liczbaPieterMax = ttk.Entry(filtersValuesFrame, width=5)
            liczbaPieterMax.grid(column=3, row=_indexFilter, sticky=ttk.NSEW, padx=5, ipady=10)
            _indexFilter += 2

            def zabijGo():
                # filtry_menu.destroy()
                filtry_menu.withdraw()

            def filtryButton():
                ustawFiltry()

            filtersActionsButtons = ttk.Frame(filtry_menu)
            filtersActionsButtons.pack(fill=ttk.X, side=BOTTOM, pady=10, padx=10)
            saveButton = ttk.Button(filtersActionsButtons, text="Zapisz", command=filtryButton)
            cancelButton = ttk.Button(filtersActionsButtons, text="Anuluj", command=zabijGo)
            saveButton.pack(side=ttk.LEFT, expand=True, fill=ttk.BOTH, padx=5)
            cancelButton.pack(side=ttk.LEFT, expand=True, fill=ttk.BOTH, padx=5)



        def ustawFiltry():
            global offersToShow
            error = False
            bledne = []
            filteringOffers = everyOffer.copy()
            tmp_headers = filteringOffers.pop(0)

            if filtryChecked[0].get() == "1":
                try:
                    minCena = float(cenaMin.get().replace(",", ".").replace(" ",""))
                    maxCena = float(cenaMax.get().replace(",", ".").replace(" ",""))
                    cenaMin.delete(0, 'end')
                    cenaMin.insert(0, ('{:.2f}'.format(minCena)).replace(".",","))
                    cenaMax.delete(0, 'end')
                    cenaMax.insert(0, ('{:.2f}'.format(maxCena)).replace(".",","))
                    if minCena > maxCena:
                        error = True
                        bledne.append("Cena - max<min")
                    filteringOffers = filter(lambda item: (maxCena >= float(str(item[2]).replace(",", ".").replace(" ","")) >= minCena),
                                             filteringOffers)
                except:
                    error = True
                    bledne.append(filtryLista[0])
            if filtryChecked[1].get() == "1":
                try:
                    typ = typ_box.get()
                    if typ != "Inne":
                        filteringOffers = filter(lambda item: str(item[36]).lower() == typ.lower(), filteringOffers)
                    else:

                        filteringOffers = filter(
                            lambda item: str(item[36]).lower() not in ["dom wolnostojący", "mieszkanie", "lokal użytkowy"],
                            filteringOffers)
                except:
                    error = True
                    bledne.append(filtryLista[1])

            if filtryChecked[2].get() == "1":
                try:
                    minPokoi = int(liczbaPokoiMin.get())
                    maxPokoi = int(liczbaPokoiMax.get())
                    liczbaPokoiMin.delete(0, 'end')
                    liczbaPokoiMin.insert(0, str(minPokoi))
                    liczbaPokoiMax.delete(0, 'end')
                    liczbaPokoiMax.insert(0, str(maxPokoi))
                    if minPokoi > maxPokoi:
                        error = True
                        bledne.append("Pomieszczenia - max<min")
                    filteringOffers = filter(lambda item: (maxPokoi >= int(item[12]) >= minPokoi),
                                             filteringOffers)
                except:
                    error = True
                    bledne.append(filtryLista[2])
            if filtryChecked[3].get() == "1":
                try:
                    typ_transakcji = typ_transakcji_box.get()
                    if typ_transakcji != "Inne":
                        filteringOffers = filter(lambda item: str(item[37]).lower() == typ_transakcji.lower(), filteringOffers)
                    else:

                        filteringOffers = filter(
                            lambda item: str(item[37].lower() not in ["sprzedaz", "wynajem"]),
                            filteringOffers)
                except:
                    error = True
                    bledne.append(filtryLista[3])
            if filtryChecked[4].get() == "1":
                try:
                    minPieter = int(liczbaPieterMin.get())
                    maxPieter = int(liczbaPieterMax.get())
                    liczbaPieterMin.delete(0, 'end')
                    liczbaPieterMin.insert(0, str(minPieter))
                    liczbaPieterMax.delete(0, 'end')
                    liczbaPieterMax.insert(0, str(maxPieter))
                    if minPieter > maxPieter:
                        error = True
                        bledne.append("Pietra - max<min")
                    filteringOffers = filter(lambda item: (maxPieter >= int(0 if "".join(re.findall("\[0-9]",item[1])) == '' else "".join(re.findall("\[0-9]",item[1])))>= minPieter),
                                             filteringOffers)
                except:
                    error = True
                    bledne.append(filtryLista[4])
            if error:
                ErrStr = "Błąd w: \n"
                for blad in bledne:
                    ErrStr = ErrStr + blad + "\n"
                messagebox.showerror(title="BŁĄD FILTRÓW!", message=ErrStr)
            else:
                print(len(offersToShow))
                offersToShow = list(filteringOffers)
                offersToShow.insert(0, tmp_headers)
                print(len(offersToShow))
                filtry_menu.withdraw()
                showOffers()




    # guziki sortowania
    sortButtonsList = []
    sortButtonsContainer = ttk.Frame(offers_frame)
    sortButtonsContainer.pack(fill=ttk.BOTH, side=ttk.TOP, pady=10)
    sortButtonsContainer.rowconfigure(0, weight=1)
    sortButtonsContainer.rowconfigure(1, weight=1)
    sortButtonsContainer.columnconfigure(0, weight=0)
    label_sort = ttk.Label(sortButtonsContainer, text="Sortowanie po:")
    label_sort.grid(column=0, row=0, sticky="nse")
    _indexFilter = 0
    for sort in sortNazwy:
        sortButtonsContainer.columnconfigure(_indexFilter + 1, weight=1)
        sortButton = ttk.Button(sortButtonsContainer, text=f"{sort}", bootstyle="info", width=10)
        sortButton.configure(command=lambda bajton=sortButton, id=_indexFilter: handleSortButtonClick(bajton, id))
        sortButton.grid(column=_indexFilter + 1, row=0, sticky="nwse", padx=5, ipady=10)
        sortButtonsList.append(sortButton)
        _indexFilter += 1

    # guzik filtrowania
    sortButtonsContainer.columnconfigure(_indexFilter + 1, weight=1)
    label_filtr = ttk.Label(sortButtonsContainer, text="|")
    label_filtr.grid(column=_indexFilter + 1, row=0)
    filtrButton = ttk.Button(sortButtonsContainer, text=f"FILTRUJ", bootstyle="secondary", width=8)
    filtrButton.configure(command=lambda: handleFiltrButtonClick())
    filtrButton.grid(column=_indexFilter + 2, row=0, sticky="nwse", padx=5, ipady=10)

    offersAmmount = ttk.Label(sortButtonsContainer)
    offersAmmount.grid(column=0, row=1, columnspan=3, sticky="nsw")
    offerCanvas = ttk.Canvas(offers_frame)
    offerCanvas.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=1)
    oferty = ttk.Frame(offerCanvas)
    scrollbarRight = ttk.Scrollbar(offers_frame, orient=ttk.VERTICAL, command=offerCanvas.yview, bootstyle="info")
    scrollbarRight.pack(side=ttk.RIGHT, fill=ttk.Y)
    offerCanvas.configure(yscrollcommand=scrollbarRight.set)
    oferty.bind('<Configure>', lambda event: offerCanvas.configure(scrollregion=offerCanvas.bbox("all")))
    offerCanvas.create_window((0, 0), window=oferty, anchor="nw")

    # to samo co niżej. Pajton lubi gryźć
    zdjeciaSzczegoly = []

    def pokazSzczegolyOferty(indeksOferty: int):
        global everyOffer
        szczegoly = Toplevel(root)
        szczegoly.title(f"Szczegóły oferty nr.{everyOffer[indeksOferty][21]}")
        szczegoly.geometry("600x600")
        szczegoly.minsize(600, 400)

        def zabijGo():
            szczegoly.destroy()

        exitBajton = ttk.Button(szczegoly, text="Zamknij szczegóły", command=zabijGo)
        exitBajton.pack(fill=ttk.X, side=BOTTOM)
        scrollbarLeftSzczegol = ttk.Scrollbar(szczegoly, orient=ttk.VERTICAL, bootstyle="light")
        scrollbarLeftSzczegol.pack(side=ttk.LEFT, fill=ttk.Y)

        panelCanvas = ttk.Canvas(szczegoly)
        panelCanvas.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=1)
        panelWewnetrzny = ttk.Frame(panelCanvas)
        panelWewnetrzny.pack(fill=ttk.BOTH, side=ttk.LEFT, expand=1)
        scrollbarLeftSzczegol.configure(command=panelCanvas.yview)
        panelCanvas.configure(yscrollcommand=scrollbarLeftSzczegol.set)
        panelWewnetrzny.bind('<Configure>', lambda event: panelCanvas.configure(scrollregion=panelCanvas.bbox("all")))
        panelCanvas.create_window((0, 0), window=panelWewnetrzny, anchor="nw")
        panelWewnetrzny.columnconfigure(0, weight=1)
        panelWewnetrzny.columnconfigure(1, weight=1)
        panelWewnetrzny.columnconfigure(2, weight=1)
        panelWewnetrzny.rowconfigure(0, weight=1)
        panelWewnetrzny.rowconfigure(1, weight=1)
        panelWewnetrzny.rowconfigure(2, weight=1)
        panelWewnetrzny.rowconfigure(3, weight=1)

        global zdjeciaSzczegoly
        pobraneInfo = next(os.walk(f"{os.getcwd()}/zdjecia/{everyOffer[indeksOferty][21]}/"), (None, None, []))[2]
        odpowiednieZdjecia = pobraneInfo
        zapisaneIndeks = 0
        if len(pobraneInfo) > 0:
            indeksOdTylu = len(pobraneInfo) - 1
            for nazwa in reversed(pobraneInfo):
                filename, file_extension = os.path.splitext(pobraneInfo[indeksOdTylu])
                if file_extension == ".thumbnail":
                    odpowiednieZdjecia.pop(indeksOdTylu)
                    indeksOdTylu -= 1
                    continue
                indeksOdTylu -= 1
            zdjeciaSzczegoly = [None] * len(odpowiednieZdjecia)
            for nazwa in odpowiednieZdjecia:
                filename, file_extension = os.path.splitext(nazwa)
                if file_extension.lower() == ".jpg":
                    zdjeciaSzczegoly[zapisaneIndeks] = ImageTk.PhotoImage(image=(
                        Image.open(f'{os.getcwd()}/zdjecia/{everyOffer[indeksOferty][21]}/{filename}.jpg')).resize(
                        (200, 150)))
                else:
                    zdjeciaSzczegoly[zapisaneIndeks] = ttk.PhotoImage(
                        image=Image.open(f'{os.getcwd()}/zdjecia/{everyOffer[indeksOferty][21]}/{filename}.png'))
                zapisaneIndeks += 1

        global indeksZmianyZdjecia
        indeksZmianyZdjecia = 0

        def zmienZdjecie(nastepny: bool):
            global indeksZmianyZdjecia
            if nastepny:
                indeksZmianyZdjecia += 1
                if indeksZmianyZdjecia >= len(zdjeciaSzczegoly):
                    indeksZmianyZdjecia = 0
            else:
                indeksZmianyZdjecia -= 1
                if indeksZmianyZdjecia < 0:
                    indeksZmianyZdjecia = len(zdjeciaSzczegoly) - 1
            labelPhotoImage.configure(image=zdjeciaSzczegoly[indeksZmianyZdjecia])

        labelPhotoImage = ttk.Label(panelWewnetrzny)
        labelPhotoImage.grid(column=1, row=0, padx=10, rowspan=2, sticky="")
        if zdjeciaSzczegoly and len(zdjeciaSzczegoly) > 0:
            labelPhotoImage.configure(image=zdjeciaSzczegoly[0])
            if len(zdjeciaSzczegoly) > 1:
                bajtonLeft = ttk.Button(panelWewnetrzny, text="Poprzednie", command=lambda: zmienZdjecie(False))
                bajtonLeft.grid(column=0, row=0, sticky="nse")
                bajtonRight = ttk.Button(panelWewnetrzny, text="Następne", command=lambda: zmienZdjecie(True))
                bajtonRight.grid(column=2, row=0, sticky="nsw")

        #Tabela z info
        row_names = ['balkon', 'budynek_pietra', 'cena', 'cena_za_m2', 'data_dodania_oferty', 'data_skanowania',
        'dojazd', 'dostepny', 'dzielnica', 'email', 'kaucja', 'liczba_lazienek', 'liczba_pomieszczen',
        'liczba_wyswietlen', 'liczba_zdjec', 'link', 'lokale_uzytkowe', 'lokalizacja', 'miejsce_parkingowe',
        'miejscowosc', 'nazwa_biura', 'numer_oferty', 'ogrod', 'opis', 'oplaty', 'pietro', 'piwnica',
        'powierzchnia', 'powierzchnia_dzialki', 'przeznaczenie', 'rok_budowy', 'rynek', 'stan_prawny_dzialki', 'stan_wykonczenia',
        'standard_wykonczenia', 'telefon', 'typ', 'typ_transakcji', 'typ_zabudowy', 'ulica', 'umeblowanie',
        'winda', 'wojewodztwo', 'wystawa_okien', 'zdjecie_glowne', 'zdjecie_glowne_link']

        for x in range(len(row_names)):
            if (x == 23 or x == 44 or x == 45):
                continue
            else:
                temp_dane = everyOffer[indeksOferty][x]
                if (temp_dane == '-1'):
                    temp_dane = 'Brak danych'
                ttk.Label(panelWewnetrzny, text=row_names[x]+' : '+temp_dane).grid(row=x+3, column=1)
        
        lokal = ttk.Label(panelWewnetrzny, text=everyOffer[indeksOferty][17], wraplength=280, justify=ttk.CENTER, anchor="center")
        lokal.grid(column=1,row=2)
        Opis = ttk.Label(panelWewnetrzny, text=everyOffer[indeksOferty][23], wraplength=600, justify=ttk.CENTER, anchor="center",borderwidth=2, relief="groove")
        Opis.grid(column=1, row=len(row_names)+5)

    # oferty
    oferty.columnconfigure(0, weight=1)

    # to musi tutaj być!!!!!!! - python to ścierwo i jego garbage collector usuwa zdjęcia przypisane do label'a jak przypisuje się je w funkcji.
    zdjecia = []

    def readOffersFromCSV():
        global everyOffer, offersToShow
        everyOffer = []
        offersToShow = []
        with open(nazwaPolaczonegoPliku, mode='r', encoding="utf8") as file:
            reader = csv.reader(file)
            rows = []
            for row in reader:
                rows.append(row)
            everyOffer = rows
            offersToShow = rows
        showOffers()

    def showOffers():
        if not (wybranySort == 0 and sorty[0] == 0):
            sortOffers()
        ammount: int = len(offersToShow)
        global zdjecia
        zdjecia = [None] * ammount
        offersAmmount.configure(text=f"Ilość ofert: {ammount}")
        for indeksOferty in range(1, ammount):
            oferty.rowconfigure(indeksOferty, weight=1)
            pojedynczaOferta = ttk.Frame(oferty)
            pojedynczaOferta.grid(column=0, row=indeksOferty, sticky="nswe")
            bajton = ttk.Button(pojedynczaOferta, text=f'Szczegóły\noferty',
                                command=lambda indeks=indeksOferty: pokazSzczegolyOferty(indeksOferty=indeks))
            bajton.grid(column=0, row=0, ipady=5, pady=10, rowspan=2)
            # pobiera zdjecia z folderu zdjecia/ numer oferty /
            plikiZdjec = next(os.walk(f"{os.getcwd()}/zdjecia/{offersToShow[indeksOferty][21]}/"), (None, None, []))[2]
            if len(plikiZdjec) > 0:
                filename, file_extension = os.path.splitext(plikiZdjec[0])
                try:
                    if file_extension == ".jpg" or file_extension == ".JPG":
                        with Image.open(
                                f'{os.getcwd()}/zdjecia/{offersToShow[indeksOferty][21]}/{plikiZdjec[0]}') as im:
                            im.thumbnail((160, 80), Image.ANTIALIAS)
                            im.save(f"{os.getcwd()}/zdjecia/{offersToShow[indeksOferty][21]}/{filename}.thumbnail",
                                    "JPEG")
                except UnidentifiedImageError:
                    if (offersToShow[indeksOferty][20] == "WGN"):
                        filename = "\WGN\wgn.jpg"
                    elif offersToShow[indeksOferty][20] == "Cargos Nieruchomości":
                        filename = "\Cargos/avatarCargos.jpg"
                    else:
                        filename = "\PepperHouse/avatarPepper.jpg"
                    with Image.open(f"{os.getcwd()}{filename}") as im:
                        im.save(f"{os.getcwd()}/zdjecia/{offersToShow[indeksOferty][21]}/{offersToShow[indeksOferty][20]}.jpg", "JPEG")
                        im.thumbnail((160, 80), Image.ANTIALIAS)
                        im.save(f"{os.getcwd()}/zdjecia/{offersToShow[indeksOferty][21]}/{offersToShow[indeksOferty][20]}.jpg.thumbnail", "JPEG")
                try:
                    zdjecia[indeksOferty - 1] = ImageTk.PhotoImage(image=Image.open(
                        f'{os.getcwd()}/zdjecia/{offersToShow[indeksOferty][21]}/{filename}.thumbnail'))
                except:
                    zdjecia[indeksOferty - 1] = ImageTk.PhotoImage(
                        image=Image.open(f'{os.getcwd()}/no_thumbnail.thumbnail'))
                zdjecie = ttk.Label(pojedynczaOferta, image=zdjecia[indeksOferty - 1])
                zdjecie.grid(column=1, row=0, padx=10, rowspan=2, sticky="nswe")
            numerOferty = ttk.Label(pojedynczaOferta, text=f"Nr. oferty: {offersToShow[indeksOferty][21]}")
            numerOferty.grid(column=2, row=0, sticky="nswe", padx=5)
            powierzchniaOferty = ttk.Label(pojedynczaOferta, text=({offersToShow[indeksOferty][
                                                                        27]} != -1 and f"Powierzchnia: {offersToShow[indeksOferty][27]}" or f"Powierzchnia działki: {offersToShow[indeksOferty][26]}") + " m2")
            powierzchniaOferty.grid(column=2, row=1, sticky="nswe", padx=5)
            biuroOferty = ttk.Label(pojedynczaOferta, text=f"Biuro: {offersToShow[indeksOferty][20]}")
            biuroOferty.grid(column=3, row=0, sticky="nswe", padx=5)
            balkonOferty = ttk.Label(pojedynczaOferta, text="Balkon: " + (
                    offersToShow[indeksOferty][20] == "True" and "Posiada" or "Brak"))
            balkonOferty.grid(column=3, row=1, sticky="nswe", padx=5)
            cenaOferty = ttk.Label(pojedynczaOferta, text=f"Cena: {offersToShow[indeksOferty][2]} zł")
            cenaOferty.grid(column=4, row=0, sticky="nswe", padx=5)
            lokalizacjaOferty = ttk.Label(pojedynczaOferta, text=f"Lokalizacja: {offersToShow[indeksOferty][17]}")
            lokalizacjaOferty.grid(column=4, row=1, sticky="nswe", padx=5)

    readOffersFromCSV()
    buttonsContainer = ttk.Frame(underRoot)
    buttonsContainer.grid(column=0, row=2, sticky="nswe")
    buttonsContainer.columnconfigure(0, weight=1)
    buttonsContainer.columnconfigure(1, weight=1)
    buttonsContainer.rowconfigure(0, weight=1)
    bExit = ttk.Button(buttonsContainer, text="Wyłącz aplikacje", bootstyle="danger-outline", command=lambda: exit())
    bExit.grid(column=0, row=0, sticky='nswe', padx=10, pady=10)
    bReload = ttk.Button(buttonsContainer, text="Odśwież liste", bootstyle="info-outline",
                         command=lambda: readOffersFromCSV())
    bReload.grid(column=1, row=0, sticky='nswe', padx=10, pady=10)

    def exit():
        root.destroy()

    root.mainloop()


if __name__ == "__main__":
    projekt02_GUI()
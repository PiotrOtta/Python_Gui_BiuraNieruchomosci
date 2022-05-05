import csv
import os
import threading
from tkinter import BOTTOM, Toplevel, filedialog
from PIL import ImageTk, Image
import ttkbootstrap as ttk
# PepperHouse
import PepperHouse.downloadAllLinks as PepperHouse_DownloadAllLinks
import PepperHouse.laczarkaPlikow as PepperHouse_LaczarkaPlikow
import PepperHouse.parseInfoInLinks as PepperHouse_ParseInfoInLinks
import PepperHouse.porownywarka as PepperHouse_Porownywarka

#Cargos
import Cargos.generateData as Cargos_GenerateData
wybraneBiuro = [True, False, False, False, False]
nazwyPrzeanalizowanychPlikow = ["PepperHouse.csv", ".csv", "Cargos.csv", ".csv", ".csv"]

filtryNazwy = ["Cena", "Powierzchnia", "Balkon", "Coś 2", "Coś 3"]
filtry = [0]*len(filtryNazwy) # 0 - nie bierz pod uwagę, 1 - asc, 2 - desc
nazwaPolaczonegoPliku = "Symbioza.csv"
officeButton = None
everyOffer = []
def handleOfficeButtonClick(button:ttk.Button, indeks:int):
    global wybraneBiuro
    wybraneBiuro = [False, False, False, False, False]
    for officebuttons in officeButton:
        officebuttons.configure(bootstyle="disabled")
    wybraneBiuro[indeks] = not wybraneBiuro[indeks]
    if wybraneBiuro[indeks]:
        button.configure(bootstyle="light")
    else:
        button.configure(bootstyle="disabled")

def handleFilterButtonClick(button:ttk.Button, indeks:int):
    prefix:str = filtryNazwy[indeks]
    match filtry[indeks]:
        case 0:
            button.configure(text=f"{prefix} ASC", bootstyle="secondary")
            filtry[indeks] = 1
        case 1:
            button.configure(text=f"{prefix} DESC", bootstyle="primary")
            filtry[indeks] = 2
        case 2:
            button.configure(text=f"{prefix}", bootstyle="info-outline")
            filtry[indeks] = 0



def PepperHouse(numerOperacji:int = None, progress = None, labelDownload = None):
    match numerOperacji:
        case 1: PepperHouse_DownloadAllLinks.DownloadAllLinks(progress, labelDownload)
        case 2: PepperHouse_ParseInfoInLinks.ParseInfoInLinks(progress, labelDownload)
        case 3: PepperHouse_Porownywarka.Porownywarka(), # to raczej jest useless do tego projektu
        case 4: PepperHouse_LaczarkaPlikow.LaczarkaPlikow()

def Cargos(numerOperacji:int = None, progress = None, labelDownload = None):
    match numerOperacji:
        case 1: Cargos_GenerateData.GenerateData(progress, labelDownload)
        # case 2:
        # case 3:
        # case 4:
absPath:str = os.path.abspath(os.getcwd())
def getFileName(Info:str = ""):
    name:str = filedialog.askopenfilename(
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
    root.minsize(700,400)
    root.title("Projekt 2 - GUI pięciu biur nieruchomości")
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)
    root.grid_rowconfigure(0, weight=1)
    underRoot = ttk.Frame(root)
    underRoot.grid(column=0, row=0, sticky="nswe")
    underRoot.grid_columnconfigure(0, weight=1)
    underRoot.grid_rowconfigure(0, weight=1)

    # ikony użyte do przycisków
    findFileIcon = ttk.PhotoImage(file = 'PepperHouse/outline_find_in_page_white_24dp.png')
    pepperHouse = ttk.PhotoImage(file = 'PepperHouse/avatarPepper.png')
    pepperHouse = pepperHouse.subsample(2)
    kingdomElblag = ttk.PhotoImage(file = 'Kingdom Elblag/zdjecia/logo.png')
    cargos = ttk.PhotoImage(file = 'Cargos/avatarCargos.png')
    cargos = cargos.subsample(2)
    biuro4 = ttk.PhotoImage(file = 'PepperHouse/avatarPepper.png')
    biuro4 = biuro4.subsample(2)
    biuro5 = ttk.PhotoImage(file = 'PepperHouse/avatarPepper.png')
    biuro5 = biuro5.subsample(2)

    textContainer = ttk.Frame(underRoot)
    textContainer.grid(column=0, row=0, sticky='nswe', pady=5)
    textContainer.grid_columnconfigure(0, weight=1)
    textContainer.grid_rowconfigure(0, weight=1)
    textContainer.grid_rowconfigure(1, weight=1)
    label1 = ttk.Label(textContainer, text='Projekt 2', bootstyle="default", font=(None,30), anchor='center')
    label1.grid(column=0, row=0, sticky='nswe', padx=5, pady=5)

    officeButtonsContainer = ttk.Frame(textContainer)
    officeButtonsContainer.grid(column=0, row=1, pady=5)
    officeButtonsContainer.grid_rowconfigure(0, weight=1)

    office_1_button = ttk.Button(officeButtonsContainer, image=pepperHouse, bootstyle='light', command=lambda: handleOfficeButtonClick(office_1_button, 0))
    office_1_button.grid(column=0, row=1, padx=10, pady=20)
    office_2_button = ttk.Button(officeButtonsContainer, image=kingdomElblag, bootstyle='disabled', command=lambda: handleOfficeButtonClick(office_2_button, 1))
    office_2_button.grid(column=1, row=1, padx=10, pady=20)
    office_3_button = ttk.Button(officeButtonsContainer, image=cargos, bootstyle='disabled', command=lambda: handleOfficeButtonClick(office_3_button, 2))
    office_3_button.grid(column=2, row=1, padx=10, pady=20)
    office_4_button = ttk.Button(officeButtonsContainer, image=biuro4, bootstyle='disabled', command=lambda: handleOfficeButtonClick(office_4_button, 3))
    office_4_button.grid(column=3, row=1, padx=10, pady=20)
    office_5_button = ttk.Button(officeButtonsContainer, image=biuro5, bootstyle='disabled', command=lambda: handleOfficeButtonClick(office_5_button, 4))
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
                print("")
            case 4: 
                # biuro 5
                print("")

    def manageStateDownload():
        threadDownload = threading.Thread(target=PobierzIPrzeanalizuj, args=(progress, labelDownload))
        threadDownload.start()

    b1 = ttk.Button(frame, text="Przeanalizuj oferty biura", bootstyle="info-outline", command=lambda: manageStateDownload())
    b1.grid(column=0, row=0, sticky='nswe', padx=5, pady=5)
    progress = ttk.Progressbar(frame, orient=ttk.HORIZONTAL, bootstyle="info-info", length=100, mode='determinate')
    labelDownload = ttk.Label(frame, text='Pobieranie...', bootstyle="info", font=(None,10))

    def manageStateJoin():
        threadJoin = threading.Thread(target=scal)
        threadJoin.start()
    
    def scal():
        if not os.path.exists(nazwaPolaczonegoPliku):
            with open (f'{nazwaPolaczonegoPliku}','w', encoding='utf-8', newline='') as file:
                print("Nowy plik csv")
        for nazwaPliku in nazwyPrzeanalizowanychPlikow:
            if os.path.exists(nazwaPliku):
                PepperHouse_LaczarkaPlikow.LaczarkaPlikow(
                    nazwa1=nazwaPliku, 
                    nazwa2=nazwaPolaczonegoPliku, nazwaPolaczenia=nazwaPolaczonegoPliku)
            else:
                print(f"Nie można znaleźć pliku {nazwaPliku}")
        readOffersFromCSV()

    b4 = ttk.Button(frame, text="Scal oferty wszystkich biur", bootstyle="primary",command=lambda: manageStateJoin())
    b4.grid(column=0, row=8, columnspan=3, sticky='nswe', padx=5, pady=5)

    # oferty po prawej stronie aplikacji
    offers_frame = ttk.Frame(root)
    offers_frame.grid(column=1, row=0, sticky="nswe", padx=5, pady=5)
    # guziki filtrowania
    filterButtonsContainer = ttk.Frame(offers_frame)
    filterButtonsContainer.pack(fill=ttk.BOTH, side=ttk.TOP, pady=10)
    filterButtonsContainer.rowconfigure(0, weight=1)
    filterButtonsContainer.rowconfigure(1, weight=1)
    filterButtonsContainer.columnconfigure(0, weight=0)
    label_filter = ttk.Label(filterButtonsContainer, text="Filtrowanie po:")
    label_filter.grid(column=0, row=0, sticky="nse")
    _indexFilter = 0
    for filtr in filtryNazwy:
        filterButtonsContainer.columnconfigure(_indexFilter+1, weight=1)
        filterButton = ttk.Button(filterButtonsContainer, text=f"{filtr}", bootstyle="info", width=14)
        filterButton.configure(command= lambda bajton = filterButton, id = _indexFilter: handleFilterButtonClick(bajton, id))
        filterButton.grid(column=_indexFilter+1, row=0, sticky="nwse", padx=5, ipady=10)
        _indexFilter += 1
    offersAmmount = ttk.Label(filterButtonsContainer)
    offersAmmount.grid(column=0, row=1, columnspan=3, sticky="nsw")
    offerCanvas = ttk.Canvas(offers_frame)
    offerCanvas.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=1)
    oferty = ttk.Frame(offerCanvas)
    scrollbarRight = ttk.Scrollbar(offers_frame, orient=ttk.VERTICAL, command=offerCanvas.yview, bootstyle="info")
    scrollbarRight.pack(side=ttk.RIGHT, fill=ttk.Y)
    offerCanvas.configure(yscrollcommand=scrollbarRight.set)
    oferty.bind('<Configure>', lambda event: offerCanvas.configure(scrollregion = offerCanvas.bbox("all")))
    offerCanvas.create_window((0,0), window=oferty, anchor="nw")

    # to samo co niżej. Pajton lubi gryźć
    zdjeciaSzczegoly = []
    def pokazSzczegolyOferty(indeksOferty:int):
        global everyOffer
        szczegoly = Toplevel(root)
        szczegoly.title(f"Szczegóły oferty nr.{everyOffer[indeksOferty][21]}")
        szczegoly.geometry("420x600")
        szczegoly.minsize(420,400)

        def zabijGo():
            szczegoly.destroy()
        exitBajton = ttk.Button(szczegoly, text="Zamknij szczegóły", command= zabijGo)
        exitBajton.pack(fill=ttk.X, side=BOTTOM)
        scrollbarLeftSzczegol = ttk.Scrollbar(szczegoly, orient=ttk.VERTICAL, bootstyle="light")
        scrollbarLeftSzczegol.pack(side=ttk.LEFT, fill=ttk.Y)

        panelCanvas = ttk.Canvas(szczegoly)
        panelCanvas.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=1)
        panelWewnetrzny = ttk.Frame(panelCanvas)
        panelWewnetrzny.pack(fill=ttk.BOTH, side=ttk.LEFT, expand=1)
        scrollbarLeftSzczegol.configure(command=panelCanvas.yview)
        panelCanvas.configure(yscrollcommand=scrollbarLeftSzczegol.set)
        panelWewnetrzny.bind('<Configure>', lambda event: panelCanvas.configure(scrollregion = panelCanvas.bbox("all")))
        panelCanvas.create_window((0,0), window=panelWewnetrzny, anchor="nw")
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
        if len(pobraneInfo)>0:
            indeksOdTylu = len(pobraneInfo)-1
            for nazwa in reversed(pobraneInfo):
                filename, file_extension = os.path.splitext(pobraneInfo[indeksOdTylu])
                if file_extension == ".thumbnail":
                    odpowiednieZdjecia.pop(indeksOdTylu)
                    indeksOdTylu -= 1
                    continue
                indeksOdTylu -= 1
            zdjeciaSzczegoly = [None]*len(odpowiednieZdjecia)
            for nazwa in odpowiednieZdjecia:
                filename, file_extension = os.path.splitext(nazwa)
                if file_extension == ".jpg":
                    zdjeciaSzczegoly[zapisaneIndeks] = ImageTk.PhotoImage(image=(Image.open(f'{os.getcwd()}/zdjecia/{everyOffer[indeksOferty][21]}/{filename}.jpg')).resize((200,150)))
                else:
                    zdjeciaSzczegoly[zapisaneIndeks] = ttk.PhotoImage(image=Image.open(f'{os.getcwd()}/zdjecia/{everyOffer[indeksOferty][21]}/{filename}.png'))
                zapisaneIndeks += 1
        
        global indeksZmianyZdjecia
        indeksZmianyZdjecia = 0
        def zmienZdjecie(nastepny:bool):
            global indeksZmianyZdjecia
            if nastepny:
                indeksZmianyZdjecia += 1
                if indeksZmianyZdjecia >= len(zdjeciaSzczegoly):
                    indeksZmianyZdjecia = 0
            else:
                indeksZmianyZdjecia -= 1
                if indeksZmianyZdjecia < 0:
                    indeksZmianyZdjecia = len(zdjeciaSzczegoly)-1
            labelPhotoImage.configure(image=zdjeciaSzczegoly[indeksZmianyZdjecia])

        labelPhotoImage = ttk.Label(panelWewnetrzny)
        labelPhotoImage.grid(column=1, row=0, padx=10, rowspan=2, sticky="nswe")
        if len(zdjeciaSzczegoly)>0:
            labelPhotoImage.configure(image=zdjeciaSzczegoly[0])
            if len(zdjeciaSzczegoly)>1:
                bajtonLeft = ttk.Button(panelWewnetrzny, text="Poprzednie", command= lambda: zmienZdjecie(False))
                bajtonLeft.grid(column=0, row=0, sticky="nse")
                bajtonRight= ttk.Button(panelWewnetrzny, text="Następne", command= lambda: zmienZdjecie(True))
                bajtonRight.grid(column=2, row=0, sticky="nsw")


        lokal = ttk.Label(panelWewnetrzny, text=everyOffer[indeksOferty][17], wraplength=280, justify=ttk.CENTER, anchor="center")
        lokal.grid(column=0, columnspan=3, row=2, sticky="nswe", padx=10, pady=10)
        Opis = ttk.Label(panelWewnetrzny, text=everyOffer[indeksOferty][23], wraplength=280, justify=ttk.CENTER, anchor="center")
        Opis.grid(column=0, columnspan=3, row=3, sticky="nswe", padx=10, pady=10)

    # oferty
    oferty.columnconfigure(0, weight=1)

    # to musi tutaj być!!!!!!! - python to ścierwo i jego garbage collector usuwa zdjęcia przypisane do label'a jak przypisuje się je w funkcji.
    zdjecia = []
    def readOffersFromCSV():
        global everyOffer
        everyOffer = []
        with open(nazwaPolaczonegoPliku, mode='r', encoding="utf8") as file:
            reader = csv.reader(file)
            rows = []
            for row in reader:
                rows.append(row)
            everyOffer = rows
        ammount:int = len(everyOffer)
        global zdjecia
        zdjecia = [None] * ammount
        offersAmmount.configure(text=f"Ilość ofert: {ammount}")
        for indeksOferty in range(1, ammount):
            oferty.rowconfigure(indeksOferty, weight=1)
            pojedynczaOferta = ttk.Frame(oferty)
            pojedynczaOferta.grid(column=0, row=indeksOferty, sticky="nswe")
            bajton = ttk.Button(pojedynczaOferta, text=f'Szczegóły\noferty', command= lambda indeks=indeksOferty: pokazSzczegolyOferty(indeksOferty=indeks))
            bajton.grid(column=0, row=0, ipady=5,pady=10, rowspan=2)
            # pobiera zdjecia z folderu zdjecia/ numer oferty /
            plikiZdjec = next(os.walk(f"{os.getcwd()}/zdjecia/{everyOffer[indeksOferty][21]}/"), (None, None, []))[2]
            if len(plikiZdjec)>0:
                filename, file_extension = os.path.splitext(plikiZdjec[0])
                if file_extension == ".jpg":
                    with Image.open(f'{os.getcwd()}/zdjecia/{everyOffer[indeksOferty][21]}/{plikiZdjec[0]}') as im:
                        im.thumbnail((160,80), Image.ANTIALIAS)
                        im.save(f"{os.getcwd()}/zdjecia/{everyOffer[indeksOferty][21]}/{filename}.thumbnail", "JPEG")
                zdjecia[indeksOferty-1] = ImageTk.PhotoImage(image=Image.open(f'{os.getcwd()}/zdjecia/{everyOffer[indeksOferty][21]}/{filename}.thumbnail'))
                zdjecie = ttk.Label(pojedynczaOferta, image=zdjecia[indeksOferty-1])
                zdjecie.grid(column=1, row=0, padx=10, rowspan=2, sticky="nswe")
            numerOferty = ttk.Label(pojedynczaOferta, text=f"Nr. oferty: {everyOffer[indeksOferty][21]}")
            numerOferty.grid(column=2, row=0, sticky="nswe", padx=5)
            powierzchniaOferty = ttk.Label(pojedynczaOferta, text=({everyOffer[indeksOferty][27]} != -1 and f"Powierzchnia: {everyOffer[indeksOferty][27]}" or f"Powierzchnia działki: {everyOffer[indeksOferty][26]}") + " m2")
            powierzchniaOferty.grid(column=2, row=1, sticky="nswe", padx=5)
            biuroOferty = ttk.Label(pojedynczaOferta, text=f"Biuro: {everyOffer[indeksOferty][20]}")
            biuroOferty.grid(column=3, row=0, sticky="nswe", padx=5)
            balkonOferty = ttk.Label(pojedynczaOferta, text="Balkon: " + (everyOffer[indeksOferty][20] == "True" and "Posiada" or "Brak"))
            balkonOferty.grid(column=3, row=1, sticky="nswe", padx=5)
            cenaOferty = ttk.Label(pojedynczaOferta, text=f"Cena: {everyOffer[indeksOferty][2]} zł")
            cenaOferty.grid(column=4, row=0, sticky="nswe", padx=5)
            lokalizacjaOferty = ttk.Label(pojedynczaOferta, text=f"Lokalizacja: {everyOffer[indeksOferty][17]}")
            lokalizacjaOferty.grid(column=4, row=1, sticky="nswe", padx=5)

    readOffersFromCSV()
    buttonsContainer = ttk.Frame(underRoot)
    buttonsContainer.grid(column=0, row=2, sticky="nswe")
    buttonsContainer.columnconfigure(0, weight=1)
    buttonsContainer.columnconfigure(1, weight=1)
    buttonsContainer.rowconfigure(0, weight=1)
    bExit = ttk.Button(buttonsContainer, text="Wyłącz aplikacje", bootstyle="danger-outline", command=lambda: exit())
    bExit.grid(column=0, row=0, sticky='nswe', padx= 10, pady=10)
    bReload = ttk.Button(buttonsContainer, text="Odśwież liste", bootstyle="info-outline", command=lambda: readOffersFromCSV())
    bReload.grid(column=1, row=0, sticky='nswe', padx= 10, pady=10)

    def exit():
        root.destroy()
    root.mainloop()

if __name__ == "__main__":
    projekt02_GUI()
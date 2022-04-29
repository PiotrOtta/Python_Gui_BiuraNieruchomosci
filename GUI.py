import os
import threading
from tkinter import HORIZONTAL, filedialog
import ttkbootstrap as ttk
from downloadAllLinks import DownloadAllLinks
from laczarkaPlikow import LaczarkaPlikow
from parseInfoInLinks import ParseInfoInLinks
from porownywarka import Porownywarka

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

def projekt01_PiotraOtta18902():
    root = ttk.Window(themename="darkly")
    root.geometry('950x550')
    root.minsize(700,550)
    root.title("Projekt 1 - Piotr Otta 18902")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=0)

    textContainer = ttk.Frame(root)
    textContainer.grid_columnconfigure(0, weight=1)
    textContainer.grid_columnconfigure(1, weight=0)
    textContainer.grid_columnconfigure(2, weight=1)
    textContainer.grid(column=0, row=0, sticky='nswe', pady=5)
    myImage = ttk.PhotoImage(file = 'avatarPepper.png')
    myImage = myImage.subsample(3)
    imgButton = ttk.Button(textContainer, image=myImage, bootstyle='light')
    imgButton.grid(column=0, row=0, sticky='nse', padx=10, pady=20)
    label1 = ttk.Label(textContainer, text='Projekt 1', bootstyle="default", font=(None,30), anchor='e')
    label1.grid(column=1, row=0, sticky='nse', padx=5, pady=5)
    smallContainer = ttk.Frame(textContainer)
    smallContainer.grid_columnconfigure(0, weight=1)
    smallContainer.grid_columnconfigure(1, weight=1)
    smallContainer.grid(column=2, row=0, sticky='we', pady=5)
    label2 = ttk.Label(smallContainer, text='www.pepperhouse.pl', bootstyle="info", font=(None,15), anchor='w')
    label2.grid(column=0, row=0, sticky='nsw')
    label3 = ttk.Label(smallContainer, text='Piotr Otta 18902', bootstyle="danger", font=(None,10), anchor='w')
    label3.grid(column=0, row=1, sticky='nsw')

    frame = ttk.Frame(root)
    frame.grid(column=0, row=1, sticky='nswe', padx=5, pady=5)
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_columnconfigure(3, weight=0)

    def manageStateDownload():
        threadDownload = threading.Thread(target=DownloadAllLinks, args=(progress, labelDownload))
        threadDownload.start()

    b1 = ttk.Button(frame, text="Pobierz linki do pliku CSV", bootstyle="info-outline", command=lambda: manageStateDownload())
    b1.grid(column=0, row=0, sticky='nswe', padx=5, pady=5)
    progress = ttk.Progressbar(frame, orient=HORIZONTAL, bootstyle="info-info", length=100, mode='determinate')
    labelDownload = ttk.Label(frame, text='Pobieranie...', bootstyle="info", font=(None,10))

    def manageStateParse():
        threadParse = threading.Thread(target=ParseInfoInLinks, args=(progressParse, labelParse, labelAfterParse))
        threadParse.start()

    b2 = ttk.Button(frame, text="Przeanalizuj linki", bootstyle="warning-outline",command=lambda: manageStateParse())
    b2.grid(column=0, row=1, sticky='nswe', padx=5, pady=5)
    progressParse = ttk.Progressbar(frame, orient=HORIZONTAL, bootstyle="striped-warning", length=100, mode='determinate')
    labelParse = ttk.Label(frame, text='Analizowanie...', bootstyle="warning", font=(None,10))
    labelAfterParse = ttk.Label(frame, text='', bootstyle="warning", font=(None,10))
    labelAfterParse.grid(column=0, columnspan=3, row=2, sticky='nswe', padx=5, pady=5)

    def manageStateCompare():
        textbox1.configure(bootstyle='light')
        textbox2.configure(bootstyle='light')
        labelAfterCompare.configure(text=f'', bootstyle='light')
        if not textbox1.get() or not textbox2.get():
            if not textbox1.get():
                textbox1.configure(bootstyle='danger')
            if not textbox2.get():
                textbox2.configure(bootstyle='danger')
            return
        threadCompare = threading.Thread(target=Porownywarka, args=(textbox1.get(),textbox2.get(), labelAfterCompare))
        threadCompare.start()
    
    findFileIcon = ttk.PhotoImage(file = 'outline_find_in_page_white_24dp.png')

    b3 = ttk.Button(frame, text="Porównaj dwa pliki", bootstyle="light-outline",command=lambda: manageStateCompare())
    b3.grid(column=0, row=3, sticky='nswe', rowspan=2, padx=5, pady=5)
    ttk.Label(frame, text='Nazwa pierwszego arkusza:', bootstyle="light", font=(None,10)).grid(column=1, row=3, sticky='nswe', padx=5, pady=5)
    ttk.Label(frame, text='Nazwa drugiego arkusza:', bootstyle="light", font=(None,10)).grid(column=2, row=3, sticky='nswe', padx=5, pady=5)
    string1 = ttk.StringVar()
    string2 = ttk.StringVar()
    rowFrame1 = ttk.Frame(frame)
    rowFrame1.grid(column=1, row=4, sticky='nswe', padx=5, pady=5)
    rowFrame1.rowconfigure(0, weight=1)
    rowFrame1.columnconfigure(0, weight=1)
    rowFrame1.columnconfigure(1, weight=0)
    textbox1 = ttk.Entry(rowFrame1, textvariable=string1, bootstyle='light')
    textbox1.grid(column=0, row=0, sticky='nswe')
    ttk.Button(rowFrame1, image=findFileIcon, bootstyle="light-outline",command=lambda: string1.set(getFileName())).grid(column=1, row=0, sticky='nswe')
    rowFrame2 = ttk.Frame(frame)
    rowFrame2.grid(column=2, row=4, sticky='nswe', padx=5, pady=5)
    rowFrame2.rowconfigure(0, weight=1)
    rowFrame2.columnconfigure(0, weight=1)
    rowFrame2.columnconfigure(1, weight=0)
    textbox2 = ttk.Entry(rowFrame2, textvariable=string2, bootstyle='light')
    textbox2.grid(column=0, row=0, sticky='nswe')
    ttk.Button(rowFrame2, image=findFileIcon, bootstyle="light-outline",command=lambda: string2.set(getFileName())).grid(column=1, row=0, sticky='nswe')
    labelAfterCompare = ttk.Label(frame, text='', bootstyle="light", font=(None,10))
    labelAfterCompare.grid(column=0, columnspan=3, row=5, sticky='nswe', padx=5, pady=5)

    def manageStateJoin():
        textbox3.configure(bootstyle='light')
        textbox4.configure(bootstyle='light')
        textbox5.configure(bootstyle='light')
        labelAfterJoin.configure(text=f'', bootstyle='primary')
        if not textbox3.get() or not textbox4.get() or not textbox5.get():
            if not textbox3.get():
                textbox3.configure(bootstyle='danger')
            if not textbox4.get():
                textbox4.configure(bootstyle='danger')
            if not textbox5.get():
                textbox5.configure(bootstyle='danger')
            return
        threadJoin = threading.Thread(target=LaczarkaPlikow, args=(textbox3.get(),textbox4.get(), textbox5.get(),labelAfterJoin))
        threadJoin.start()

    b4 = ttk.Button(frame, text="Połącz dwa arkusze", bootstyle="primary",command=lambda: manageStateJoin())
    b4.grid(column=0, row=8, columnspan=3, sticky='nswe', padx=5, pady=5)
    ttk.Label(frame, text='Nazwa pierwszego arkusza:', bootstyle="light", font=(None,10)).grid(column=0, row=6, sticky='nswe', padx=5, pady=5)
    ttk.Label(frame, text='Nazwa drugiego arkusza:', bootstyle="light", font=(None,10)).grid(column=1, row=6, sticky='nswe', padx=5, pady=5)
    ttk.Label(frame, text='Nazwa połączonego arkusza:', bootstyle="light", font=(None,10)).grid(column=2, row=6, sticky='nswe', padx=5, pady=5)
    string3 = ttk.StringVar()
    string4 = ttk.StringVar()
    string5 = ttk.StringVar()
    rowFrame3 = ttk.Frame(frame)
    rowFrame3.grid(column=0, row=7, sticky='nswe', padx=5, pady=5)
    rowFrame3.rowconfigure(0, weight=1)
    rowFrame3.columnconfigure(0, weight=1)
    rowFrame3.columnconfigure(1, weight=0)
    textbox3 = ttk.Entry(rowFrame3, textvariable=string3, bootstyle='light')
    textbox3.grid(column=0, row=0, sticky='nswe')
    ttk.Button(rowFrame3, image=findFileIcon, bootstyle="light-outline",command=lambda: string3.set(getFileName())).grid(column=1, row=0, sticky='nswe')
    rowFrame4 = ttk.Frame(frame)
    rowFrame4.grid(column=1, row=7, sticky='nswe', padx=5, pady=5)
    rowFrame4.rowconfigure(0, weight=1)
    rowFrame4.columnconfigure(0, weight=1)
    rowFrame4.columnconfigure(1, weight=0)
    textbox4 = ttk.Entry(rowFrame4, textvariable=string4, bootstyle='light')
    textbox4.grid(column=0, row=0, sticky='nswe')
    ttk.Button(rowFrame4, image=findFileIcon, bootstyle="light-outline",command=lambda: string4.set(getFileName())).grid(column=1, row=0, sticky='nswe')
    rowFrame5 = ttk.Frame(frame)
    rowFrame5.grid(column=2, row=7, sticky='nswe', padx=5, pady=5)
    rowFrame5.rowconfigure(0, weight=1)
    rowFrame5.columnconfigure(0, weight=1)
    rowFrame5.columnconfigure(1, weight=0)
    textbox5 = ttk.Entry(rowFrame5, textvariable=string5, bootstyle='light')
    textbox5.grid(column=0, row=0, sticky='nswe')
    ttk.Button(rowFrame5, image=findFileIcon, bootstyle="light-outline",command=lambda: string5.set(getFileName())).grid(column=1, row=0, sticky='nswe')
    labelAfterJoin = ttk.Label(frame, text='', bootstyle="primary", font=(None,10))
    labelAfterJoin.grid(column=0, columnspan=3, row=9, sticky='nswe', padx=5, pady=5)

    bExit = ttk.Button(root, text="Wyłącz aplikacje", bootstyle="danger-outline", command=lambda: exit())
    bExit.grid(column=0, row=2, sticky='nswe', padx= 10, pady=10)
    def exit():
        root.destroy()
    root.mainloop()

if __name__ == "__main__":
    projekt01_PiotraOtta18902()
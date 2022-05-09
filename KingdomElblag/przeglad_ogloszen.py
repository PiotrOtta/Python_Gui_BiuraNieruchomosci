import random
import tkinter as tk
from bs4 import BeautifulSoup
from urllib import request
import numpy as np
import re
import datetime
import requests
import csv
from PIL import ImageTk,Image

master = tk.Tk()
master.title('Przeglad')
master.geometry("1000x800")





def wyswietlOferte(id,info):
    newWindow = tk.Toplevel(master)
    newWindow.title("Oferta "+str(id))
    newWindow.geometry("800x500")
    label = tk.Label(newWindow,text=info['numer oferty'])
    label.pack()

tab = []
tab_all = []
with open('Kingdom Elblag/final.csv', "rt", encoding="utf-8", newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        temp = row['nazwa_biura']+" | Oferta numer: " + row['numer oferty'] + ", Lokalizacja: "+row['lokalizacja']+", Typ: "+row['typ']+",cena: " + row['cena'] + ", ZDJECIE" + row['zdjecie_glowne']
        tab.append(temp)
        tab_all.append(row)


canvas = tk.Canvas(master)
scroll_y = tk.Scrollbar(master, orient="vertical", command=canvas.yview)

frame = tk.Frame(canvas)
for i in range(len(tab)):
    x = tab_all[i]
    label = tk.Label(frame, text=tab[i])
    button = tk.Button(frame, text='Pokaż ofertę', width=25, command=lambda i=i, x=x:wyswietlOferte(i,x))
    label.pack()
    button.pack()

canvas.create_window(0, 0, anchor='nw', window=frame)
canvas.update_idletasks()

canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)
                 
canvas.pack(fill='both', expand=True, side='left')
scroll_y.pack(fill='y', side='right')

master.mainloop()
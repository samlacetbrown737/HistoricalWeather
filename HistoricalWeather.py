# Load libraries
import pandas
from datetime import datetime
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import numpy
import tkinter as tk
from tkinter import ttk
from tkmacosx import Button
from PIL import ImageTk,Image
display = tk.Tk()
display.geometry('210x130')
display.title("Date Selection")
names = ['station', 'name', 'date', 'wind', 'rain', 'snow', 'avg_temp', 'max_temp', 'min_temp']
dataset = pandas.read_csv("stations.csv", skiprows=1, names=names)

seattleRow = 0;
bostonRow = 0;
alaskaRow = 0;

selectedDay = 0;

def get_date():
    switcher = {
        "January": "1",
        "February": "2",
        "March": "3",
        "April": "4",
        "May": "5",
        "June": "6",
        "July": "7",
        "August": "8",
        "September": "9",
        "October": "10",
        "November": "11",
        "December": "12"
    }
    monthNum = switcher.get(monthVar.get(), "Invalid month")
    selectedDay = monthNum + "/" + dayVar.get() + "/"+ yearVar.get()
    notValidDate = False
    try:
        datetime.strptime(selectedDay, '%m/%d/%Y')
    except ValueError:
        notValidDate = True
    if(notValidDate):
        get_date()
    else:
        date_format = "%m/%d/%Y"
        a = datetime.strptime('04/03/2003', date_format)
        b = datetime.strptime(selectedDay, date_format)
        delta = b - a
        alaskaRow = delta.days
        if(alaskaRow < 0):
            selectedDay = "04/03/2003"
            alaskaRow = 0
            print("Date must be after 04/02/2003: ")     
        seattleRow = alaskaRow + 5970
        bostonRow = seattleRow + 5970
    print("Results for " + selectedDay)
    print("Seattle")
    show_results(seattleRow, "SEATTLE", "deepskyblue3", "Seattle", selectedDay,"27")
    print()
    print("Boston")
    show_results(bostonRow, "BOSTON", "firebrick3", "Boston", selectedDay,"347")
    print()
    print("Fairbanks")
    show_results(alaskaRow, "FAIRBANKS", "green4", "Fairbanks", selectedDay,"667")

def get_avg_temp(date):
    if(numpy.isnan(dataset['avg_temp'][date])):
        return ((dataset['max_temp'][date] + dataset['min_temp'][date])/2)
    else:
        return dataset['avg_temp'][date]

def get_max_temp(date):
    return dataset['max_temp'][date]

def get_min_temp(date):
    return dataset['min_temp'][date]

def get_rain(date):
    return dataset['rain'][date]

def get_snow(date):
    if(numpy.isnan(dataset['snow'][date])):
        return 0
    else:
        return dataset['snow'][date]

def get_wind(date):
    return dataset['wind'][date]

dayText = tk.Label(display, text="Day: ")
dayText.grid(row=1, column=1, pady=(7,0))
dayVar = tk.StringVar(display)
dayVar.set("1")
dayPicker = tk.OptionMenu(display, dayVar, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
dayPicker.config(width=10)
dayPicker.grid(row=1, column=2, pady=(10,0))
monthText = tk.Label(display, text="Month: ")
monthText.grid(row=2, column=1)
monthVar = tk.StringVar(display)
monthVar.set("January")
monthPicker = tk.OptionMenu(display, monthVar, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
monthPicker.config(width=10)
monthPicker.grid(row=2, column=2)
yearText = tk.Label(display, text="Year: ")
yearText.grid(row=3,column=1)
yearVar = tk.StringVar(display)
yearVar.set("2003")
yearPicker = tk.OptionMenu(display, yearVar, "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019")
yearPicker.config(width=10)
yearPicker.grid(row=3, column=2)
setDate = Button(display, text="DONE", command=get_date, bg="black", fg="white", padx=5, pady=5, borderless=1)
setDate.grid(row=4,column=1, columnspan=2, pady=(10,0))
def change_date(*args):
    return (dayVar.get() + " " + monthVar.get() + ", " + yearVar.get());
dayVar.trace('w', change_date)
monthVar.trace('w', change_date)
yearVar.trace('w', change_date)
def show_results(row, label, color, results, day,move):
    print("Avg. Temperature: " + str(get_avg_temp(row)))
    print("Avg. Wind Speed: " + str(get_wind(row)))
    print("Total Precipitation: " + str(get_rain(row)))
    print("Snow On Ground: " + str(get_snow(row)))
    resultsTitle = results + " Weather For " + day
    results = tk.Tk()
    results.title(resultsTitle)
    results.geometry('280x150+'+move+'+250')
    results.configure(background=color)
    #cityText = tk.Label(results, text=label, bg=color, fg="white", font=("Times New Roman", 48), anchor="center")
    #cityText.grid(row=5, columnspan=2)
    tempText = tk.Label(results, text="Avg. Temperature: ", bg=color, fg="white", font=("Times New Roman", 24))
    tempText.grid(row=1, column=1, sticky='W', padx=(10,0), pady=(6,0))
    tempNumText = tk.Label(results, text=str(get_avg_temp(row)), bg=color, fg="white", font=("Times New Roman", 24))
    tempNumText.grid(row=1, column=2, pady=(6,0))
    windText = tk.Label(results, text="Avg. Wind Speed: ", bg=color, fg="white", font=("Times New Roman", 24))
    windText.grid(row=2, column=1, sticky='W', padx=(10,0))
    windNumText = tk.Label(results, text=str(get_wind(row)), bg=color, fg="white", font=("Times New Roman", 24))
    windNumText.grid(row=2, column=2)
    rainText = tk.Label(results, text="Total Precipitation: ", bg=color, fg="white", font=("Times New Roman", 24))
    rainText.grid(row=3, column=1, sticky='W', padx=(10,0))
    rainNumText = tk.Label(results, text=str(get_rain(row)), bg=color, fg="white", font=("Times New Roman", 24))
    rainNumText.grid(row=3, column=2)
    snowText = tk.Label(results, text="Snow On Ground: ", bg=color, fg="white", font=("Times New Roman", 24))
    snowText.grid(row=4, column=1, sticky='W', padx=(10,0))
    snowNumText = tk.Label(results, text=str(get_snow(row)), bg=color, fg="white", font=("Times New Roman", 24))
    snowNumText.grid(row=4, column=2)
    menubar = tk.Menu(results)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=display.destroy)
    menubar.add_cascade(label="File", menu=filemenu)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help", command=showHelp)
    helpmenu.add_command(label="About...", command=showAbout)
    menubar.add_cascade(label="Help", menu=helpmenu)
    results.config(menu=menubar)
    
def showHelp():
    x = 0;
def showAbout():
    x = 0;
menubar = tk.Menu(display)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=display.destroy)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=showHelp)
helpmenu.add_command(label="About...", command=showAbout)
menubar.add_cascade(label="Help", menu=helpmenu)
display.config(menu=menubar)
display.mainloop() 



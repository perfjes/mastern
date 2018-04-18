from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog

import os

from compute.modules import classifier, regressor, dataset


# GUI class for users to interact with the program
file = ['df.csv']
dtc = classifier
dtr = regressor


app = Tk()
app.title('Bongo')
app.geometry('800x400')


def regclicked():
    res = dtr.regress(file[0])
    output.insert(INSERT, res)
    n = '\n' '\n'
    output.insert(INSERT, n, n)
    print(file)


def clasclicked():
    res = dtc.classify(file[0])
    output.insert(INSERT, res)
    n = '\n' '\n'
    output.insert(INSERT, n, n)


def clearoutput():
    output.delete(1.0, END)


def loadfile():
    path = filedialog.askopenfilename(parent=app,
                                    initialdir=os.getcwd(),
                                    title="Please select a file:",
                                    filetypes=(('CSV files', '.csv'), ('All files', '*.*')))
    pathlist = path.split("/")
    file[0] = pathlist[(len(pathlist)-1)]


# ---------- LABELS ----------
welcomelabel = Label(app, text='Which function do you want to perform')
output = scrolledtext.ScrolledText(app, width=60, height=20)
output.grid(column=0, row=0)


# ---------- BUTTONS ----------
regressionBTN = Button(app, text='Regression', command=regclicked)
regressionBTN.grid(column=1, row=0)


classifierBTN = Button(app, text='Classification', command=clasclicked)
classifierBTN.grid(column=1, row=1)


clearoutputBTN = Button(app, text='Clear output field', command=clearoutput)
clearoutputBTN.grid(column=1, row=2)


loadfileBTN = Button(app, text='Load dataset CSV', command=loadfile)
loadfileBTN.grid(column=2, row=0)

app.mainloop()
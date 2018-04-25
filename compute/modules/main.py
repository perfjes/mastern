from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog

import os

from compute.modules import classifier, regressor, dataset

# GUI class for users to interact with the program
file = ['df.csv'] #file variable as list to enable mutation
dtc = classifier
dtr = regressor

app = Tk()
app.title('Bongo')
app.geometry('1200x900')


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
    if(pathlist[(len(pathlist)-1)].lower().endswith('.csv')):
        file[0] = pathlist[(len(pathlist)-1)]
        output.insert(INSERT, 'File ' + file[0] + ' loaded', '\n', '\n')
    else:
        output.insert(INSERT, 'Wrong filetype - Please select a CSV file', '\n', '\n')


def printdataset():
    output.insert(INSERT, dataset.loaddataframe(file[0]).to_string())


def saveasnew():
    data = dataset.loaddataframe(file[0])
    message = dataset.saveasnew(data)
    output.insert(INSERT, 'Saved file as: ' + message)


# ---------- LABELS ----------
welcomelabel = Label(app, text='Which function do you want to perform')
welcomelabel.grid(column=0, row=0)

# ---------- OUTPUT -----------
output = scrolledtext.ScrolledText(app, width=110, height=50)
output.grid(column=3, row=5)


# ---------- BUTTONS ----------
regressionBTN = Button(app, text='Regression', command=regclicked)
regressionBTN.grid(column=0, row=1)


classifierBTN = Button(app, text='Classification', command=clasclicked)
classifierBTN.grid(column=0, row=2)


clearoutputBTN = Button(app, text='Clear output field', command=clearoutput)
clearoutputBTN.grid(column=2, row=3)


loadfileBTN = Button(app, text='Load dataset CSV', command=loadfile)
loadfileBTN.grid(column=2, row=1)


savenewfileBTN = Button(app, text='Save dataset as new', command=saveasnew)
savenewfileBTN.grid(column=2, row=2)


printdataBTN = Button(app, text='Print dataset', command=printdataset)
printdataBTN.grid(column=1, row=1)


app.mainloop()

from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog

import os

from compute.modules import classifier, regressor, dataset

# GUI class for users to interact with the program
# file variable as list to enable mutation
file = ['df.csv']
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
    if pathlist[(len(pathlist) - 1)].lower().endswith('.csv'):
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


# Test methods for quick testing
def mregtest():
    mean = list()
    for i in range(20):
        regclicked()
        

def mclastest():
    for i in range(20):
        clasclicked()


# ---------- LABELS ----------
# welcomelabel = Label(app, text='I\'m afraid I can\'t do that, Dave')
# welcomelabel.grid(column=0, row=0)

# ---------- OUTPUT -----------
output = scrolledtext.ScrolledText(app, width=110, height=50)
output.grid(column=3, row=0)


# ---------- BUTTONS ----------
buttonframe = Frame(app)
massiveregtest = Button(buttonframe, text="Regress 20", command=mregtest)
massiveregtest.pack(padx=10, pady=10)

massiveclastest = Button(buttonframe, text="Classify 20", command=mclastest)
massiveclastest.pack(padx=10, pady=10)

regressionBTN = Button(buttonframe, text='Regression', command=regclicked)
regressionBTN.pack(padx=5, pady=5)


classifierBTN = Button(buttonframe, text='Classification', command=clasclicked)
classifierBTN.pack(padx=5, pady=15)


clearoutputBTN = Button(buttonframe, text='Clear output field', command=clearoutput)
clearoutputBTN.pack(padx=5, pady=15)


loadfileBTN = Button(buttonframe, text='Load dataset CSV', command=loadfile)
loadfileBTN.pack(padx=5, pady=5)


savenewfileBTN = Button(buttonframe, text='Save dataset as new', command=saveasnew)
savenewfileBTN.pack(padx=5, pady=15)


printdataBTN = Button(buttonframe, text='Print dataset', command=printdataset)
printdataBTN.pack(padx=5, pady=5)

buttonframe.grid(column='0', row='0')

app.mainloop()

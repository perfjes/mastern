from tkinter import *
from tkinter import scrolledtext
from compute.modules import classifier, regressor, dataset


# GUI class for users to interact with the program

dtc = classifier
dtr = regressor


app = Tk()
app.title('Bongo')
app.geometry('600x400')


def regclicked():
    res = dtr.regress()
    output.insert(INSERT, res)
    n = '\n' '\n'
    output.insert(INSERT, n, n)


def clasclicked():
    res = dtc.classify()
    output.insert(INSERT, res)
    n = '\n' '\n'
    output.insert(INSERT, n, n)

def clearoutput():
    output.delete(1.0, END)


# ---------- LABELS ----------
welcomelabel = Label(app, text='Which function do you want to perform')
output = scrolledtext.ScrolledText(app, width=40, height=20)
output.grid(column=0, row=0)


# ---------- BUTTONS ----------
regressionBTN = Button(app, text='Regression', command=regclicked)
regressionBTN.grid(column=1, row=0)


classifierBTN = Button(app, text='Classification', command=clasclicked)
classifierBTN.grid(column=1, row=1)


clearoutputBTN = Button(app, text='Clear output field', command=clearoutput)
clearoutputBTN.grid(column=1, row=2)


app.mainloop()
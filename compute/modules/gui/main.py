from tkinter import *
from tkinter import scrolledtext, simpledialog
from tkinter import filedialog
from compute.modules import datahandler
from compute.modules.ml import classifier, regressor
import os


# System modules abbreviated for simplicity
dtc = classifier
dtr = regressor
dth = datahandler

# GUI-related variables
app = Tk()
app.title('Bongo')
app.geometry('1200x900')


# Ask for the user to input their desired split, where the input defines the test set size.
# The greater the test set the less the training set, and vice versa.
def askforsplit():
    answer = simpledialog.askfloat("Input", "Which percentage of \n the dataset will be \n used for testing? \n "
                                            "Please input a value \n greater than 0.0 and \n less than 1.0",
                                   parent=app, minvalue=0, maxvalue=0.999)
    if answer is not None:
        dth.Data.split = answer
        splitstring = '%s%s' % (dth.Data.split * 100, '% of the dataset will be used for testing.')
        output.insert(INSERT, splitstring)
        return True
    else:
        output.insert(INSERT, 'Operation cancelled', spacing())
        return False


# Runs the regression function on the currently loaded dataset, outputs the results in the GUI
def regclicked():
    result, mae = dtr.regress(dth.Data.dataframe, dth.Data.split)
    output.insert(INSERT, result, spacing())
    output.insert(INSERT, mae, spacing())


# Runs the classification function on the currently loaded dataset, outputs the results in the GUI
def clasclicked():
    res = dtc.classify(dth.Data.dataframe, dth.Data.split)
    output.insert(INSERT, res, spacing())


# Clears the output field of the GUI for a fresh start
def clearoutput():
    output.delete(1.0, END)


# Lets the user choose a file from their computer to use with the system
def loadfile():
    path = filedialog.askopenfilename(parent=app,
                                      initialdir=os.getcwd(),
                                      title="Please select a file:",
                                      filetypes=(('CSV files', '.csv'), ('All files', '*.*')))
    pathlist = path.split("/")
    if pathlist[(len(pathlist) - 1)].lower().endswith('.csv'):
        pathend = pathlist[(len(pathlist) - 1)]
        dth.Data.dataframe = dth.load_dataframe(pathend)
        dth.autosave_dataframe_to_pickle(dth.Data.dataframe)
        output.insert(INSERT, 'File ' + pathend + ' loaded', spacing())

    else:
        output.insert(INSERT, 'Wrong filetype - Please select a CSV file', spacing())


# Prints the entire dataset to the output window of the GUI
def printdataset():
    output.insert(INSERT, dth.Data.dataframe.to_string())


# Saves the currently loaded dataset as a new file (to allow mutation without deletion
def saveasnew():
    message = dth.save_as_new(dth.Data.dataframe)
    output.insert(INSERT, 'Saved file as: ' + message)


# Test methods for quick testing - work in progress for creating better methods and stuff
def mregtest():
    mean_absolute_error = list()
    # for i in range(20):
    #    regclicked()

    # Implemented input for custom splits with option to cancel, hence the if statement.
    for i in range(20):
        result, mae = regressor.regress(dth.Data.dataframe, dth.Data.split)
        mean_absolute_error.append(mae)
        output.insert(INSERT, result, spacing())
    output.insert(INSERT, sum(mean_absolute_error)/len(mean_absolute_error), spacing())
    output.insert(INSERT, dth.Data.split)


# Same as above, test method.
def mclastest():
    # for i in range(20):
    #    clasclicked()
    females = dth.filter_criterion(dth.Data.dataframe, 'sex', 2)
    result, mae = dtr.regress(females, dth.Data.split)
    output.insert(INSERT, result, spacing())
    output.insert(INSERT, mae, spacing())
    output.insert(INSERT, females, spacing())


# Adds some breaklines to the output text field to increase readability by seven thousand percent
def spacing():
    output.insert(INSERT, '\n', '\n', '\n')


# ---------- LABELS ----------
# welcomelabel = Label(app, text='I\'m afraid I can\'t do that, Dave')
# welcomelabel.grid(column=0, row=0)

# ---------- OUTPUT -----------
output = scrolledtext.ScrolledText(app, width=110, height=50)
output.grid(column=3, row=0)

buttonframe = Frame(app)
# ---------- TEMP BUTTONS ----------
massiveregtest = Button(buttonframe, text="Regress 20", command=mregtest)
massiveregtest.pack(padx=10, pady=10)

massiveclastest = Button(buttonframe, text="Classify 20", command=mclastest)
massiveclastest.pack(padx=10, pady=10)


# ---------- BUTTONS ----------

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

inputsplitBTN = Button(buttonframe, text="Change split value", command=askforsplit)
inputsplitBTN.pack(padx=15, pady=15)

buttonframe.grid(column='0', row='0')

app.mainloop()

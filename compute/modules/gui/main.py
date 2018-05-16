from tkinter import *
from tkinter import scrolledtext, simpledialog
from tkinter import filedialog
from os.path import dirname
from compute.modules import datahandler
from compute.modules.ml import classifier, regressor
import os


# System modules abbreviated for simplicity
dtc = classifier
dtr = regressor
dth = datahandler


# Fix for different paths - html.py / main.py
# TODO make it better
dth.Path.pickle_data = '%s%s' % (dirname(dirname(os.getcwd())), r'/data/data.pkl')
dth.Path.pickle_data = '%s%s' % (dirname(dirname(os.getcwd())), r'/data/split.pkl')


# GUI-related variables
app = Tk()
app.title('Bongo')
app.geometry('1200x900')
stree = StringVar()

if dth.Data.dataframe.empty:
    dth.Data.dataframe = dth.load_dataframe(dth.Path.path)


# Ask for the user to input their desired split, where the input defines the test set size.
# The greater the test set the less the training set, and vice versa.
def askforsplit():
    answer = simpledialog.askfloat("Input", "Which percentage of \n the dataset will be \n used for testing? \n "
                                            "Please input a value \n greater than 0.0 and \n less than 1.0",
                                   parent=app, minvalue=0, maxvalue=0.999)
    if answer is not None:
        dth.update_pickle(dth.Data.dataframe, answer)
        splitstring = '%s%s' % (dth.Data.split * 100, '% of the dataset will be used for testing.')
        stree.set('%s%s' % ('Split value is: ', dth.Data.split))
        output.insert(INSERT, splitstring)
        app.update_idletasks()

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
def classify_clicked():
    res = dtc.classify(dth.Data.dataframe, dth.Data.split)
    output.insert(INSERT, res, spacing())


# Clears the output field of the GUI for a fresh start
def clear_output():
    output.delete(1.0, END)


# Lets the user choose a file from their computer to use with the system
def load_file():
    dialogpath = '%s%s' % (dirname(dirname(os.getcwd())), '/data/')
    path = filedialog.askopenfilename(parent=app,
                                      initialdir=dialogpath,
                                      title="Please select a file:",
                                      filetypes=(('CSV files', '.csv'), ('All files', '*.*')))
    pathlist = path.split("/")
    if pathlist[(len(pathlist) - 1)].lower().endswith('.csv'):
        pathend = pathlist[(len(pathlist) - 1)]
        dth.Data.dataframe = dth.load_dataframe(path)
        dth.autosave_dataframe_to_pickle(dth.Data.dataframe)
        output.insert(INSERT, 'File ' + pathend + ' loaded', spacing())

    else:
        output.insert(INSERT, 'Wrong filetype - Please select a CSV file', spacing())


# Prints the entire dataset to the output window of the GUI
def print_dataset():
    output.insert(INSERT, dth.Data.dataframe.to_string())


# Saves the currently loaded dataset as a new file (to allow mutation without deletion
def save_as_new():
    message = dth.save_as_new(dth.Data.dataframe)
    output.insert(INSERT, 'Saved file as: ' + message, spacing())


# Test methods for quick testing - work in progress for creating better methods and stuff
def mass_regression_test():
    mean_absolute_error = list()
    # for i in range(20):
    #    regclicked()
    ladies = dth.filter_criterion(dth.Data.dataframe, 'sex', 2)
    # Implemented input for custom splits with option to cancel, hence the if statement.
    for i in range(20):
        result, mae = regressor.regress(ladies, dth.Data.split)
        mean_absolute_error.append(mae)
        output.insert(INSERT, result, spacing())
    output.insert(INSERT, sum(mean_absolute_error)/len(mean_absolute_error), spacing())
    output.insert(INSERT, dth.Data.split)


# Same as above, test method.
def mass_classification_test():
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

stree.set('%s%s' % ('Split value is: ', dth.Data.split))
split_value_label = Label(app, textvariable=stree.get())
split_value_label.grid(column=0, row=2)

# ---------- OUTPUT -----------
output = scrolledtext.ScrolledText(app, width=110, height=50)
output.grid(column=3, row=0)

buttonframe = Frame(app)


# ---------- TEMP BUTTONS ----------
massiveregtest = Button(buttonframe, text="Regress 20", command=mass_regression_test)
massiveregtest.pack(padx=10, pady=10)

massiveclastest = Button(buttonframe, text="Classify 20", command=mass_classification_test)
massiveclastest.pack(padx=10, pady=10)


# ---------- BUTTONS ----------

regressionBTN = Button(buttonframe, text='Regression', command=regclicked)
regressionBTN.pack(padx=5, pady=5)

classifierBTN = Button(buttonframe, text='Classification', command=classify_clicked)
classifierBTN.pack(padx=5, pady=15)

clearoutputBTN = Button(buttonframe, text='Clear output field', command=clear_output)
clearoutputBTN.pack(padx=5, pady=15)

loadfileBTN = Button(buttonframe, text='Load dataset CSV', command=load_file)
loadfileBTN.pack(padx=5, pady=5)

savenewfileBTN = Button(buttonframe, text='Save dataset as new', command=save_as_new)
savenewfileBTN.pack(padx=5, pady=15)

printdataBTN = Button(buttonframe, text='Print dataset', command=print_dataset)
printdataBTN.pack(padx=5, pady=5)

inputsplitBTN = Button(buttonframe, text="Change split value", command=askforsplit)
inputsplitBTN.pack(padx=15, pady=15)

buttonframe.grid(column='0', row='0')


app.mainloop()

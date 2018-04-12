# Deprecated - no need to convert xls to json

import xlrd
import simplejson as json
from collections import OrderedDict

# Open the workbook and select the first worksheet
workbook = xlrd.open_workbook('database.xls')
sheet = workbook.sheet_by_index(0)

# List to hold dictionaries
data_list = []

# Iterate through each row in worksheet and fetch values into dict
for rownum in range(1, sheet.nrows):
    info = OrderedDict()
    row_values = sheet.row_values(rownum)
    categories = row_values[0].split(',')
    temp = 0
    for item in categories:
        info[item] = categories[temp]
        temp += 1

    data_list.append(info)

# Serialize the list of dicts to JSON
j = json.dumps(data_list)

# Write to file
with open('data.json', 'w') as f:
    f.write(j)

with open('data.json', 'r') as file:
    bob = file.read().split(',')
    for tib in bob:
        print(tib + '\n')

print(data_list)
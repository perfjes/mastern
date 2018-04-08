import xlrd
import simplejson as json
from collections import OrderedDict

# Open the workbook and select the first worksheet
workbook = xlrd.open_workbook('excel-xlrd-sample.xls')
sheet = workbook.sheet_by_index(0)

# List to hold dictionaries
data_list = []

# Iterate through each row in worksheet and fetch values into dict
for rownum in range(1, sheet.nrows):
    info = OrderedDict()
    row_values = sheet.row_values(rownum)
    info['car-id'] = row_values[0]
    categories = row_values[0].split(',')
    for item in categories:
        info[item] = what the fuck

    data_list.append(info)

# Serialize the list of dicts to JSON
j = json.dumps(data_list)

# Write to file
with open('data.json', 'w') as f:
    f.write(j)
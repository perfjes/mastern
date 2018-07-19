from root.webinterface.modules import datahandler
from root.deprecated import regressor

dth = datahandler
df = dth.Data.dataframe


all_positive_cases = df.loc[df['Case'] == 1]
all_negative_cases = df.loc[df['Case'] == 0]


# Sex describes the gender of the patient, where 1 equals male and 2 equals female.
malecase = all_positive_cases.loc[all_positive_cases['sex'] == 1]
femalecase = all_positive_cases.loc[all_positive_cases['sex'] == 2]


def mpredlongevity(split):
    return regressor.regress(malecase, split)


def fpredlongevity(split):
    return regressor.regress(femalecase, split)

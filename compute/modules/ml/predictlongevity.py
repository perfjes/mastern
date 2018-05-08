from compute.modules import datahandler
from compute.modules.ml import regressor

dth = datahandler
df = regressor.Regressdata.df
allpositivecases = df.loc[df['Case'] == 1]


# Sex describes the gender of the patient, where 1 equals male and 2 equals female.
malecase = allpositivecases.loc[allpositivecases['sex'] == 1]
femalecase = allpositivecases.loc[allpositivecases['sex'] == 2]


def mpredlongevity(split):
    return regressor.regress(malecase, split)


def fpredlongevity(split):
    return regressor.regress(femalecase, split)

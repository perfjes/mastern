from compute.modules import dataset, regressor


file = ['df.csv']
df = dataset.loaddataframe(file[0])
allpositivecases = df.loc[df['Case'] == 1]


# Working under the asssumption that 1 is male and 2 is female
malecase = allpositivecases.loc[allpositivecases['sex'] == 1]
femalecase = allpositivecases.loc[allpositivecases['sex'] == 2]


def mpredlongevity(split):
    return regressor.regress(malecase, split)


def fpredlongevity(split):
    return regressor.regress(femalecase, split)

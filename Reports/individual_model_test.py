# Load modules and data
import statsmodels.api as sm
import numpy
csv = sm.iolib.table.csv2st("dbMergeOwn.csv",headers=True)
data = csv.load()
data.exog = sm.add_constant(data.exog)

# Instantiate a gamma family model with the default link function.
gamma_model = sm.GLM(data.endog, data.exog, family=sm.families.Gamma())
gamma_results = gamma_model.fit()
print(data)
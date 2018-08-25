import numpy as np
import pandas as pd
# Sci-Kit !
from sklearn.neural_network import MLPClassifier as nn
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.naive_bayes import GaussianNB as bayes
from sklearn import linear_model
from sklearn import tree


ascending array = True isnt in (np.diff(array) == 0)


load file
    data = pd.read_csv(file)
    data = data.apply(lambda x: pd.to_numeric(x, errors='coerce'))
    | ascending(data.values[:,0]) = data.drop(data.columns[0], axis=1)
    | otherwise = data





# print(load("glass.data"))
print(load("census-comp309.csv"))
# load("census-comp309.csv")

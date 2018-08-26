import numpy as np
import pandas as pd
# Sci-Kit !
from sklearn.neural_network import MLPClassifier as nn
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.naive_bayes import GaussianNB as bayes
from sklearn import linear_model
from sklearn import tree
from sklearn.preprocessing import Imputer
# Others
import matplotlib.pyplot as plt

# Is an array in strictly ascending order?
ascending array = False isnt in (np.diff(array) >= 0)

# Slice a Numpy array vertically
verticalSlice array index = (array[:,0:index-1], array[:,index-1])

# Split a Pandas dataframe by inputs and output columns
split df = (df.drop(df.columns[-1], axis=1), df[df.columns[-1]])

# Split a Pandas dataframe by rows
horizontalSlice df index = (df[:index], df[index:])


impute df method
    | method == "drop" = df.dropna()
    | otherwise = Imputer(strategy=method).fit_transform(df)

load file
    data = pd.read_csv(file)
    data = data.apply(lambda x: pd.to_numeric(x, errors='coerce'))
    | ascending(data.values[:,0]) = data.drop(data.columns[0], axis=1)
    | otherwise = data

histogram feature name
    plt.hist(feature)
    plt.show()

factorial n
    | n == 1 = 1
    | otherwise = n * factorial2 (n-1)

start program
    data = load("census-comp309.csv")
    training, test = horizontalSlice(data, 3000)
    training_x = split(training)[0]
    imputed_x = impute(training_x, "mean")
    histogram(imputed_x[:,5], "test")

start


# Bubbles-Language

Bubbles is a experimental, functional and fun Super-Set Language for Python!
The aim is to provide beautiful and functional syntax!

#### Syntax examples:
```
Type NumpyArray = numpy.float64 | numpy.ndarray

ascending :: NumpyArray -> Bool
ascending array = False isnt in (np.diff(array) >= 0)

impute df method
    | method == "drop" = df.dropna()
    | otherwise = Imputer(strategy=method).fit_transform(df)

load file
    data = pd.read_csv(file)
    data = data.apply(lambda x: pd.to_numeric(x, errors='coerce'))
    | ascending(data.values[:,0]) = data.drop(data.columns[0], axis=1)
    | otherwise = data

factiorial :: Number -> Number
factorial n
    | n == 1 = 1
    | otherwise = n * factorial2 (n-1)

start program
    data = load("x.csv")
    training, test = horizontalSlice(data, 3000)
    training_x = split(training)[0]
    imputed_x = impute(training_x, "mean")
    histogram(imputed_x[:,5], "test")

start
```

#### Currently features:
- Supports Haskell-style Functional control and pattern matching.
- Basic Algebraic Data Types ( Union is to do )
- Dynamic Function Type checking
- Has new keywords for easy readibility:
    isnt == not --> if element isnt in set

#### Ideas of things to do:
- Graph based Type/Set System, high level set functions
- Folds?
- Security Features?
- Simple/Easy syntax for Meta Programming and Dynamic Object Creation
- Create beautified syntax for Classes and add more functional control:
-  Remove explicit .self in class declarations, use implicit scoping
- Remove or replace object __init__ constructor syntax


It can be used either within Python: python bubbles example.bb
Potentially will have binary for command line use: bubbles example.bb

It is potentially quite buggy / hackish, it's mostly for fun!

Copyright 2018 - Thomas Watts - twatts@protonmail.com

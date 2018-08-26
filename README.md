# Bubbles-Language

Bubbles is a work in progress, experimental, fun Super-Set Language for Python!

The primary aim is to provide beautiful syntax and provide functional Haskell-like control!

#### Syntax examples:
```
ascending array = False isnt in (np.diff(array) >= 0)

impute df method
    | method == "drop" = df.dropna()
    | otherwise = Imputer(strategy=method).fit_transform(df)

load file
    data = pd.read_csv(file)
    data = data.apply(lambda x: pd.to_numeric(x, errors='coerce'))
    | ascending(data.values[:,0]) = data.drop(data.columns[0], axis=1)
    | otherwise = data

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
```

#### Currently features:
- Supports Haskell-style Functional control and pattern matching.
- Has new keywords for easy readibility:
    isnt == not --> if element isnt in set

#### Ideas of things to do:
- Haskell-like type system, can add type constraints to functions
  Definitely have dynamic type checking for these functions, making compile time checks might not be possible.
- Improved security, constrain I/O?
- Simple/Easy syntax for Meta Programming and Dynamic Object Creation

- Create beautified syntax for Classes and add more functional control:
  Remove explicit .self in class declarations, use implicit scoping
  Remove or replace object __init__ constructor syntax


It can be used either within Python: python bubbles example.bb
Potentially will have binary for command line use: bubbles example.bb

It is potentially quite buggy / hackish, it's mostly for fun!

Copyright 2018 - Thomas Watts - twatts@protonmail.com

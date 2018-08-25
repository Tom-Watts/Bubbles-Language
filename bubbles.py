import sys
import ast

"""
Bubbles is a experimental/fun Super-Set Language for Python.

Currently it supports Haskell-style Functional control and pattern matching.

Potential Ideas:
- Haskell-like type system, can add type constraints to functions
- Improved security, constrain I/O
- Simple/Easy syntax for Meta Programming and Dynamic Object Creation

- Remove explicit .self in class declarations, use implicit scoping
- Remove or replace object __init__ constructor syntax
- Introduce new keywords, for instance "isn't" for easy readibility:
    if element isn't in set:

- It can be used either within Python: python bubbles example.bb
- Potentially will have binary for command line use: bubbles example.bb

Copyright 2018 - Thomas Watts - twatts@protonmail.com

"""



keywords = ["if", "else", "elif", "not", "in", "for", "return", "*", "+", "-", "/"
            "while", "and", "False", "True", "|", ":", "="]

function_map = {}


# No statements can have only 0 or 1 tokens
def empty(line):
    tokens = line.split()
    return len(tokens) == 0 or len(tokens) == 1

# We need to check where the position of "=" in lhs = rhs for translation
equalPos = lambda t, i: t[i-1] !="=" and t[i]=="=" and t[i+1] != "="
equalIndex = lambda t: [equalPos(t, i) for i in range(1, len(t)-1)].index(True) + 1

# Check if have a valid function body
def functionBody(line):
    if not line:
        return False
    tokens = line.split()
    if len(tokens) == 0:
        return False
    if tokens[0] != "|":
        return False
    # Need checks here!!! Otherwise things will blow up
    return True

# Parse and Translate Bubbles inner function, to a Python function's body
def parseFunctionBody(text, translation):
    tokens = text[0].split()
    index = equalIndex(tokens)
    statement = ""
    if(tokens[1] != "otherwise"):
        statement += "    if ("
        for t in tokens[1:index]:
            statement+= t
        statement += "): \n    "

    statement += "    return ("
    for t in tokens[index+1:]:
        statement+=t
    statement += ") \n"

    if len(text) != 1 and functionBody(text[1]):
        return parseFunctionBody(text[1:], translation + statement)
    return parse(text[1:], translation + statement)


# Create declarations for a python function and lambda to reference it
# We can't use complex chains (e.g. if/else) normally in Python's Lambdas
# That is why there is a normal function, and then a lambda to be passed around.
def parseFunction(text, translation):
    # return parse(text[1:], translation + text[0])
    tokens = text[0].split()
    function_map[tokens[0]] = True

    lmbda = tokens[0] + " = lambda "
    for i in range(1, len(tokens)-1):
        lmbda += tokens[i] + ","
    lmbda += tokens[-1]
    lmbda += ": " + tokens[0] + "_BUBBLES_DEF("
    for i in range(1, len(tokens)-1):
        lmbda += tokens[i] + ","
    lmbda += tokens[-1]
    lmbda += ") \n \n"

    declaration = "def " + tokens[0] + "_BUBBLES_DEF("
    for i in range(1, len(tokens)-1):
        declaration += tokens[i] + ","
    declaration += tokens[-1] + "): \n"
    if not functionBody(text[1]):
        raise SyntaxError("Expected Guard after function declaration")
    return parseFunctionBody(text[1:], translation + lmbda + declaration)

# Check if we have a valid function declaration
def functionDeclaration(line):
    tokens = line.split()
    if True in [(t in keywords) for t in tokens]:
        return False
    if tokens[-1][-1] == ":":
        return False
    # Args cannot be numbers, good for differentiating declarations from evals
    for t in tokens:
        if "(" in t or ")" in t:
            return False
        try:
            float(t)
            return False
        except ValueError:
            continue
    return True

# Unused:
# Could keep Haskell evaluation syntax, e.g. add 3 4
# Better to keep consistent with Python e.g. add(3,4)
"""
def parseFunctionEval(text, translation):
    tokens = text[0].split()
    eval = tokens[0] + "("
    for t in tokens[1:-1]:
        eval+= t + ","
    eval += tokens[-1] + ")"
    return parse(text[1:], translation+eval)

# Check if we a line is evaluating a Bubbles function
def functionEvalualation(line):
    tokens = line.split()
    if True in [(t in keywords) for t in tokens]:
        return False
    if tokens[-1][-1] == ":":
        return False
    # Probably need to do some checks here to be 100% certain no overlap with decs
    return True
"""


# Use tail recursion to parse and translate Bubbles code to Python code
def parse(text, translation):
    if len(text) == 0:
        return translation
    text[0] = text[0].split('#', 1)[0]
    if empty(text[0]):
        return parse(text[1:], translation + text[0])
    if functionDeclaration(text[0]):
        return parseFunction(text, translation)
    return parse(text[1:], translation + text[0])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Bubbles needs code!")
    else:
        f = open(sys.argv[1],"r")
        text = [t for t in f]
        translation = parse(text, "")
        print(translation)
        exec(translation)

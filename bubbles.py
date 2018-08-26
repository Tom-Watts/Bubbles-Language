import sys
import ast

"""-----------------------------------------------------------------------------
BUBBLES:
Is a experimental, functional and fun Super-Set Language for Python!
The aim is to provide beautiful and functional syntax!

Currently features:
- Supports Haskell-style functionals and pattern matching.
- Has new keywords for easy readibility:
    isnt == not --> if element isnt in set

Ideas / To Do:
- Haskell-like type system, can add type constraints to functions
- Improved security, constrain I/O or sys calls?
- Partial Application for currying?
- Simple/Easy syntax for Meta Programming
- Neater Object Oriented syntax:
- Remove explicit .self in class declarations, use implicit scoping
- Remove or replace object __init__ constructor syntax

Copyright 2018 - Tom Watts: twatts@protonmail.com

-----------------------------------------------------------------------------"""


keywords = ["if", "else", "elif", "not", "in", "for", "return", "*", "+", "-", "/"
            "while", "and", "False", "True", "|", ":", "=", "import", "as"]

# Not yet used
function_map = {}

# Used for keeping track of dependencies / imports
file_map = {}


#------------------------- Patterns and Translation ----------------------------

# No statements can have only 0 or 1 tokens (unless start)
def empty(line):
    tokens = line.split()
    return len(tokens) == 0 or (len(tokens) == 1 and tokens[0] != "start")


# Swap new keywords with their traditional Python counterparts
def matchKeywords(line):
    return line.replace("isnt", "not")


# We need to check where the position of "=" in lhs = rhs for translation
equalPos = lambda t, i: (
    (t[i-1] !="=" and t[i]=="=" and t[i+1] != "=") or
    (t[i-1] !="!" and t[i]=="=") or
    (t[i-1] !=">" and t[i]=="=") or
    (t[i-1] !="<" and t[i]=="=")
    )
# Check if the above pattern is in an array
equalIndex = lambda t: [equalPos(t, i) for i in range(1, len(t)-1)].index(True) + 1
# Check if a line is an assignment statement
def assignment(line):
    tokens = line.split()
    for i in range(1, len(tokens)):
        if tokens[i] == "=":
            if tokens[i-1] != "<" or tokens[i-1] != ">" or tokens[i-1] != "!" or tokens[i-1] != "!":
                return True
    return False


# Check if there is a valid function body
def functionBody(line, indent):
    if not line:
        return False
    tokens = line.split()
    if len(tokens) == 0:
        return False
    # Need checks here!!! Otherwise things will blow up
    return True
# Parse and Translate Bubbles inner function, to a Python function's body
def parseFunctionBody(text, translation, indent, k):
    text[0] = text[0].replace("isnt", "not")
    tokens = text[0].split()
    if tokens[0] != "|":
        if len(text) != 1 and functionBody(text[1], indent):
            return parseFunctionBody(text[1:], translation + text[0], indent, k+1)
        return parse(text[1:], translation + text[0], indent, k+1)
    index = equalIndex(tokens)
    statement = ""
    if(tokens[1] != "otherwise"):
        statement += "    if ("
        for t in tokens[1:index]:
            statement+= t + " "
        statement += "): \n    "
    statement += "    return ("
    for t in tokens[index+1:]:
        statement+=t
    statement += ") \n"
    if len(text) != 1 and functionBody(text[1], indent):
        return parseFunctionBody(text[1:], translation + statement, indent, k+1)
    return parse(text[1:], translation + statement, indent, k+1)


# Create declarations for a python function and lambda to reference it
# We can't use complex chains (e.g. if/else) normally in Python's Lambdas
# That is why there is a normal function, and then a lambda to be passed around.
def parseFunction(text, translation, indent, k):
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
    if not functionBody(text[1], indent+1):
        print("Error on line: ", k)
        raise SyntaxError("Expected Indent after function declaration.")
    return parseFunctionBody(text[1:], translation + lmbda + declaration, indent+1, k+1)
# Check if we have a valid function declaration
def functionDeclaration(line, indent):
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
def parseFunctionEval(text, translation, indent, k):
    print("evaluating function eval")
    tokens = text[0].split()
    eval = tokens[0] + "("
    for t in tokens[1:-1]:
        eval+= t + ","
    eval += tokens[-1] + ")"
    return parse(text[1:], translation+eval, indent, k+1)
# Check if we a line is evaluating a Bubbles function
def functionEvalualation(line, indent):
    tokens = line.split()
    if True in [(t in keywords) for t in tokens]:
        return False
    if tokens[-1][-1] == ":":
        return False
    # Probably need to do some checks here to be 100% certain no overlap with decs
    return True


# Convert nice looking single line lambda to Python's version
def parseSingleLineLambda(text, translation, indent, k):
    tokens = text[0].split()
    index = equalIndex(tokens)
    lmbda = tokens[0] + " = lambda "
    for i in range(1, index-1):
        lmbda += tokens[i] + ", "
    lmbda += tokens[index-1] + " : "
    for t in tokens[index+1:]:
        lmbda += t + " "
    lmbda += "\n"
    return parse(text[1:], translation + lmbda, indent, k+1)
# Check if we have a single line lambda of form: name (variables ...) = (body)
def singleLineLambda(line, indent):
    if not assignment(line):
        return False
    tokens = line.split()
    index = equalIndex(tokens)
    if index < 2:
        return False
    for i in range(0, index):
        try:
            float(tokens[0])
            return False
        except ValueError:
            continue
    return True


# A special keyword start, is used to replace if __name__ == "__main__":
def startDeclaration(line):
    tokens = line.split()
    if len(tokens) == 0:
        return False
    if len(tokens) == 1 and tokens[0] == "start":
        return True
    return False
# there must be a function calleed (start program) in order to use start
def parseStart(text, translation, indent, k):
    stmt = "start(True) \n"
    return parse(text[1:], translation + stmt, indent, k+1)


# Check if we have a statement of form: include .... (files can be .py or .bb)
def importStatement(line):
    tokens = line.split()
    return tokens[0] == "include"
# Parse the above
def parseImport(text, translation, indent, k):
    tokens = text[0].split()
    block = translate(tokens[1])
    return parse(text[1:], translation + block, indent, k+1)

#------------------------------ Main Loop --------------------------------------

# Use tail recursion to parse and translate Bubbles code to Python code
def parse(text, translation, indent, k):
    if len(text) == 0:
        return translation
    text[0] = text[0].split('#', 1)[0]
    text[0] = matchKeywords(text[0])

    # Check and parse unique syntax patterns
    if empty(text[0]):
        return parse(text[1:], translation + text[0], indent, k+1)
    if importStatement(text[0]):
        return parseImport(text, translation, indent, k+1)
    if startDeclaration(text[0]):
        return parseStart(text, translation, indent, k+1)
    if singleLineLambda(text[0], indent):
        return parseSingleLineLambda(text, translation, indent, k+1)
    if functionDeclaration(text[0], indent):
        return parseFunction(text, translation, indent, k+1)
    # Otherwise keep line / do not translate
    return parse(text[1:], translation + text[0], indent, k+1)

#-------------------------------------------------------------------------------

def translate(file):
    try:
        f = open(file,"r")
        text = [t for t in f]
        return parse(text, "", indent=0, k=0)
    except:
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Bubbles needs code!")
    else:
        translation = translate(sys.argv[1])
        print(translation)
        exec(translation)

import re

# Regex List
regexList = [
    r'[_a-zA-Z]+[_A-Za-z0-9]*',
    r'^[-+]?[0-9]+$',
    r'[+-]?[0-9]+\.[0-9]+' ,
    #r'[#].*',
    #r'\'\'\'[\S\s]*\'\'\'',
    #r'\'[\w\W]*\'',
    #r'\"[\w\W]*\"',
    ]
# Maps regex into valid key
regexMap = {
    r'[_a-zA-Z]+[_A-Za-z0-9]*' : "variable",
    r'^[-+]?[0-9]+$' : "integer",
    r'[+-]?[0-9]+\.[0-9]+' : "float",
    #r'[#].*' : "comment",
    #r'\'\'\'[\S\s]*\'\'\'' : "comment",
    #r'\'[\w\W]*\'' : "string",
    #r'\"[\w\W]*\"' : "string",
    }

# Valid Operator
operators = [':', ',', '=', '<', '>', '>=', '<=', '==', '!=', r'\+', '-', r'\*', '/', r'\*\*', r'\(', r'\)',r'\'\'\'', r'\'', r'\"']

# Supported Syntax
availableTerminal=[ 'False' , 'True'    , 'None'    , 'and'     , 'as'      , 'break', 
                    'class' , 'continue', 'def'     , 'elif'    , 'else'    , 'for', 
                    'from'  , 'if'      , 'import'  , 'in'      , 'is'      , 'not', 
                    'or'    , 'pass'    , 'raise'   , 'return'  , 'while'   , 'with',
                    'print' , 'string'  , 'range'   , 'content']

def concatString(content):
    startComment = []
    endComment = []
    count = 1
    for i in range (len(content)):
        if (content[i] == '\"'):
            if(count % 2 == 1):
                startComment.append(i)
                count += 1
            else:
                endComment.append(i)
                count += 1
    for i in range(len(startComment)):
        if (endComment[i] != None):
            content[startComment[i]+1:endComment[i]] = [" ".join(content[startComment[i]+1:endComment[i]])]
            content[startComment[i]+1] = 'string'
        else:
            content[startComment[i]+1:] = [" ".join(content[startComment[i]:])]
            content[startComment[i]+1] = 'string'
    return content

def concatMultiLineComment1(content):
    startComment = []
    endComment = []
    count = 1
    print(content)
    for i in range (len(content)):
        if (content[i] == '\'\'\''):
            if(count % 2 == 1):
                startComment.append(i)
                count += 1
            else:
                endComment.append(i)
                count += 1
    for i in range(len(startComment)-1,-1,-1):
        if (len(startComment) == len(endComment)):
            content[startComment[i]+1:endComment[i]] = [" ".join(content[startComment[i]+1:endComment[i]])]
            content[startComment[i]+1] = 'content'
        else:
            content[startComment[i]+1:] = [" ".join(content[startComment[i]:])]
            content[startComment[i]+1] = 'content'
    return content

def concatMultiLineComment2(content):
    startComment = []
    endComment = []
    count = 1
    for i in range (len(content)):
        if (content[i] == '\"\"\"'):
            if(count % 2 == 1):
                startComment.append(i)
                count += 1
            else:
                endComment.append(i)
                count += 1
    for i in range(len(startComment)-1,-1,-1):
        if (len(startComment) == len(endComment)):
            content[startComment[i]+1:endComment[i]] = [" ".join(content[startComment[i]+1:endComment[i]])]
            content[startComment[i]+1] = 'content'
        else:
            content[startComment[i]+1:] = [" ".join(content[startComment[i]:])]
            content[startComment[i]+1] = 'content'
    return content

def concatSingleLineComment(content):
    startComment = []
    endComment = []
    count = 0
    for i in range (len(content)):
        if (content[i] == '#'):
            startComment.append(i)
            count += 1
        if (count == 1):
            if (content[i] == '\\n'):
                endComment.append(i)
                count = 0

    for i in range(len(startComment)):
        if (endComment[i] != None):
            content[startComment[i]+1:endComment[i]+1] = [" ".join(content[startComment[i]+1:endComment[i]+1])]
            content[startComment[i]+1] = 'content'
        else:
            content[startComment[i]+1:] = [" ".join(content[startComment[i]+1:])]
            content[startComment[i]+1] = 'content'
    return content

def concatComment(content):       
    content = concatMultiLineComment1(content)
    content = concatMultiLineComment2(content)
    content = concatSingleLineComment(content)
    return content

def tokenizeInput(inputFilename):
    # Read from file
    f = open(inputFilename, "r")
    contents = f.read()
    f.close()
    result = contents.split()

    for operator in operators:
        temporaryResult = []
        for statement in result:
            if(statement != '\'\'\'' and statement != '\"\"\"'):
                format = r"[A..z]*(" + operator +r")[A..z]*"
                x = re.split(format, statement)
             
                for splitStatement in x:
                    temporaryResult.append(splitStatement) 
            else:
                temporaryResult.append(statement)
        result = temporaryResult

    temporaryResult = []
    for statement in result:
        stripped = statement.split()
        for splitStatement in stripped: 
            temporaryResult.append(splitStatement)

    result = temporaryResult
    result = [string for string in result if string!='']
    result = concatComment(result)
    result = concatString(result)
    
    # Change every number to their type
    for i in range(len(result)):
        found = False
        for syntax in availableTerminal:
            if syntax == result[i]:
                found = True
        if not found:
            for pattern in regexList:
                if(re.match(pattern, result[i])):
                    result[i] = regexMap[pattern]
    return result
from lib2to3.pgen2.tokenize import tokenize
from operator import index
from typing import NamedTuple
import re

class Tokenized(NamedTuple):
    type: str
    string: str
    line_num: int
    column: int
    
def tokenizeFile(filename):

    tokens = []
    sourceName = filename 
    input = open(sourceName, "r")

    keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'elif', 'await',
    'break', 'class', 'continue']
    token_specification = [
        ('Number',      r'\d+(\.\d*)?'),  # Integer or decimal number
        ('Delimiters',  r'[;:]'),         # Statement terminator
        ('Identifiers', r'[A-Za-z]+'),    # Identifiers
        ('Operators',   r'[+\-*<>/]'),    # Arithmetic operators
        ('NEWLINE',     r'[\n]+'),        # Line endings
        ('SKIP',        r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH',    r'.'),            # Any other character
        
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 0
    for line in input:
        print(line)
        line_num += 1
        line_start = 0
        for mo in re.finditer(tok_regex, line):
            type = mo.lastgroup
            string = mo.group()
            column = mo.start() - line_start
            if type == 'Number':
                string = float(string) if '.' in string else int(string)
            elif type == 'Identifiers' and string in keywords:
                type = 'Keyword'
            elif type == 'Identifiers':
                type = 'Identifiers'
            elif type == 'NEWLINE':
                line_start = mo.end()
                continue
            elif type == 'SKIP':
                continue
            elif type == 'MISMATCH':
                print("error")
            
            tokens.append(Tokenized(type, string, line_num, column))
    return tokens

#print(tokens)


for token in tokenizeFile("hei.txt"):
    print(token)

v = tokenizeFile("hei.txt")
print(v)

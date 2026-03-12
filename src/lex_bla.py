import ply.lex as lex
import sys

"""
Lexical Analyser which does lexical analysis for the BLA programming language.
:author: Siyabonga Madondo
:version: 18/03/2026
"""

# Token Definitions
tokens = [
    'ID',
    'BINARY_LITERAL',
    'WHITESPACE',
    'COMMENT',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'A',
    'S',
    'M',
    'D',
]

# Regular Expressions
t_ID = r'[a-z_][A-Za-z0-9_]*'
t_BINARY_LITERAL = r'[+-]?[01]+'
t_WHITESPACE = r'\s+'
t_COMMENT = r'//.*|/\*[\s\S]*?\*/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_A = r'A'
t_S = r'S'
t_M = r'M'
t_D = r'D'

# Error Function
def t_error(t):
    t.lexer.skip(1)

# Lexer Initialisation
lexer = lex.lex()

def tokeniser(filename: str) -> None:
    # Input File Handling
    input_file = filename
    content = ''

    with open(input_file, 'r') as file:
        content = file.read()

    lexer.input(content)

    # Output File Handling
    output_file = input_file.replace('.bla', '.tkn')

    with open(output_file, 'w') as file:
        while True:
            token = lexer.token()
            if not token:
                break
            elif token.type in {'WHITESPACE', 'COMMENT'}:
                print(f"{token.type}")
                file.write(f"{token.type}\n")
            elif token.type in {'EQUALS', 'LPAREN', 'RPAREN', 'A', 'S', 'M', 'D'}:
                print(f"{token.value}")
                file.write(f"{token.value}\n")
            else:
                print(f"{token.type},{token.value}")
                file.write(f"{token.type},{token.value}\n")
        
if __name__ == '__main__':
    # Check if correct number of args given
    if len(sys.argv) == 1:
        filename = sys.argv[1]
        tokeniser(filename)
    else:
        print('Usage: python lex_bla.py <filename>.bla')
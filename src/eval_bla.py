from lex_bla import lexer
from parse_bla import parser, FilteredLexer
import sys

"""
Evaluator for the BLA programming language.
:author: Siyabonga Madondo
:version: 18/03/2026
"""

def evaluate(ast, symbol_table, file):
    # Evaluate Each Statement in AST
    for statement in ast[1]:
        _, variable, value, _ = statement
        result = eval_expr(value, symbol_table)
        symbol_table[variable] = result
        stmt = f'{variable}[{int_to_binary(result)}]'
        print(stmt)
        file.write(stmt + '\n')

def eval_expr(value, symbol_table):
    # Evaluate Each Expression
    if isinstance(value, tuple):
        op, left, right = value
        l = eval_expr(left, symbol_table)
        r = eval_expr(right, symbol_table)

        if op == 'A':
            return l + r
        elif op == 'S':
            return l - r
        elif op == 'M':
            return  l * r
        elif op == 'D':
            return l // r
        
    elif value.startswith(('0', '1', '+', '-')):
        return int(value,2)
    else:
        return symbol_table[value]
    
def int_to_binary(value):
    # Convert to binary and remove the 0b prefix
    if value < 0:
        return f"-{bin(abs(value))[2:]}"
    else:
        return bin(value)[2:]
        
def process(filename: str):
    # Input File Handling
    input_file = filename
    content = ''

    with open(input_file, 'r') as file:
        content = file.read()

    # Intialise Filtered Lexer 
    filtered_lexer = FilteredLexer(lexer)

    # Parse Input Program
    ast = parser.parse(content, lexer=filtered_lexer)
    
    # Output File Handling 
    output_file = input_file.replace('.bla', '.eva')

    # Initialise Symbol Table
    symbol_table = {}

    # Evaluate Formula
    with open(output_file, 'w') as file:
        evaluate(ast, symbol_table, file)

if __name__ == '__main__':
    # Check if correct number of args given
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        process(filename)
    else:
        print('Usage: python errors_bla.py <filename>.bla')
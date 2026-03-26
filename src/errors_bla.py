
from lex_bla import lexer, error_messages as lex_errors
from parse_bla import parser, FilteredLexer, error_messages as parse_errors
import sys

"""
Error analyser which does semantic analysis for the BLA programming language.
:author: Siyabonga Madondo
:version: 18/03/2026
"""

def semantic_analysis(ast, symbol_table):    
    # Perform Semantic Analysis
    for statement in ast[1]:
        operator, variable, value, lineno = statement

        # Check If RHS Variable in Symbol Table
        error_message = check_rhs(value, symbol_table, lineno)
        if error_message:
            return error_message

        # Check If Attempting To Reassign
        if operator == '=' and variable in symbol_table:
            error_message = f"semantic error on line {lineno}"
            return error_message
        
        # Add Value to Symbol Table
        symbol_table[variable] = value
    
    return None

def check_rhs(value, symbol_table, lineno):
    # If tuple, recurse into both operations.
    if isinstance(value, tuple):
        _, left, right = value
        error = check_rhs(left, symbol_table, lineno)
        if error: 
            return error
        return check_rhs(right, symbol_table, lineno)
    else:
        # Check if RHS variables exist in the symbol table.
        if not value.startswith(('0', '1', '+', '-')):
            if value not in symbol_table:
                return f"semantic error on line {lineno}"
    return None
                 
def process(filename : str) -> None:
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
    output_file = input_file.replace('.bla', '.err')

    with open(output_file, 'w') as file:
        if lex_errors:
            file.write(lex_errors[0])
            print(lex_errors[0])
            return
        elif parse_errors:
            file.write(parse_errors[0])
            print(parse_errors[0])
            return
    
    # Initialise Symbol Table
    symbol_table = {}

    # Perform Semantic Analysis
    error_message = semantic_analysis(ast, symbol_table)

    with open(output_file, 'w') as file:
        if error_message:
            file.write(error_message)
            print(error_message)
            return

if __name__ == '__main__':
    # Check if correct number of args given
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        process(filename)
    else:
        print('Usage: python errors_bla.py <filename>.bla')
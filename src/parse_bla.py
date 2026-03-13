import ply.yacc as yacc
from lex_bla import tokens, lexer
import sys

"""
Parser which does syntactic analysis for the BLA programming language.
:author: Siyabonga Madondo
:version: 18/03/2026
"""

class FilteredLexer:
    """
    Lexer implementation which filters out WHITESPACE and COMMENT tokens.
    """
    def __init__(self, lexer):
        self.lexer = lexer

    def token(self):
        while True:
            t = self.lexer.token()
            if not t:
                break
            if t.type not in {'WHITESPACE', 'COMMENT'}:
                return t
            
    def input(self, data):
        self.lexer.input(data)
 
# Parsing Rules (Production Rules)
def p_program(p):
    '''
    program : statements
    '''
    p[0] = ('Program', p[1])

def p_statements(p):
    '''
    statements : statements statement
               | empty
    '''
    # If given more statements, add them to the list
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_statement(p):
    '''
    statement : ID EQUALS expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression(p):
    '''
    expression : expression A term
               | expression S term
               | term
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_term(p):
    '''
    term : term M factor
         | term D factor
         | factor
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_factor(p):
    '''
    factor : LPAREN expression RPAREN
           | BINARY_LITERAL
           | ID
    '''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# Parser Initialisation
parser = yacc.yacc()

def parsing(filename: str) -> None:
    # Input File Handling
    input_file = filename
    content = ''

    with open(input_file, 'r') as file:
        content = file.read()

    # Intialise Filtered Lexer 
    filtered_lexer = FilteredLexer(lexer)

    # Parse Input Program
    ast = parser.parse(content, lexer=filtered_lexer)

    # Output File Handling (Create AST)
    output_file = input_file.replace('.bla', '.ast')

    with open(output_file, 'w') as file:
        traverse(ast, file = file)

def traverse(node: tuple, indent: int = 0, file = None) -> None:
    # Base Case: Process Leaves
    if not isinstance(node, tuple) and file:
        if node.startswith(('0', '1', '+', '-')):
            output = '\t' * indent + f'BINARY_LITERAL,{node}'
        else:
            output = '\t' * indent + f'ID,{node}'    
        print(output)
        file.write(output + '\n')
        return

    # Process Current Node
    line = '\t' * indent + node[0]
    print(line)
    if file:
        file.write(line + '\n')

    # Recurse to child nodes
    for child in node[1:]:
        if isinstance(child, list):
            for item in child:
                traverse(item, indent + 1, file)
        else:
            traverse(child, indent + 1, file)
        
if __name__ == '__main__':
    # Check if correct number of args given
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        parsing(filename)
    else:
        print('Usage: python parse_bla.py <filename>.bla')
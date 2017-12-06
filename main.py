import ast

from type_parsers import parse_statement
from tools import convert_to_string, remove_imports

def return_statements(fil):
    '''Function to return the statement tree of a python file'''

    tree = ast.parse(open(fil).read())
    return [statement for statement in tree.body]

def parse(statements):
    no_imports = remove_imports(statements)

    computed_statements = []

    for statement in no_imports:
        computed_statements.append(parse_statement(statement))
    
    return computed_statements

if __name__ == "__main__":
    file_name = "test.py"
    
    tree = return_statements(file_name)

    print(convert_to_string(tree))

    retval = parse(tree)

    print(retval)

    print('\n'.join(retval))

    

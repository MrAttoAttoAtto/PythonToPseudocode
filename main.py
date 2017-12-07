import ast

from type_parsers import parse_statement
from tools import convert_to_string, remove_imports

def return_fil_statements(fil):
    '''Function to return the statement tree of a python file'''

    tree = ast.parse(open(fil).read())
    return [statement for statement in tree.body]

def return_statements(code):
    tree = ast.parse(code)
    return [statement for statement in tree.body]

def parse(statements):
    no_imports, imports = remove_imports(statements)

    computed_statements = []

    for statement in no_imports:
        computed_statements.append(parse_statement(statement, imports))
    
    return computed_statements

def activate_shell():
    while True:
        statement = input(">>> ")

        if statement.endswith(":"):
            while True:
                next_line = input("... ")
                if next_line != '':
                    statement += "\n" + next_line
                else:
                    break


        tree = return_statements(statement)
        print('\n'.join(parse(tree)))

if __name__ == "__main__":
    #file_name = input("Filename: ")
    
    #tree = return_statements(file_name)

    #print(convert_to_string(tree))

    #retval = parse(tree)

    #print(retval)

    #print('\n'.join(retval))

    activate_shell()

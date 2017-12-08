import ast

from type_parsers import parse_statement, parse_error, ParseError
from tools import convert_to_string, remove_imports, parse_comments

def return_fil_statements(fil):
    '''Function to return the statement tree of a python file'''

    code = open(fil).read()
    tree = ast.parse(code)
    return [statement for statement in tree.body]

def return_statements(code):
    tree = ast.parse(code)
    return [statement for statement in tree.body]

def parse(statements):
    no_imports, imports = remove_imports(statements)

    computed_statements = []

    for statement in no_imports:
        try:
            computed_statements.append(parse_statement(statement, imports))
        except RecursionError:
            raise ParseError("Your code has caused the parser to exceed the maximum recursion depth, try moving things onto different lines instead of calling them all on one line.")
            computed_statements = ["ERROR, MAX RECURSTION DEPTH EXCEEDED"]
            break

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

        try:
            tree = return_statements(statement)
            print('\n'.join(parse(tree)))
        except SyntaxError as e:
            print(str(e)+"\nStatement:\n\"\n" + statement + "\n\"\nerrored.")

if __name__ == "__main__":
    #file_name = input("Filename: ")

    file_name = 'test.py'
    
    tree = return_fil_statements(file_name)

    #parse_comments(open(file_name).read())

    #print(convert_to_string(tree))

    retval = parse(tree)

    print("-------------------INPUTTED PYTHON------------------\n")

    print(open(file_name).read()+"\n")

    #print(retval)

    print("----------------OUTPUTTED PSEUDOCODE----------------\n")

    print('\n'.join(retval)+"\n")

    activate_shell()

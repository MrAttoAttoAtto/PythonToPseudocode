import ast

def convert_to_string(statements):
    '''Converts it into a nice string for printing (not that nice but whatever)'''

    return '\n\n'.join([ast.dump(statement) for statement in statements])

def remove_imports(statements):
    '''Removes all 'Import' statements, as those do not occur in pseudocode'''

    to_delete = []

    imports = []

    for index, statement in enumerate(statements):
        if isinstance(statement, ast.Import) or isinstance(statement, ast.ImportFrom):
            to_delete.append(index)
            if statement.names[0].asname == None:
                imports.append(statement.names[0].name)
            else:
                imports.append(statement.names[0].asname)

    filtered_statements = [i for j, i in enumerate(statements) if j not in to_delete]
    
    return filtered_statements, imports

def parse_comments(code):
    new_code = []

    for line in code.split('\n'):
        #if len(line.split('#')) > 1:
        new_line = line.replace("#", "__comment_private_func(", 1)
        
        if new_line != line:
            new_line += ')'
        
        new_code.append(new_line)
    
    print('\n'.join(new_code))

def evaluate_order(completed_statements):
    '''Switches up the order of the statements depending on if they were configured to be in front of others'''

    new_list = [unit.split(';;;;;') for unit in completed_statements]
    flattened = [item for sublist in new_list for item in sublist]

    return flattened
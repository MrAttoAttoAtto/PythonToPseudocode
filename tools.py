import ast

def convert_to_string(statements):
    '''Converts it into a nice string for printing (not that nice but whatever)'''

    return '\n\n'.join([ast.dump(statement) for statement in statements])

def remove_imports(statements):
    '''Removes all 'Import' statements, as those do not occurr in pseudocode'''

    to_delete = []

    for index, statement in enumerate(statements):
        if isinstance(statement, ast.Import) or isinstance(statement, ast.ImportFrom):
            to_delete.append(index)

    filtered_statements = [i for j, i in enumerate(statements) if j not in to_delete]
    
    return filtered_statements

def evaluate_order(completed_statements):
    '''Switches up the order of the statements depending on if they were configured to be in front of others'''

    new_list = [unit.split(';;;;;') for unit in completed_statements]
    flattened = [item for sublist in new_list for item in sublist]

    return flattened
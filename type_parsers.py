import ast

TYPES_SUPPORTED = {
    "Expr":"parse_expression",
    "Assign":"parse_assignment",
    "FunctionDef":"parse_function",
    "If":"parse_if",
    "Attribute":"parse_attribute",
    "Call":"parse_call",
    "Name":"parse_name",
    "Num":"parse_num",
    "Str":"parse_string",
    "Compare":"parse_compare",
    "BinOp":"parse_binary_operation",
    "str":"pass_func"
}

BINARY_OPERATORS = {
    "Add":"+",
    "Sub":"-",
    "Mult":"*",
    "MatMult":"@",
    "Div":"/",
    "Mod":"%",
    "Pow":"**",
    "LShift":"<<",
    "RShift":">>",
    "BitOr":"|",
    "BitXor":"^",
    "BitAnd":"&",
    "FloorDiv":"//"
}

IF_OPERATORS = {
    "Eq":"=",
    "NotEq":"<>",
    "Lt":"<",
    "LtE":"<=",
    "Gt":">",
    "GtE":">=",
    "In":"IN",
    "NotIn":"NOT IN"
}

def parse_statement(statement):
    '''Takes a statement and returns its completely parsed form (a string is unchanged)'''

    function_name = TYPES_SUPPORTED[type(statement).__name__]

    function = globals()[function_name]

    retval = function(statement)

    return retval

def parse_assignment(statement):
    target = parse_statement(statement.targets[0])

    value = parse_statement(statement.value)

    return "{} <- {}".format(target, value)

def parse_name(statement):
    return statement.id

def parse_num(statement):
    return str(statement.n)

def parse_string(statement):
    return '"' + statement.s + '"'

def parse_call(statement):
    func = parse_statement(statement.func)
    formatted_func = func.upper()

    args = []

    for arg in statement.args:
        args.append(parse_statement(arg))

    if len(args) != 0:
        formatted_args = ', '.join(args)
    else:
        formatted_args = ''

    if statement.keywords != []:
        print("WARNING, SOME KWARGS WILL HAVE BEEN DELETED, THESE DO NOT EXIST IN PSEUDOCODE")
    
    return "({} {})".format(formatted_func, formatted_args)

def parse_if(statement):
    test = parse_statement(statement.test)

    true_statements = []

    else_statements = []

    for true_statement in statement.body:
        true_statements.append(parse_statement(true_statement).split('\n'))

    flattened_true = [item for sublist in true_statements for item in sublist]
    
    tabbed_true_statements = ['    '+i for i in flattened_true]

    formatted_true_statements = '\n'.join(tabbed_true_statements)

    if statement.orelse == []:
        return "IF {} THEN\n{}\nENDIF".format(test, formatted_true_statements)

    else:
        for else_statement in statement.orelse:
            else_statements.append(parse_statement(else_statement).split('\n'))
        
        flattened_else = [item for sublist in else_statements for item in sublist]

        tabbed_else_statements = ['    '+i for i in flattened_else]

        formatted_else_statements = '\n'.join(tabbed_else_statements)

        return "IF {} THEN\n{}\nELSE\n{}\nENDIF".format(test, formatted_true_statements, formatted_else_statements)

def parse_compare(statement):
    left = parse_statement(statement.left)
    right = parse_statement(statement.comparators[0])

    operator = IF_OPERATORS[type(statement.ops[0]).__name__]

    return "{} {} {}".format(left, operator, right)

def parse_expression(statement):
    retval = parse_statement(statement.value)

    if type(statement.value).__name__ == "Call":
        retval = retval[1:-1]
    
    return retval

def parse_binary_operation(statement):
    left = parse_statement(statement.left)
    right = parse_statement(statement.right)

    operator = BINARY_OPERATORS[type(statement.op).__name__]

    return "{} {} {}".format(left, operator, right)

def pass_func(string):
    return string

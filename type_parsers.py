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
    "UnaryOp":"parse_unary_operation",
    "Pass":"parse_pass",
    "While":"parse_while",
    "For":"parse_for",
    "List":"parse_list",
    "Subscript":"parse_subscript",
    "Index":"parse_index",
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

UNARY_OPERATORS = {
    "Not":"NOT"
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

IMPORTS = []

def parse_statement(statement, imports=[]):
    '''Takes a statement and returns its completely parsed form (a string is unchanged)'''
    global IMPORTS

    if IMPORTS == []:
        IMPORTS = imports

    function_name = TYPES_SUPPORTED[type(statement).__name__]

    function = globals()[function_name]

    retval = function(statement)

    return retval

def parse_assignment(statement):
    target = parse_statement(statement.targets[0])

    try:
        mabs_input = parse_statement(statement.value.func)
        if mabs_input == 'input':
            args = []

            for arg in statement.value.args:
                    args.append(parse_statement(arg))

            if len(args) == 0:
                return "INPUT {}".format(target)
            else:
                return "OUTPUT {}\nINPUT {}".format(', '.join(args), target)
    except AttributeError:
        pass

    value = parse_statement(statement.value)

    return "{} <- {}".format(target, value)

def parse_name(statement):
    return statement.id

def parse_num(statement):
    return str(statement.n)

def parse_string(statement):
    return '"' + statement.s + '"'

def parse_index(statement):
    return parse_statement(statement.value)+"+1"

def parse_list(statement):
    conts = []

    for val in statement.elts:
        if type(val).__name__ == "Str":
            conts.append(parse_statement(val)[1:-1])
        else:
            conts.append(parse_statement(val))

    return str(conts)

def parse_call(statement):
    func = parse_statement(statement.func)
    formatted_func = func.upper()

    args = []

    for arg in statement.args:
        args.append(parse_statement(arg))

    if formatted_func == 'PRINT':
        formatted_func = "OUTPUT"

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

def parse_while(statement):
    test = parse_statement(statement.test)

    while_statements = []

    else_statements = []

    for while_statement in statement.body:
        while_statements.append(parse_statement(while_statement).split('\n'))

    flattened_while = [item for sublist in while_statements for item in sublist]
    
    tabbed_while_statements = ['    '+i for i in flattened_while]

    formatted_while_statements = '\n'.join(tabbed_while_statements)

    if statement.orelse == []:
        return "WHILE {} DO\n{}\nENDWHILE".format(test, formatted_while_statements)

    else:
        for else_statement in statement.orelse:
            else_statements.append(parse_statement(else_statement).split('\n'))
        
        flattened_else = [item for sublist in else_statements for item in sublist]

        tabbed_else_statements = ['    '+i for i in flattened_else]

        formatted_else_statements = '\n'.join(tabbed_else_statements)

        return "WHILE {} DO\n{}\nELSE\n{}\nENDWHILE".format(test, formatted_while_statements, formatted_else_statements)

def parse_for(statement):
    target = parse_statement(statement.target)

    try:
        func_id = statement.iter.func.id
    except AttributeError:
        func_id = None
    
    if func_id == 'range':
        args = statement.iter.args
        if len(args) == 1:
            bound = parse_statement(args[0])
            inter_iterate = '0 TO {}'.format(bound)
        elif len(args) == 2:
            bot_bound = parse_statement(args[0])
            top_bound = parse_statement(args[1])
            inter_iterate = "{} TO {}".format(bot_bound, top_bound)
        
        iterate = "{} <- {}".format(target, inter_iterate)
    else:
        inter_iterate = parse_statement(statement.iter)
        iterate = "{} IN {}".format(target, inter_iterate)
    
    for_statements = []

    else_statements = []

    for for_statement in statement.body:
        for_statements.append(parse_statement(for_statement).split('\n'))

    flattened_for = [item for sublist in for_statements for item in sublist]
    
    tabbed_for_statements = ['    '+i for i in flattened_for]

    formatted_for_statements = '\n'.join(tabbed_for_statements)

    if statement.orelse == []:
        return "FOR {} DO\n{}\nENDFOR".format(iterate, formatted_for_statements)

    else:
        for else_statement in statement.orelse:
            else_statements.append(parse_statement(else_statement).split('\n'))
        
        flattened_else = [item for sublist in else_statements for item in sublist]

        tabbed_else_statements = ['    '+i for i in flattened_else]

        formatted_else_statements = '\n'.join(tabbed_else_statements)

        return "for {} DO\n{}\nELSE\n{}\nENDFOR".format(iterate, formatted_for_statements, formatted_else_statements)


def parse_expression(statement):
    retval = parse_statement(statement.value)

    if type(statement.value).__name__ == "Call":
        retval = retval[1:-1]
    
    return retval

def parse_attribute(statement):
    base = parse_statement(statement.value)
    attr = statement.attr

    if base in IMPORTS:
        return "{}".format(attr)
    else:
        return "{}.{}".format(base, attr)

def parse_binary_operation(statement):
    left = parse_statement(statement.left)
    right = parse_statement(statement.right)

    operator = BINARY_OPERATORS[type(statement.op).__name__]

    return "{} {} {}".format(left, operator, right)

def parse_unary_operation(statement):
    target = parse_statement(statement.operand)

    operator = UNARY_OPERATORS[type(statement.op).__name__]

    return "{} {}".format(operator, target)

def parse_subscript(statement):
    base = parse_statement(statement.value)
    index = parse_statement(statement.slice)

    return "{}[{}]".format(base, index)

def parse_pass(statement):
    return 'PASS'

def pass_func(string):
    return string

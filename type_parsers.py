import ast

TYPES_SUPPORTED = {
    "Expr":"parse_expression",
    "Assign":"parse_assignment",
    "FunctionDef":"parse_function",
    "Return":"parse_return",
    "Break":"parse_break",
    "Continue":"parse_continue",
    "If":"parse_if",
    "Attribute":"parse_attribute",
    "Call":"parse_call",
    "Name":"parse_name",
    "Num":"parse_num",
    "Str":"parse_string",
    "Compare":"parse_compare",
    "BinOp":"parse_binary_operation",
    "UnaryOp":"parse_unary_operation",
    "BoolOp":"parse_boolean_operation",
    "Pass":"parse_pass",
    "While":"parse_while",
    "For":"parse_for",
    "List":"parse_list",
    "Subscript":"parse_subscript",
    "Index":"parse_index",
    "NameConstant":"parse_name_constant",
    "Tuple":"parse_list",
    "AugAssign":"parse_augmented_assignment",
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
    "Not":"NOT ",
    "USub":"-",
    "Invert":"~"
}

BOOLEAN_OPERATORS = {
    "And":"AND",
    "Or":"OR"
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

SPECIAL_FUNCTIONS = {
    "INPUT":"parse_input"
}

LOCAL_FUNCTIONS = []

IMPORTS = []

class ParseError(Exception):
    pass

def parse_error(error, info, extd_info):
    if error == 'key':
        string = "Unfortunately, a command you tried to parse is not supported ({}). The code pertaining to this command is: {}".format(info, extd_info)
    elif error == 'input':
        string = "Unfortunately, input can only be used for assignment within pseudocode. The code pertaining to this command is: {}".format(extd_info)
    return string    

def parse_statement(statement, imports=[]):
    '''Takes a statement and returns its completely parsed form (a string is unchanged)'''
    global IMPORTS

    if IMPORTS == []:
        IMPORTS = imports

    #print(statement)

    try:
        function_name = TYPES_SUPPORTED[type(statement).__name__]
    except KeyError:
        error = parse_error("key", type(statement).__name__, ast.dump(statement))
        raise ParseError(error)

    function = globals()[function_name]

    retval = function(statement)

    return retval

def parse_assignment(statement, operator=None):
    try:
        target = parse_statement(statement.targets[0])
    except AttributeError:
        target = parse_statement(statement.target)

    try:
        mabs_input = parse_statement(statement.value.func)
        if mabs_input == 'input':
            args = []

            for arg in statement.value.args:
                args.append(parse_statement(arg))

            if len(args) == 0:
                if operator is None:
                    return "INPUT {}".format(target)
                else:
                    return "INPUT temp\n{} <- {} {} temp".format(target, target, operator)
            else:
                formatted_args = ', '.join(args)

                formatted_args = formatted_args.replace(" + ", ", ")
                formatted_args = formatted_args.replace("\n", "\\n")
                if operator is not None:
                    return "OUTPUT {}\nINPUT temp\n{} <- {} {} temp".format(formatted_args, target, target, operator)
                else:
                    return "OUTPUT {}\nINPUT {}".format(formatted_args, target)
                
    except AttributeError:
        pass

    value = parse_statement(statement.value)

    if operator is None:
        return "{} <- {}".format(target, value)
    else:
        return "{} <- {} {} {}".format(target, target, operator, value)

def parse_name(statement):
    return statement.id

def parse_num(statement):
    return str(statement.n)

def parse_string(statement):
    return '"' + statement.s + '"'

def parse_index(statement):
    try:
        return str(int(parse_statement(statement.value))+1)
    except ValueError:
        return parse_statement(statement.value)+"+1"

def parse_name_constant(statement):
    return str(statement.value).upper()

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

    if formatted_func == "INPUT":
        error = parse_error("input", None, ast.dump(statement))
        raise ParseError(error)

    for arg in statement.args:
        args.append(parse_statement(arg))

    if len(args) != 0:
        formatted_args = ', '.join(args)
    else:
        formatted_args = ''

    if formatted_func == 'PRINT':
        formatted_func = "OUTPUT"
        formatted_args = formatted_args.replace(" + ", ", ")
        formatted_args = formatted_args.replace("\n", "\\n")

    elif formatted_func == '__COMMENT_PRIVATE_FUNC':
        return "//{}".format(formatted_args)

    if statement.keywords != []:
        print("WARNING, SOME KWARGS WILL HAVE BEEN DELETED, THESE DO NOT EXIST IN PSEUDOCODE")

    if args == []:
        return "({})".format(formatted_func)
    else:
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
        return "WHILE {}\n{}\nENDWHILE".format(test, formatted_while_statements)

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
            inter_iterate = '1 TO {}'.format(bound)
        elif len(args) == 2:
            bot_bound = parse_statement(args[0]) + 1
            top_bound = parse_statement(args[1])
            inter_iterate = "{} TO {}".format(bot_bound, top_bound)
        elif len(args) == 3:
            bot_bound = parse_statement(args[0]) + 1
            top_bound = parse_statement(args[1])
            step = parse_statement(args[2])
            inter_iterate = "{} TO {} STEP {}".format(bot_bound, top_bound, step)
        
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
        return "FOR {}\n{}\nNEXT {}".format(iterate, formatted_for_statements, target)

    else:
        for else_statement in statement.orelse:
            else_statements.append(parse_statement(else_statement).split('\n'))
        
        flattened_else = [item for sublist in else_statements for item in sublist]

        tabbed_else_statements = ['    '+i for i in flattened_else]

        formatted_else_statements = '\n'.join(tabbed_else_statements)

        return "FOR {}\n{}\nELSE\n{}\nNEXT {}".format(iterate, formatted_for_statements, formatted_else_statements, target)


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

    return "{}{}".format(operator, target)

def parse_boolean_operation(statement):
    statements = []

    operator = BOOLEAN_OPERATORS[type(statement.op).__name__]

    for eval_statement in statement.values:
        statements.append(parse_statement(eval_statement))
    
    return ' {} '.format(operator).join(statements)

def parse_subscript(statement):
    base = parse_statement(statement.value)
    index = parse_statement(statement.slice)

    return "{}[{}]".format(base, index)

def parse_augmented_assignment(statement):
    operator = BINARY_OPERATORS[type(statement.op).__name__]

    return parse_assignment(statement, operator)

def parse_pass(statement):
    return 'PASS'

def parse_function(statement):
    func = statement.name

    args = []

    for arg in statement.args.args:
        args.append(arg.arg)

    formatted_args = ', '.join(args)

    func_statements = []

    for func_statement in statement.body:
        func_statements.append(parse_statement(func_statement).split('\n'))

    flattened_func = [item for sublist in func_statements for item in sublist]
    
    tabbed_func_statements = ['    '+i for i in flattened_func]

    formatted_func_statements = '\n'.join(tabbed_func_statements)

    LOCAL_FUNCTIONS.append(func)
    
    return "FUNCTION {}({})\n{}\nENDFUNCTION".format(func, formatted_args, formatted_func_statements)

def parse_return(statement):
    return "RETURN {}".format(parse_statement(statement.value))

def parse_break(statement):
    return "BREAK"

def parse_continue(statement):
    return "CONTINUE"

def pass_func(string):
    return string

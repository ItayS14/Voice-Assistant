from py_expression_eval import Parser

def calculate(num1,op,num2=None,base=10):
    """
    This function will calculate the result of the mathematical expression
    :param num1: the first number in the calculation (float or int)
    :param op: the operation to perform on the two numbers (for example, '+') (str)
    :param num2: the second number in the calculation (float or int)
    :param base: the base to use in the log operation (float or int, only relevant in log operations)
    :return: the result of the calculation (float or int)
    """
    parser = Parser() 
    exp = ""
    # Only one parameter was given and the one parameter operations need to be used
    if num2:
        exp =  f"{num1} {op} {num2}"
    # Ignore the second number and use the base instead
    elif op == 'log':
            exp = f"{op}({num1},{base})"
    else:
        exp = f"{op}({num1})"
        
    # Currently, does not support equations.
    return parser.parse(exp).evaluate({})


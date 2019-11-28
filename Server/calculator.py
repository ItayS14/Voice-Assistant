from py_expression_eval import Parser

ONE_PARAM_OPS = ['','log','cos','sin','tan','abs','asin','acos','atan']


def calculate(num1,op,num2=0,base=10):
    """
    This function will calculate the result of the mathematical expression
    :param num1: the first number in the calculation (float or int)
    :param op: the operation to perform on the two numbers (for example, '+') (str)
    :param num2: the second number in the calculation (float or int)
    :param base: the base to use in the log operation (float or int, only relevant in log operations)
    :return: the result of the calculation (float or int)
    """
    if not isinstance(num1,(int,float)) or not (isinstance(num2,(int,float)) or num2 is None) or not isinstance(op,(str,)):
        raise TypeError("Can't perform operation (Invalid types)!")
    parser = Parser() 
    exp = ""
    if op in ONE_PARAM_OPS:
        # Ignore the second number and use the base instead
        if op == 'log':
            exp = f"{op}({num1},{base})"
        else:
            exp = f"{op}({num1})"
    else:
        if num2 == None:
            raise TypeError("Too few arguments!")
        exp =  f"{num1} {op} {num2}"
    # Currently, does not support equations.
    return parser.parse(exp).evaluate({})

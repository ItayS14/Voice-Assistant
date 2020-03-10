from py_expression_eval import Parser

def calculate(expression):
    """
    This function will calculate the result of the mathematical expression
    :param expression: the expression to be calculated/evaluated (str)
    :return: the result of the calculation (float or int)
    """
    parser = Parser() 
    return parser.parse(expression).evaluate({})


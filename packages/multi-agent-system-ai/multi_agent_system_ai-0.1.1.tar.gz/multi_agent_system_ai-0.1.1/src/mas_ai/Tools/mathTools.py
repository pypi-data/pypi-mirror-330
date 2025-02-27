from langchain.tools import tool



@tool('Calculator',return_direct=False)
def Calculator(expression : str):
    """Calculator takes variable `expression` as mathematical string and evaluates it for answer."""
    try:
        return eval(expression)
    except Exception as e:
        return e
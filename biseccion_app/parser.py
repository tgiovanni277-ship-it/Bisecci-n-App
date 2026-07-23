from sympy import sympify, symbols
from sympy.utilities.lambdify import lambdify
import numpy as np

x = symbols('x')

class ParseError(Exception):
    pass

def parse_function(expr_text: str):
    """Convierte una expresión en texto a una función numérica (vectorizable con numpy).

    Retorna (callable f, sympy_expr)
    """
    try:
        expr = sympify(expr_text)
        f = lambdify(x, expr, modules=["numpy"])
        # test a tiny evaluation to detect errores tempranos
        test_val = f(0.0)
        # allow numpy arrays, so no further checking here
        return f, expr
    except Exception as e:
        raise ParseError(f"Error al parsear la función: {e}")

from dataclasses import dataclass
from typing import Callable, List, Dict, Any
import math
import numpy as np

@dataclass
class BisectionResult:
    root: float
    iterations: List[Dict[str, Any]]
    final_error: float
    f_root: float

class BisectionError(Exception):
    pass


def run_bisection(func: Callable[[float], float], a: float, b: float, tol: float = 1e-6, max_iter: int = 50) -> BisectionResult:
    """Ejecuta el método de bisección y devuelve todas las iteraciones.

    Cada iteración es un dict con: i, a, b, m, fa, fm, fb, error
    error = |m - prev_m| (None en la primera iteración)
    """
    try:
        fa = float(func(a))
        fb = float(func(b))
    except Exception as e:
        raise BisectionError(f"Error al evaluar f(a) o f(b): {e}")

    if math.isnan(fa) or math.isnan(fb):
        raise BisectionError("f(a) o f(b) es NaN")

    if fa * fb > 0:
        raise BisectionError("f(a) y f(b) deben tener signos opuestos (o uno debe ser cero).")

    iterations = []
    prev_m = None
    for i in range(1, max_iter + 1):
        m = (a + b) / 2.0
        try:
            fm = float(func(m))
        except Exception as e:
            raise BisectionError(f"Error al evaluar f(m) en iteración {i}: {e}")

        error = abs(m - prev_m) if prev_m is not None else None

        iterations.append({
            'i': i,
            'a': a,
            'b': b,
            'm': m,
            'fa': fa,
            'fm': fm,
            'fb': fb,
            'error': error,
        })

        # criterio de parada: |f(m)| < tol o cambio en m menor que tol
        if abs(fm) < tol or (error is not None and error < tol):
            break

        # actualizar intervalo
        if fa * fm < 0:
            b = m
            fb = fm
        else:
            a = m
            fa = fm

        prev_m = m

    final_root = iterations[-1]['m']
    final_error = abs(iterations[-1]['error']) if iterations[-1]['error'] is not None else 0.0
    final_froot = float(func(final_root))

    return BisectionResult(root=final_root, iterations=iterations, final_error=final_error, f_root=final_froot)

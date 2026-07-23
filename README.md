# Bisecci-n-App
Proyecto Python que implementa el método de bisección con interfaz gráfica (Tkinter).

Características:
- Permite ingresar una función como texto (ej. `x**3 - 4*x + 1`).
- Ingresar intervalo `a` y `b`, tolerancia y número máximo de iteraciones.
- Muestra, por cada iteración: a, b, punto medio m, f(a), f(m), f(b) y error.
- Muestra resultados finales: raíz aproximada, número de iteraciones, error final y verificación |f(m)|.
- Gráfica de la función y el intervalo, destacando la raíz.

Requisitos:
- Python 3.8+
- Instalar dependencias:

```
pip install -r requirements.txt
```

Uso:

```
python run.py
```

Archivo principal de GUI: `biseccion_app/gui.py`.

Notas:
- La GUI usa Tkinter (incluido en la stdlib) y matplotlib para la gráfica.
- El parser de expresiones usa SymPy para mayor seguridad en la conversión a función numérica.

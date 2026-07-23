import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from typing import Optional
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from .parser import parse_function, ParseError
from .core import run_bisection, BisectionError


class BisectionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bisección - Resolver ecuaciones no lineales")
        self.geometry('950x650')
        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self)
        frm.pack(fill='both', expand=True, padx=8, pady=8)

        # Inputs
        left = ttk.Frame(frm)
        left.pack(side='left', fill='y')

        ttk.Label(left, text='Función f(x):').grid(row=0, column=0, sticky='w')
        self.func_entry = ttk.Entry(left, width=40)
        self.func_entry.insert(0, 'x**3 - 4*x + 1')
        self.func_entry.grid(row=1, column=0, pady=4)

        row = 2
        ttk.Label(left, text='a:').grid(row=row, column=0, sticky='w')
        self.a_entry = ttk.Entry(left, width=20)
        self.a_entry.insert(0, '-3')
        self.a_entry.grid(row=row+1, column=0, sticky='w', pady=2)

        ttk.Label(left, text='b:').grid(row=row+2, column=0, sticky='w')
        self.b_entry = ttk.Entry(left, width=20)
        self.b_entry.insert(0, '3')
        self.b_entry.grid(row=row+3, column=0, sticky='w', pady=2)

        ttk.Label(left, text='Tolerancia:').grid(row=row+4, column=0, sticky='w')
        self.tol_entry = ttk.Entry(left, width=20)
        self.tol_entry.insert(0, '1e-6')
        self.tol_entry.grid(row=row+5, column=0, sticky='w', pady=2)

        ttk.Label(left, text='Iteraciones máximas:').grid(row=row+6, column=0, sticky='w')
        self.maxit_entry = ttk.Entry(left, width=20)
        self.maxit_entry.insert(0, '50')
        self.maxit_entry.grid(row=row+7, column=0, sticky='w', pady=2)

        btn_frame = ttk.Frame(left)
        btn_frame.grid(row=row+8, column=0, pady=8)
        calc_btn = ttk.Button(btn_frame, text='Calcular', command=self.on_calculate)
        calc_btn.pack(side='left', padx=4)
        clear_btn = ttk.Button(btn_frame, text='Limpiar', command=self.clear_results)
        clear_btn.pack(side='left', padx=4)

        # Results (table)
        right = ttk.Frame(frm)
        right.pack(side='left', fill='both', expand=True)

        # Treeview for iterations
        cols = ('i', 'a', 'b', 'm', 'fa', 'fm', 'fb', 'error')
        self.tree = ttk.Treeview(right, columns=cols, show='headings', height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=90, anchor='center')
        self.tree.pack(fill='x')

        # Summary
        self.summary = ScrolledText(right, height=6)
        self.summary.pack(fill='x', pady=6)

        # Plot area
        fig = Figure(figsize=(6,4), dpi=100)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=right)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def clear_results(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.summary.delete('1.0', tk.END)
        self.ax.clear()
        self.canvas.draw()

    def on_calculate(self):
        expr = self.func_entry.get().strip()
        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tol = float(self.tol_entry.get())
            maxit = int(self.maxit_entry.get())
        except Exception as e:
            messagebox.showerror('Entrada inválida', f'Error en entradas numéricas: {e}')
            return

        try:
            func, sympy_expr = parse_function(expr)
        except ParseError as e:
            messagebox.showerror('Error al parsear función', str(e))
            return

        # ejecutar bisección
        try:
            result = run_bisection(func, a, b, tol=tol, max_iter=maxit)
        except BisectionError as e:
            messagebox.showerror('Error en bisección', str(e))
            return
        except Exception as e:
            messagebox.showerror('Error inesperado', str(e))
            return

        # mostrar iteraciones
        for item in self.tree.get_children():
            self.tree.delete(item)
        for it in result.iterations:
            # format numbers
            self.tree.insert('', 'end', values=(
                it['i'],
                f"{it['a']:.6g}",
                f"{it['b']:.6g}",
                f"{it['m']:.6g}",
                f"{it['fa']:.6g}",
                f"{it['fm']:.6g}",
                f"{it['fb']:.6g}",
                f"{it['error']:.6g}" if it['error'] is not None else 'N/A'
            ))

        # resumen final
        self.summary.delete('1.0', tk.END)
        s = []
        s.append(f"Raíz aproximada: {result.root:.12g}")
        s.append(f"Número de iteraciones: {len(result.iterations)}")
        s.append(f"Error final (|Δm|): {result.final_error:.6g}")
        s.append(f"|f(root)| = {abs(result.f_root):.6g}")
        self.summary.insert(tk.END, "\n".join(s))

        # gráfica
        self._plot_function(func, a, b, result.root)

    def _plot_function(self, func, a, b, root: Optional[float]):
        try:
            self.ax.clear()
            # rango para graficar
            span = b - a
            xmin = a - 0.2 * abs(span) if span != 0 else a - 1
            xmax = b + 0.2 * abs(span) if span != 0 else b + 1
            xs = np.linspace(xmin, xmax, 1000)
            ys = func(xs)
            # try to convert to numpy array
            ys = np.array(ys, dtype=float)
            self.ax.plot(xs, ys, label='f(x)')
            # highlight interval
            self.ax.axvline(a, color='orange', linestyle='--', label='a')
            self.ax.axvline(b, color='orange', linestyle='--', label='b')
            # root marker
            self.ax.scatter([root], [func(root)], color='red', zorder=5, label='raíz (aprox)')
            self.ax.axhline(0, color='black', linewidth=0.6)
            self.ax.legend()
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('f(x)')
            self.ax.set_title('Gráfica de f(x) y raíz aproximada')
            self.canvas.draw()
        except Exception as e:
            messagebox.showwarning('Advertencia gráfica', f'No se pudo generar la gráfica: {e}')


def main():
    app = BisectionApp()
    app.mainloop()

if __name__ == '__main__':
    main()

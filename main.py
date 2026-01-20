import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime, date
import csv

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models import (
    obtener_cartuchos_activos,
    cambiar_cartucho,
    guardar_copias,
    reporte_cartuchos,
    historial_copias
)

COLOR_MAP = {
    "C": "#00B7EB",
    "M": "#E6007E",
    "Y": "#FFD300",
    "K": "#000000"
}

def parse_fecha(texto):
    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        return None


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control de copias")
        self.geometry("950x820")
        self.resizable(False, False)

        # ===== CONTENEDORES (CENTRADOS) =====
        self.cartuchos_frame = tk.LabelFrame(self, text="Cartuchos", padx=15, pady=10)
        self.cartuchos_frame.pack(anchor="center", padx=10, pady=6)

        self.copias_frame = tk.LabelFrame(self, text="Registro de copias", padx=15, pady=10)
        self.copias_frame.pack(anchor="center", padx=10, pady=6)

        self.reporte_frame = tk.LabelFrame(self, text="Reporte por cartucho", padx=15, pady=10)
        self.reporte_frame.pack(anchor="center", padx=10, pady=6)

        self.grafica_frame = tk.LabelFrame(self, text="Gráfica de consumo", padx=15, pady=10)
        self.grafica_frame.pack(anchor="center", padx=10, pady=6)

        self.historial_frame = tk.LabelFrame(self, text="Últimas copias", padx=15, pady=10)
        self.historial_frame.pack(anchor="center", padx=10, pady=6)

        self.canvas = None

        self.dibujar_cartuchos()
        self.dibujar_copias()
        self.actualizar()

    # =====================================================
    # CARTUCHOS
    # =====================================================
    def dibujar_cartuchos(self):
        for w in self.cartuchos_frame.winfo_children():
            w.destroy()

        activos = obtener_cartuchos_activos()
        hoy = date.today().isoformat()

        fila = tk.Frame(self.cartuchos_frame)
        fila.pack(anchor="center")

        for color in ("C", "M", "Y", "K"):
            sub = tk.Frame(fila, padx=25)
            sub.pack(side="left")

            activo = color in activos
            bg = COLOR_MAP[color] if activo else "#CCCCCC"

            tk.Label(sub, width=3, height=1, bg=bg, relief="solid").pack()
            tk.Label(sub, text=color, font=("Arial", 10, "bold")).pack()

            if activo:
                tk.Label(sub, text=f"Desde:\n{activos[color]}").pack()

            fecha_var = tk.StringVar(value=hoy)
            tk.Entry(sub, textvariable=fecha_var, width=10, justify="center").pack(pady=2)

            tk.Button(
                sub,
                text="Cambiar",
                command=lambda c=color, f=fecha_var: self.cambiar_cartucho_ui(c, f)
            ).pack(pady=3)

    def cambiar_cartucho_ui(self, color, fecha_var):
        fecha = parse_fecha(fecha_var.get())
        if not fecha:
            messagebox.showerror("Error", "Fecha inválida (YYYY-MM-DD)")
            return
        cambiar_cartucho(color, fecha)
        self.actualizar()

    # =====================================================
    # COPIAS
    # =====================================================
    def dibujar_copias(self):
        hoy = date.today().isoformat()

        tk.Label(self.copias_frame, text="Fecha").grid(row=0, column=0, padx=5)
        self.fecha_var = tk.StringVar(value=hoy)
        tk.Entry(self.copias_frame, textvariable=self.fecha_var, width=12, justify="center")\
            .grid(row=0, column=1, padx=5)

        tk.Label(self.copias_frame, text="B/N").grid(row=0, column=2)
        self.bn_var = tk.IntVar(value=0)
        tk.Spinbox(self.copias_frame, from_=0, to=100000, textvariable=self.bn_var, width=8)\
            .grid(row=0, column=3, padx=5)

        tk.Label(self.copias_frame, text="Color").grid(row=0, column=4)
        self.color_var = tk.IntVar(value=0)
        tk.Spinbox(self.copias_frame, from_=0, to=100000, textvariable=self.color_var, width=8)\
            .grid(row=0, column=5, padx=5)

        tk.Label(self.copias_frame, text="Descripción").grid(row=1, column=0, pady=5)
        self.desc = tk.Entry(self.copias_frame, width=60)
        self.desc.grid(row=1, column=1, columnspan=5, pady=5)

        tk.Button(
            self.copias_frame,
            text="Guardar copias",
            width=20,
            command=self.guardar
        ).grid(row=2, column=0, columnspan=6, pady=8)

    def guardar(self):
        fecha = parse_fecha(self.fecha_var.get())
        if not fecha:
            messagebox.showerror("Error", "Fecha inválida")
            return

        activos = obtener_cartuchos_activos()

        if self.bn_var.get() > 0 and "K" not in activos:
            messagebox.showerror("Error", "No hay cartucho negro")
            return

        if self.color_var.get() > 0 and not all(c in activos for c in "CMYK"):
            messagebox.showerror("Error", "Faltan cartuchos CMYK")
            return

        if self.bn_var.get() == 0 and self.color_var.get() == 0:
            messagebox.showerror("Error", "No hay copias")
            return

        guardar_copias(fecha, self.bn_var.get(), self.color_var.get(), self.desc.get())

        self.bn_var.set(0)
        self.color_var.set(0)
        self.desc.delete(0, tk.END)

        self.actualizar()

    # =====================================================
    # REPORTES
    # =====================================================
    def dibujar_reportes(self):
        for w in self.reporte_frame.winfo_children():
            w.destroy()

        for color, inicio, fin, copias in reporte_cartuchos():
            dias = (fin - inicio).days + 1
            media = round((copias or 0) / dias, 2)

            tk.Label(
                self.reporte_frame,
                text=f"{color} | {inicio} → {fin} | {copias or 0} copias | {media}/día",
                anchor="w"
            ).pack(fill="x")

        tk.Button(
            self.reporte_frame,
            text="Exportar reporte (CSV)",
            command=self.exportar_reporte
        ).pack(pady=5)

    def exportar_reporte(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".csv")
        if not ruta:
            return

        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Color", "Inicio", "Fin", "Copias"])

            for c, i, f_, cop in reporte_cartuchos():
                writer.writerow([c, i, f_, cop or 0])

        messagebox.showinfo("OK", "Reporte exportado")

    # =====================================================
    # GRÁFICA
    # =====================================================
    def dibujar_grafica(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        datos = {c: 0 for c in "CMYK"}
        for color, _, _, copias in reporte_cartuchos():
            datos[color] += copias or 0

        colores = [COLOR_MAP[c] for c in datos.keys()]

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(datos.keys(), datos.values(), color=colores)
        ax.set_ylabel("Copias")
        ax.set_title("Consumo por cartucho")

        self.canvas = FigureCanvasTkAgg(fig, master=self.grafica_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(anchor="center")

    # =====================================================
    # HISTORIAL
    # =====================================================
    def dibujar_historial(self):
        for w in self.historial_frame.winfo_children():
            w.destroy()

        for f, bn, col, d in historial_copias():
            tk.Label(
                self.historial_frame,
                text=f"{f} | BN:{bn} | Color:{col} | {d}",
                anchor="w"
            ).pack(fill="x")

    # =====================================================
    # ACTUALIZACIÓN GENERAL
    # =====================================================
    def actualizar(self):
        self.dibujar_cartuchos()
        self.dibujar_reportes()
        self.dibujar_grafica()
        self.dibujar_historial()


if __name__ == "__main__":
    App().mainloop()

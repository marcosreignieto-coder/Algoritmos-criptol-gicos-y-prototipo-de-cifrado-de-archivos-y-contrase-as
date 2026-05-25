"""Lanzador principal de la aplicación de ataques.

La interfaz y los módulos internos están organizados dentro de la carpeta
`programa_ataques` para mantener limpia la carpeta principal.
"""

from programa_ataques.interfaz import AttackApp


if __name__ == "__main__":
    app = AttackApp()
    app.mainloop()

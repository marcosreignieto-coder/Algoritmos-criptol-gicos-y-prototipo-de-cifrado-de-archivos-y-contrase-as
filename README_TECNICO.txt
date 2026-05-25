"""Interfaz roja para la página de ataque de Cripto App.

Ejecución:
    python app_ataques.py
"""

from __future__ import annotations

import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .config import UI_PROGRESS_INTERVAL_SECONDS
from .attack_algorithms import (
    AttackError,
    AttackStats,
    attack_bruteforce,
    attack_caesar_bruteforce,
    attack_dictionary,
    attack_header,
    attack_intelligent,
    attack_password_full,
    attack_png_auto,
    attack_recurrent,
    get_algorithm,
)

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
ATTACKED_IMAGES_DIR = PROJECT_DIR / "imagenes_atacadas"
ICON_PATH = BASE_DIR / "app_icon.ico"

ENCRYPTED_TYPES = (
    ("Archivos cifrados", "*.encfile *.encimg"),
    ("Todos los archivos", "*.*"),
)

ATTACK_OPTIONS = (
    "Automático recomendado",
    "César - fuerza bruta 256 desplazamientos",
    "Ataque por cabecera PNG (César/Vigenère)",
    "Ataque completo por contraseña",
    "Ataque inteligente",
    "Claves recurrentes",
    "Diccionario por librería + mutaciones",
    "Fuerza bruta limitada",
)

PASSWORD_TYPE_OPTIONS = (
    "Cualquiera",
    "Numérica",
    "Alfabética (español)",
    "Alfanumérica",
    "Alfanumérica con símbolos",
)


class AttackApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Cripto App - Ataques")
        self.geometry("980x840")
        self.minsize(900, 700)
        self.configure(bg="#1a0b0b")

        if ICON_PATH.exists():
            try:
                self.iconbitmap(str(ICON_PATH))
            except tk.TclError:
                pass

        ATTACKED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

        self.encrypted_path = tk.StringVar()
        self.detected_algorithm = tk.StringVar(value="Sin detectar")
        self.attack_selected = tk.StringVar(value=ATTACK_OPTIONS[0])
        self.dictionary_path = tk.StringVar()
        self.min_password_len = tk.StringVar(value="1")
        self.max_password_len = tk.StringVar(value="32")
        self.password_type_filter = tk.StringVar(value=PASSWORD_TYPE_OPTIONS[0])
        self.max_hours = tk.StringVar(value="4")
        self.max_iterations = tk.StringVar(value="1000000")
        self.status = tk.StringVar(value=f"Carpeta de imágenes atacadas: {ATTACKED_IMAGES_DIR}")

        self.total_tests = tk.StringVar(value="0")
        self.current_rate = tk.StringVar(value="0.00")
        self.average_rate = tk.StringVar(value="0.00")
        self.min_rate = tk.StringVar(value="0.00")
        self.max_rate = tk.StringVar(value="0.00")
        self.found_value = tk.StringVar(value="-")
        self.password_length = tk.StringVar(value="-")
        self.password_type = tk.StringVar(value="-")
        self.current_test = tk.StringVar(value="-")

        self._attack_thread: threading.Thread | None = None
        self._stop_requested = False
        self._attack_started_at: float | None = None
        self._max_seconds: float | None = None
        self._last_progress_ui = 0.0
        self._last_progress_total = 0
        self.start_button: ttk.Button | None = None
        self.stop_button: ttk.Button | None = None

        self._configure_style()
        self._build_ui()

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Main.TFrame", background="#1a0b0b")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Panel.TFrame", background="#fff7f7", relief="flat")
        style.configure("Title.TLabel", background="#1a0b0b", foreground="#fee2e2", font=("Segoe UI", 24, "bold"))
        style.configure("Subtitle.TLabel", background="#1a0b0b", foreground="#fecaca", font=("Segoe UI", 11))
        style.configure("CardTitle.TLabel", background="#ffffff", foreground="#7f1d1d", font=("Segoe UI", 15, "bold"))
        style.configure("CardText.TLabel", background="#ffffff", foreground="#334155", font=("Segoe UI", 10))
        style.configure("PanelTitle.TLabel", background="#fff7f7", foreground="#7f1d1d", font=("Segoe UI", 16, "bold"))
        style.configure("PanelText.TLabel", background="#fff7f7", foreground="#334155", font=("Segoe UI", 10))
        style.configure("StatLabel.TLabel", background="#ffffff", foreground="#7f1d1d", font=("Segoe UI", 9, "bold"))
        style.configure("StatValue.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 17, "bold"))
        style.configure("TLabel", font=("Segoe UI", 10), background="#fff7f7", foreground="#111827")
        style.configure("TEntry", padding=7)
        style.configure("TCombobox", padding=7)
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=10)
        style.configure("Secondary.TButton", font=("Segoe UI", 10), padding=8)
        style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), padding=10)
        style.configure("Status.TLabel", background="#450a0a", foreground="#fee2e2", padding=10, font=("Segoe UI", 9))

    def _build_ui(self) -> None:
        main = ttk.Frame(self, style="Main.TFrame", padding=24)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Cripto App - Ataques", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            main,
            text="Página de ataque con la misma estructura visual que el cifrador, en versión roja. Incluye ataques por cabecera, diccionario por librería, claves recurrentes y fuerza bruta limitada.",
            style="Subtitle.TLabel",
            wraplength=860,
        ).pack(anchor="w", pady=(4, 18))

        cards = ttk.Frame(main, style="Main.TFrame")
        cards.pack(fill="x", pady=(0, 16))
        self._small_card(cards, "Ataques activos", "Cabecera PNG · inteligente · diccionario · fuerza bruta limitada", 0)
        self._small_card(cards, "Entrada", "Archivo .encfile generado por la app", 1)
        self._small_card(cards, "Salida", "Carpeta exterior imagenes_atacadas", 2)
        cards.columnconfigure((0, 1, 2), weight=1)

        panel = ttk.Frame(main, style="Panel.TFrame", padding=20)
        panel.pack(fill="both", expand=True)
        self._build_attack_panel(panel)

        ttk.Label(main, textvariable=self.status, style="Status.TLabel", anchor="w").pack(fill="x", pady=(14, 0))

    def _small_card(self, parent: ttk.Frame, title: str, text: str, column: int) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=14)
        card.grid(row=0, column=column, sticky="ew", padx=6)
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text=text, style="CardText.TLabel", wraplength=245).pack(anchor="w", pady=(3, 0))

    def _build_attack_panel(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(1, weight=1)
        ttk.Label(parent, text="Atacar archivo PNG cifrado", style="PanelTitle.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 14)
        )

        ttk.Label(parent, text="Archivo cifrado:", style="PanelText.TLabel").grid(row=1, column=0, sticky="w", pady=7)
        ttk.Entry(parent, textvariable=self.encrypted_path).grid(row=1, column=1, sticky="ew", padx=10, pady=7)
        ttk.Button(parent, text="Buscar cifrado", style="Secondary.TButton", command=self.select_encrypted).grid(
            row=1, column=2, pady=7
        )

        ttk.Label(parent, text="Algoritmo detectado:", style="PanelText.TLabel").grid(row=2, column=0, sticky="w", pady=7)
        ttk.Label(parent, textvariable=self.detected_algorithm, style="PanelText.TLabel", font=("Segoe UI", 10, "bold")).grid(
            row=2, column=1, sticky="w", padx=10, pady=7
        )

        ttk.Label(parent, text="Tipo de ataque:", style="PanelText.TLabel").grid(row=3, column=0, sticky="w", pady=7)
        attack_combo = ttk.Combobox(parent, textvariable=self.attack_selected, values=ATTACK_OPTIONS, state="readonly")
        attack_combo.grid(row=3, column=1, sticky="ew", padx=10, pady=7)

        ttk.Label(parent, text="Diccionario externo:", style="PanelText.TLabel").grid(row=4, column=0, sticky="w", pady=7)
        ttk.Entry(parent, textvariable=self.dictionary_path).grid(row=4, column=1, sticky="ew", padx=10, pady=7)
        ttk.Button(parent, text="Buscar diccionario", style="Secondary.TButton", command=self.select_dictionary).grid(
            row=4, column=2, pady=7
        )

        ttk.Label(parent, text="Longitud contraseña:", style="PanelText.TLabel").grid(row=5, column=0, sticky="w", pady=7)
        length_frame = ttk.Frame(parent, style="Panel.TFrame")
        length_frame.grid(row=5, column=1, sticky="w", padx=10, pady=7)
        ttk.Label(length_frame, text="entre", style="PanelText.TLabel").pack(side="left")
        ttk.Entry(length_frame, textvariable=self.min_password_len, width=6).pack(side="left", padx=6)
        ttk.Label(length_frame, text="y", style="PanelText.TLabel").pack(side="left")
        ttk.Entry(length_frame, textvariable=self.max_password_len, width=6).pack(side="left", padx=6)
        ttk.Label(length_frame, text="caracteres", style="PanelText.TLabel").pack(side="left")

        ttk.Label(parent, text="Ayuda tipo contraseña:", style="PanelText.TLabel").grid(row=6, column=0, sticky="w", pady=7)
        type_combo = ttk.Combobox(parent, textvariable=self.password_type_filter, values=PASSWORD_TYPE_OPTIONS, state="readonly")
        type_combo.grid(row=6, column=1, sticky="ew", padx=10, pady=7)

        ttk.Label(parent, text="Tiempo máximo:", style="PanelText.TLabel").grid(row=7, column=0, sticky="w", pady=7)
        time_frame = ttk.Frame(parent, style="Panel.TFrame")
        time_frame.grid(row=7, column=1, sticky="w", padx=10, pady=7)
        ttk.Entry(time_frame, textvariable=self.max_hours, width=8).pack(side="left", padx=(0, 6))
        ttk.Label(time_frame, text="horas", style="PanelText.TLabel").pack(side="left")

        ttk.Label(parent, text="Límite de iteraciones:", style="PanelText.TLabel").grid(row=8, column=0, sticky="w", pady=7)
        iter_frame = ttk.Frame(parent, style="Panel.TFrame")
        iter_frame.grid(row=8, column=1, sticky="w", padx=10, pady=7)
        ttk.Entry(iter_frame, textvariable=self.max_iterations, width=16).pack(side="left", padx=(0, 6))
        ttk.Label(iter_frame, text="pruebas", style="PanelText.TLabel").pack(side="left")

        buttons = ttk.Frame(parent, style="Panel.TFrame")
        buttons.grid(row=9, column=1, sticky="e", padx=10, pady=12)
        self.start_button = ttk.Button(buttons, text="Iniciar ataque", style="Primary.TButton", command=self.start_attack)
        self.start_button.pack(side="left", padx=(0, 8))
        self.stop_button = ttk.Button(buttons, text="Detener", style="Danger.TButton", command=self.stop_attack)
        self.stop_button.pack(side="left")

        ttk.Label(parent, text="Estadísticas del ataque", style="PanelTitle.TLabel").grid(
            row=10, column=0, columnspan=3, sticky="w", pady=(8, 8)
        )

        stats_frame = ttk.Frame(parent, style="Panel.TFrame")
        stats_frame.grid(row=11, column=0, columnspan=3, sticky="ew")
        stats_frame.columnconfigure((0, 1, 2, 3), weight=1)
        self._stat_card(stats_frame, "Pruebas totales", self.total_tests, 0, 0)
        self._stat_card(stats_frame, "Pruebas/s actuales", self.current_rate, 0, 1)
        self._stat_card(stats_frame, "Pruebas/s medias", self.average_rate, 0, 2)
        self._stat_card(stats_frame, "Clave / desplazamiento", self.found_value, 0, 3)
        self._stat_card(stats_frame, "Mínimo pruebas/s", self.min_rate, 1, 0)
        self._stat_card(stats_frame, "Máximo pruebas/s", self.max_rate, 1, 1)
        self._stat_card(stats_frame, "Longitud contraseña", self.password_length, 1, 2)
        self._stat_card(stats_frame, "Tipo contraseña", self.password_type, 1, 3)

        ttk.Label(parent, text="Prueba actual:", style="PanelText.TLabel").grid(row=12, column=0, sticky="w", pady=(12, 4))
        ttk.Label(parent, textvariable=self.current_test, style="PanelText.TLabel", font=("Segoe UI", 10, "bold")).grid(
            row=12, column=1, columnspan=2, sticky="w", padx=10, pady=(12, 4)
        )

        ttk.Label(
            parent,
            text=f"Las imágenes recuperadas se guardan automáticamente en:\n{ATTACKED_IMAGES_DIR}\n\nPuedes ajustar longitud, tipo de contraseña, tiempo máximo y límite de iteraciones para controlar el ataque.",
            style="PanelText.TLabel",
            wraplength=820,
        ).grid(row=13, column=0, columnspan=3, sticky="w", pady=(10, 0))

    def _stat_card(self, parent: ttk.Frame, title: str, variable: tk.StringVar, row: int, column: int) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=12)
        card.grid(row=row, column=column, sticky="ew", padx=6, pady=6)
        ttk.Label(card, text=title, style="StatLabel.TLabel").pack(anchor="w")
        ttk.Label(card, textvariable=variable, style="StatValue.TLabel").pack(anchor="w", pady=(4, 0))

    def select_encrypted(self) -> None:
        path = filedialog.askopenfilename(
            title="Selecciona un archivo cifrado",
            initialdir=BASE_DIR,
            filetypes=ENCRYPTED_TYPES,
        )
        if path:
            self.encrypted_path.set(path)
            try:
                algorithm = get_algorithm(path)
                self.detected_algorithm.set(algorithm or "Desconocido")
                self.status.set(f"Archivo seleccionado: {path}")
                if algorithm == "CESAR":
                    self.attack_selected.set("César - fuerza bruta 256 desplazamientos")
                elif algorithm == "VIGNERE":
                    self.attack_selected.set("Ataque por cabecera PNG (César/Vigenère)")
                elif algorithm in {"RC4", "DES", "AES"}:
                    self.attack_selected.set("Ataque inteligente")
            except AttackError as exc:
                self.detected_algorithm.set("No válido")
                self.status.set(f"Error: {exc}")
                messagebox.showerror("Error", str(exc))


    def select_dictionary(self) -> None:
        path = filedialog.askopenfilename(
            title="Selecciona un diccionario de contraseñas",
            initialdir=PROJECT_DIR,
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
        )
        if path:
            self.dictionary_path.set(path)
            self.status.set(f"Diccionario seleccionado: {path}")


    def _get_password_length_range(self) -> tuple[int, int]:
        try:
            min_len = int(self.min_password_len.get().strip())
            max_len = int(self.max_password_len.get().strip())
        except ValueError:
            raise AttackError("La longitud de contraseña debe ser numérica.")
        if min_len < 1 or max_len < 1:
            raise AttackError("La longitud mínima y máxima deben ser mayores que cero.")
        if min_len > max_len:
            raise AttackError("La longitud mínima no puede ser mayor que la máxima.")
        if max_len > 64:
            raise AttackError("Para mantener el ataque controlado, la longitud máxima no puede superar 64 caracteres.")
        return min_len, max_len

    def _get_attack_limits(self) -> tuple[float, int]:
        try:
            max_hours = float(self.max_hours.get().strip().replace(",", "."))
        except ValueError:
            raise AttackError("El tiempo máximo debe ser numérico. Ejemplo: 4")
        try:
            max_iterations = int(self.max_iterations.get().strip())
        except ValueError:
            raise AttackError("El límite de iteraciones debe ser un número entero. Ejemplo: 1000000")
        if max_hours <= 0:
            raise AttackError("El tiempo máximo debe ser mayor que cero.")
        if max_iterations <= 0:
            raise AttackError("El límite de iteraciones debe ser mayor que cero.")
        return max_hours, max_iterations

    def _limit_reached(self) -> bool:
        if self._stop_requested:
            return True
        if self._attack_started_at is None or self._max_seconds is None:
            return False
        return (time.perf_counter() - self._attack_started_at) >= self._max_seconds

    def start_attack(self) -> None:
        if self._attack_thread and self._attack_thread.is_alive():
            messagebox.showwarning("Ataque en ejecución", "Ya hay un ataque en marcha.")
            return

        encrypted = self.encrypted_path.get().strip()
        if not encrypted:
            messagebox.showwarning("Falta archivo", "Selecciona primero un archivo cifrado.")
            return

        try:
            min_len, max_len = self._get_password_length_range()
            max_hours, max_iterations = self._get_attack_limits()
        except AttackError as exc:
            messagebox.showwarning("Parámetros no válidos", str(exc))
            return

        self._reset_stats()
        self._stop_requested = False
        self._attack_started_at = time.perf_counter()
        self._max_seconds = max_hours * 3600
        self._last_progress_ui = 0.0
        self._last_progress_total = 0
        if self.start_button is not None:
            self.start_button.configure(state="disabled")
        if self.stop_button is not None:
            self.stop_button.configure(state="normal")
        selected_type = self.password_type_filter.get().strip() or "Cualquiera"
        type_text = "cualquier tipo" if selected_type == "Cualquiera" else selected_type.lower()
        self.status.set(f"Ataque iniciado con contraseñas de {min_len} a {max_len} caracteres, tipo {type_text}, máximo {max_hours:g} h y {max_iterations:,} iteraciones...")

        self._attack_thread = threading.Thread(target=self._run_attack_worker, args=(encrypted, min_len, max_len, selected_type, max_iterations), daemon=True)
        self._attack_thread.start()

    def _run_attack_worker(self, encrypted: str, min_len: int, max_len: int, password_type_filter: str, max_iterations: int) -> None:
        try:
            selected = self.attack_selected.get()
            dictionary = self.dictionary_path.get().strip() or None
            if selected == "César - fuerza bruta 256 desplazamientos":
                result = attack_caesar_bruteforce(
                    encrypted,
                    ATTACKED_IMAGES_DIR,
                    progress_callback=self._progress_from_worker,
                    stop_callback=self._limit_reached,
                    max_iterations=max_iterations,
                )
            elif selected == "Ataque por cabecera PNG (César/Vigenère)":
                result = attack_header(
                    encrypted,
                    ATTACKED_IMAGES_DIR,
                    progress_callback=self._progress_from_worker,
                    stop_callback=self._limit_reached,
                    max_iterations=max_iterations,
                )
            elif selected == "Ataque completo por contraseña":
                result = attack_password_full(
                    encrypted,
                    ATTACKED_IMAGES_DIR,
                    progress_callback=self._progress_from_worker,
                    stop_callback=self._limit_reached,
                    dictionary_path=dictionary,
                    min_password_len=min_len,
                    max_password_len=max_len,
                    password_type_filter=password_type_filter,
                    max_iterations=max_iterations,
                )
            elif selected == "Ataque inteligente":
                result = attack_intelligent(
                    encrypted,
                    ATTACKED_IMAGES_DIR,
                    progress_callback=self._progress_from_worker,
                    stop_callback=self._limit_reached,
                    dictionary_path=dictionary,
                    min_password_len=min_len,
                    max_password_len=max_len,
                    password_type_filter=password_type_filter,
                    max_iterations=max_iterations,
                )
            elif selected == "Claves recurrentes":
                result = attack_recurrent(
                    encrypted,
                    ATTACKED_IMAGES_DIR,
                    progress_callback=self._progress_from_worker,
                    stop_callback=self._limit_reached,
                    min_password_len=min_len,
                    max_password_len=max_len,
                    password_type_filter=password_type_filter,
                    max_iterations=max_iterations,
                )
            elif selected == "Diccionario por librería + mutaciones":
                result = attack_dictionary(
                    encrypted,
                    ATTACKED_IMAGES_DIR,
                    progress_callback=self._progress_from_worker,
                    stop_callback=self._limit_reached,
                    dictionary_path=dictionary,
                    min_password_len=min_len,
                    max_password_len=max_len,
                    password_type_filter=password_type_filter,
                    max_iterations=max_iterations,
                )
            elif selected == "Fuerza bruta limitada":
                result = attack_bruteforce(
                    encrypted,
                    ATTACKED_IMAGES_DIR,
                    progress_callback=self._progress_from_worker,
                    stop_callback=self._limit_reached,
                    min_password_len=min_len,
                    max_password_len=max_len,
                    password_type_filter=password_type_filter,
                    max_iterations=max_iterations,
                )
            else:
                result = attack_png_auto(
                    encrypted,
                    ATTACKED_IMAGES_DIR,
                    progress_callback=self._progress_from_worker,
                    stop_callback=self._limit_reached,
                    dictionary_path=dictionary,
                    min_password_len=min_len,
                    max_password_len=max_len,
                    password_type_filter=password_type_filter,
                    max_iterations=max_iterations,
                )
            self.after(0, self._finish_attack, result)
        except AttackError as exc:
            self.after(0, self._show_error, str(exc))
        except Exception as exc:
            self.after(0, self._show_error, f"Error inesperado: {exc}")

    def _progress_from_worker(self, stats: AttackStats, current: str) -> None:
        # Tkinter no debe recibir decenas de miles de actualizaciones en ataques
        # largos. Se limita el refresco visual, pero el contador interno sigue
        # avanzando y al finalizar se muestra el total exacto.
        now = time.perf_counter()
        enough_time = (now - self._last_progress_ui) >= UI_PROGRESS_INTERVAL_SECONDS
        enough_tests = (stats.total_tests - self._last_progress_total) >= 1000
        if enough_time or enough_tests or stats.total_tests == 0:
            self._last_progress_ui = now
            self._last_progress_total = stats.total_tests
            self.after(0, self._update_stats, stats, current)

    def _update_stats(self, stats: AttackStats, current: str) -> None:
        self.total_tests.set(str(stats.total_tests))
        self.current_rate.set(f"{stats.current_rate:.2f}")
        self.average_rate.set(f"{stats.average_rate:.2f}")
        self.min_rate.set(f"{stats.min_rate:.2f}")
        self.max_rate.set(f"{stats.max_rate:.2f}")
        self.current_test.set(current or "-")
        self.status.set(f"Probando: {current}")

    def _finish_attack(self, result) -> None:
        if self.start_button is not None:
            self.start_button.configure(state="normal")
        if self.stop_button is not None:
            self.stop_button.configure(state="normal")
        self._stop_requested = False
        self._update_stats(result.stats, result.found_value or "finalizado")
        if result.success:
            self.found_value.set(result.found_value or "-")
            self.password_length.set(str(result.password_length) if result.password_length is not None else "-")
            self.password_type.set(result.password_type or "-")
            self.status.set(f"Éxito: {result.output_path}")
            messagebox.showinfo("PNG recuperado", f"{result.message}\n\nGuardado en:\n{result.output_path}")
        else:
            self.found_value.set(result.found_value or "-")
            self.password_length.set(str(result.password_length) if result.password_length is not None else "-")
            self.password_type.set(result.password_type or "-")
            self.status.set(result.message)
            messagebox.showwarning("Ataque finalizado", result.message)

    def _show_error(self, message: str) -> None:
        if self.start_button is not None:
            self.start_button.configure(state="normal")
        if self.stop_button is not None:
            self.stop_button.configure(state="normal")
        self._stop_requested = False
        self.status.set(f"Error: {message}")
        messagebox.showerror("Error", message)

    def _reset_stats(self) -> None:
        self.total_tests.set("0")
        self.current_rate.set("0.00")
        self.average_rate.set("0.00")
        self.min_rate.set("0.00")
        self.max_rate.set("0.00")
        self.found_value.set("-")
        self.password_length.set("-")
        self.password_type.set("-")
        self.current_test.set("-")

    def stop_attack(self) -> None:
        self._stop_requested = True
        self.status.set("Deteniendo ataque...")


if __name__ == "__main__":
    app = AttackApp()
    app.mainloop()

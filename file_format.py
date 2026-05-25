"""Configuración interna de la app de ataques."""

from __future__ import annotations

# Valor interno usado por los ataques que prueban muchas contraseñas.
MAX_WORKERS = 10

# Diccionario mediante librerías.
# Wordfreq se usa SOLO en español para palabras frecuentes.
LIBRARY_LANGUAGES = ("es",)
LIBRARY_WORDS_PER_LANGUAGE = 90000
LIBRARY_MUTATION_WORDS_PER_LANGUAGE = 8000

# Faker genera nombres y apellidos españoles frecuentes/probables.
FAKER_LOCALE = "es_ES"
FAKER_NAME_SAMPLES = 120000
FAKER_SURNAME_SAMPLES = 120000
FAKER_FULLNAME_SAMPLES = 80000

# Años y números típicos que se combinan con nombres/apellidos/palabras.
YEAR_START = 1950
YEAR_END = 2030
SHORT_YEAR_START = 50
SHORT_YEAR_END = 30

# Evita probar candidatos demasiado largos que no son razonables para el proyecto.
MAX_CANDIDATE_LENGTH = 32

# Numero maximo de nombres/apellidos sobre los que se aplican mutaciones con anos.
# Limita el coste para mantener el ataque razonablemente rapido.
NAME_YEAR_MUTATION_LIMIT = 15000

# Ataque inteligente: nombres, apellidos, años cercanos y separadores/símbolos.
INTELLIGENT_NAME_LIMIT = 12000
INTELLIGENT_SURNAME_LIMIT = 12000
INTELLIGENT_PAIR_LIMIT = 35000
INTELLIGENT_YEAR_CENTER = 2026
INTELLIGENT_YEAR_RADIUS = 40
INTELLIGENT_SPECIAL_CHARS = ("_", "-", ".", "!", "@", "#", "*")

# Tamano de lote interno para que las estadisticas arranquen rapido incluso con filtros estrictos.
SEARCH_CHUNK_SIZE = 25

# Limite de memoria para deduplicacion de candidatos.
# Evita que ataques de millones de pruebas acumulen millones de strings en RAM.
UNIQUE_CACHE_LIMIT = 100000

# Frecuencia maxima de refresco de la interfaz durante ataques largos.
UI_PROGRESS_INTERVAL_SECONDS = 0.35

Notas técnicas de la app de ataques
===================================

Estructura:
- app_ataques.py: lanzador exterior.
- programa_ataques/interfaz.py: interfaz roja.
- programa_ataques/attack_algorithms.py: coordinador de ataques.
- programa_ataques/tipos_ataques/: un archivo por tipo de ataque.
- imagenes_atacadas/: carpeta exterior donde se guardan los PNG recuperados.

Ataque inteligente:
- Usa Faker es_ES para generar nombres y apellidos españoles.
- Usa wordfreq solo en español para ampliar palabras probables.
- Prioriza nombres, apellidos, nombre+apellido y nombre+apellido+año.
- Ordena los años por cercanía a la época actual del proyecto: 2026, 2025, 2027, 2024, 2028...
- Prueba símbolos en medio: nombre_apellido, nombre-apellido, nombre!2026, nombre_apellido_2026, etc.

Campos de resultado:
- Longitud contraseña: número de caracteres de la contraseña encontrada.
- Tipo contraseña: Numérica, Alfabética (español), Alfanumérica o Alfanumérica con símbolos.

Los hilos se usan internamente y no se muestran en la interfaz.


Filtro de tipo de contraseña: la interfaz permite limitar las candidatas a Numérica, Alfabética (español), Alfanumérica o Alfanumérica con símbolos. Este filtro se aplica internamente antes de probar HMAC/descifrado.

LÍMITES CONFIGURABLES
- Tiempo máximo: la interfaz lo muestra en horas. Por defecto son 4 horas.
- Límite de iteraciones: número máximo de candidatas válidas que se probarán tras aplicar filtros de longitud y tipo. Por defecto es 1.000.000.
- Estos límites se aplican principalmente a los ataques por contraseña. En César y Vigenère por cabecera el número de pruebas es naturalmente muy bajo, pero el límite de tiempo también se respeta.

Correccion de estabilidad para ataques largos
===========================================

Problema detectado:
- En ataques de muchas horas y millones de pruebas, la deduplicacion de candidatos podia acumular millones de cadenas en memoria.
- Eso podia hacer que Windows congelase o cerrase la aplicacion aunque el ataque estuviera funcionando.
- La interfaz tambien podia recibir demasiadas actualizaciones durante ejecuciones largas.

Cambios aplicados:
1. Deduplicacion con memoria limitada:
   - La funcion unique() ahora mantiene una ventana de candidatos vistos.
   - Cuando supera UNIQUE_CACHE_LIMIT, limpia la cache.
   - Esto evita crecimiento ilimitado de RAM durante ataques de 3M+ pruebas.

2. Refresco de interfaz limitado:
   - La app actualiza las estadisticas con una frecuencia controlada.
   - El contador interno sigue avanzando, pero Tkinter no se satura.

3. Boton Iniciar protegido:
   - Al empezar un ataque, el boton Iniciar se desactiva.
   - Se vuelve a activar al finalizar, detener o producirse un error.

4. Configuracion nueva en programa_ataques/config.py:
   - UNIQUE_CACHE_LIMIT = 100000
   - UI_PROGRESS_INTERVAL_SECONDS = 0.35

Resultado esperado:
- La app puede permanecer abierta durante ataques largos sin acumular memoria de forma indefinida.
- Si se fija un limite de 4 horas o 3.000.000 iteraciones, debe detenerse por el limite correspondiente en vez de bloquearse.

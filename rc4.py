INFORME DE COMPROBACION - APP DE ATAQUES

Problema detectado:
- Con filtros estrictos de longitud/tipo de contraseña, el generador inteligente podia tardar en producir el primer lote de candidatos.
- Por eso la interfaz podia mostrar "Ya hay un ataque en marcha" y las estadisticas quedaban en 0 durante un rato: el ataque no estaba roto, pero estaba preparando candidatos antes de empezar a contarlos.

Cambios aplicados:
- El ataque inteligente ahora emite candidatos inmediatos antes de cargar listas grandes de Faker/wordfreq.
- Se redujo el tamaño interno de lote para que las estadisticas arranquen antes.
- Se añadieron candidatos compuestos de contexto: palabras humanas unidas, con guiones, guion bajo, punto, ! y @.
- Se reforzaron patrones como palabra+anio, anio+palabra y palabra+simbolo+anio.
- Se mantiene el uso de wordfreq y Faker, no se sustituye por un diccionario pequeño cerrado.

Pruebas realizadas:
- CESAR con desplazamiento 73: OK.
- VIGENERE con clave limon por cabecera PNG: OK.
- RC4 con claves numerica, alfabetica, alfanumerica y con simbolos: OK.
- DES con claves numerica, alfabetica, alfanumerica y con simbolos: OK.
- AES con claves numerica, alfabetica, alfanumerica y con simbolos: OK.
- Ataque inteligente: OK.
- Ataque completo por contraseña: OK.
- Diccionario por libreria + mutaciones: comprobado en RC4 con todos los tipos: OK.
- Fuerza bruta limitada numerica: comprobada en RC4, DES y AES: OK.

Contraseñas de prueba:
- Numerica: 123456789
- Alfabetica: mianotuya
- Alfanumerica: marco2026
- Alfanumerica con simbolos: marco_2026

Resultado final: FULL_MATRIX_OK

INFORME DE CORRECCION HONESTA

1. El estimador no descifra archivos ni sabe la contraseña real de un .encfile.
   Solo responde a la pregunta: si la contraseña escrita se probara con el generador actual,
   ¿en que posicion exacta apareceria?

2. La app de ataques si descifra el archivo real. Si la contraseña del archivo no coincide
   exactamente con la contraseña analizada en el estimador, los resultados no pueden coincidir.

3. Se ha comprobado con un archivo RC4 de prueba cifrado con la contraseña exacta
   Nicolas2006, rango 8-12 y tipo Alfanumerica:
   - el generador inteligente contiene Nicolas2006 antes de 1.000.000 de candidatos validos;
   - la app de ataques recupera el PNG con esa contraseña;
   - el estimador busca coincidencia exacta, sin convertir Nicolas2006 en nicolas2006.

4. La cifra de intentos puede variar ligeramente entre estimador y app porque la app prueba
   en paralelo por lotes y se detiene en cuanto encuentra una coincidencia. Lo importante es
   que ambos usan el mismo orden logico de candidatos y que la contraseña aparece dentro
   del mismo limite.

5. Si en tu prueba real la app no encuentra la clave, las causas mas probables son:
   - el archivo no fue cifrado con la contraseña que estas analizando en el estimador;
   - el algoritmo o la version de cifrado no coincide con esta app;
   - el filtro de tipo/longitud excluye la contraseña real;
   - la contraseña real no aparece dentro del limite de iteraciones configurado.

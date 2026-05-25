INFORME GENERADOR COMPARTIDO

Corrección aplicada:
- La app de ataques y el estimador usan ahora el mismo generador lógico de candidatos.
- El ataque inteligente genera variantes humanas reales sin considerar equivalentes dos claves distintas.
- Ejemplo: nicolas2006 y Nicolas2006 son candidatas distintas.
- Si la clave real es Nicolas2006, la app debe probar exactamente Nicolas2006.

Mejoras del ataque inteligente:
- Variantes de mayúsculas/minúsculas: nicolas, Nicolas, NICOLAS.
- Combinaciones con años: nicolas2006, Nicolas2006, 2006Nicolas.
- Separadores/símbolos: Nicolas_2006, Nicolas-2006, Nicolas.2006, Nicolas@2006.
- Orden de años determinista para que estimador y ataque recorran igual.

Importante:
- No se ha añadido bichobola como palabra sembrada.
- El estimador no considera coincidencias por normalización: solo coincidencia exacta.

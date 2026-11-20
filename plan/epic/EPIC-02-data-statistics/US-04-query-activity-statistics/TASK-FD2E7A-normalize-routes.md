# Tarea técnica — Adaptar en lectura y consultar Routes por periodo

## Trazabilidad en Milano

- Código: `FD2E7A`.
- Story Points: 5.

## Resumen

Implementar el repositorio autorizado de rutas y su traducción a registros canónicos de actividad.

## Justificación

Los 3.087 documentos observados tienen dos variantes superiores, pero mezclan enteros y decimales, contienen coordenadas opacas, un `id` opcional no canónico, referencias históricas no resolubles y distancias atípicas que no deben distorsionar cálculos.

## Alcance

Incluido:
1. Definir el modelo canónico mínimo de paseo con `datetime` UTC consciente de zona, duración en segundos y distancia en metros.
2. Definir el contrato bruto de lectura para las dos variantes observadas de `Routes` y aceptar las formas con y sin `id` sin tratar ese campo como identificador canónico.
3. Diseñar consultas filtradas por `userId` y periodo compatibles con índices verificados, sin escaneo global ni comprobación previa contra todos los usuarios.
4. Confirmar con los productores móviles que `time` representa segundos Unix y convertir enteros y decimales al `datetime` UTC canónico mediante una regla documentada, exclusivamente en memoria.
5. Normalizar duración en segundos y distancia en metros sin leer ni deserializar `coordinates`.
6. Definir límites plausibles y política para distancia cero, distancia extrema, duración inválida, duplicados y documentos malformados.
7. Aplicar paginación y límites para historiales grandes.
8. Emitir categorías sanitizadas de exclusión o advertencia sin identificadores ni coordenadas.

Excluido:
- Deserialización de coordenadas y actividad en curso.
- Reparación de documentos históricos.
- Corrección de `id`, referencias de usuario, unidades o valores atípicos en Firestore.

## Criterios de aceptación

- Solo se consultan rutas del `uid` autenticado y dentro del periodo autorizado.
- Los fixtures de enteros y decimales en segundos se normalizan según el contrato verificado; cualquier unidad distinta se rechaza como incompatible.
- Los registros inválidos no se convierten silenciosamente en cero.
- El adaptador no materializa `coordinates` y admite las dos variantes superiores observadas.
- La conversión temporal nunca escribe el valor canónico de vuelta en Firestore.
- La consulta usa índices y paginación definidos, sin escaneo global.

## Riesgo de no realizarla

Las cifras podrían ser incorrectas y las consultas degradarse o cruzar ámbitos de usuario.

## Pruebas

- Unitarias:
  - Enteros y decimales temporales, unidades, valores extremos, variantes con/sin `id`, duplicados y límites de periodo.
- Integración:
  - Consultas indexadas y aisladas con emulador.
- La funcionalidad existente no debe verse afectada (regresión).

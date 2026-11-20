# Tarea técnica — Adaptar en lectura el perfil desde Users

## Trazabilidad en Milano

- Código: `FD2E72`.
- Story Points: 5.

## Resumen

Implementar el repositorio autorizado de `Users` y la traducción de solo lectura desde todas las variantes heredadas observadas a un modelo canónico mínimo de perfil.

## Justificación

Los 898 documentos observados presentan 87 variantes y entre 1 y 29 campos. El documento mezcla dueño, perro, dispositivo, localización, relaciones, suscripción y estado de paseo; combina ausencia, nulos y vacíos; y usa fechas textuales y catálogos numéricos. La adaptación debe ser explícita y no puede convertirse en una tarea de saneamiento de Firestore.

## Alcance

Incluido:
1. Definir el modelo canónico mínimo de perfil requerido por el catálogo.
2. Leer exclusivamente `Users/{uid}` usando el `uid` autenticado.
3. Definir el contrato bruto de lectura que cubra todas las variaciones observadas de `Users` relevantes para perfil y distinga campo ausente, `null`, cadena vacía y valor inválido.
4. Parsear `dogDate` en sus variantes observadas de 4, 9 y 10 dígitos mediante reglas confirmadas, sin completar valores ambiguos.
5. Traducir raza, sexo, sociabilidad y energía con catálogos verificados en iOS y Android.
6. Resolver variantes de foto solo si una capacidad las necesita.
7. Validar la coherencia entre identificador de documento y `userId` sin rechazar silenciosamente las excepciones históricas.
8. Excluir email, token de dispositivo, premium, amigos, ubicación, claves dinámicas y paseo en curso del modelo conversacional.
9. Registrar categorías sanitizadas de compatibilidad y calidad, nunca valores personales.

Excluido:
- Mutaciones del documento `Users`.
- Backfill, limpieza de vacíos o nulos, corrección de identificadores y separación física de propietario y perro.
- Inferencia de valores desconocidos por el modelo.

## Criterios de aceptación

- El repositorio no acepta un `uid` libre procedente del payload o del modelo.
- Fixtures representativos de iOS y Android producen el mismo modelo canónico cuando son equivalentes.
- Todas las variantes de `Users` relevantes para perfil están cubiertas por fixtures derivados y anonimizados; las variantes fuera de alcance se ignoran de forma explícita.
- Valores desconocidos permanecen ausentes o explícitamente no soportados.
- Los campos fuera de alcance no se envían al modelo.

## Riesgo de no realizarla

El chatbot podría responder con catálogos incorrectos, filtrar datos innecesarios o confiar en estado client-writable.

## Pruebas

- Unitarias:
  - Fechas de 4, 9 y 10 dígitos, catálogos, ausencia/null/vacío, variantes de imagen, identificador incoherente y campos inválidos.
- Integración:
  - Lectura aislada de `Users/{uid}` con emulador.
- La funcionalidad existente no debe verse afectada (regresión).

# Tarea técnica — Implementar consultas autorizadas de salud

## Trazabilidad en Milano

- Código: `FD2E8A`.
- Story Points: 3.

## Resumen

Crear el repositorio y los casos de uso para listar registros, filtrar por tipo y consultar próximas fechas dentro del usuario autenticado.

## Justificación

La conversación necesita recuperar datos estructurados sin exponer rutas de Firestore ni permitir identificadores ajenos.

## Alcance

Incluido:
1. Definir modelos de dominio y filtros permitidos.
2. Implementar repositorio sobre la subcolección derivada del principal autenticado.
3. Añadir orden, límites, paginación y semántica de próxima fecha.
4. Implementar tools de consulta sin argumentos de identidad.
5. Ocultar existencia de registros ajenos en accesos por identificador.
6. Integrar healthRecords en el flujo verificado de borrado de cuenta.
7. Deserializar únicamente versiones de esquema soportadas y devolver un error controlado ante una versión futura desconocida.

Excluido:
- Escritura y confirmación de registros de salud.
- Notificaciones de próximas fechas.
- Lectura o corrección de datos de salud desde campos heredados de otras colecciones.

## Criterios de aceptación

- Todas las consultas derivan la ruta del `uid` autenticado.
- La paginación es estable y no mezcla cuentas.
- Próximas fechas se calculan por código con contrato temporal explícito.
- Las fechas civiles no sufren conversiones implícitas de zona horaria y los timestamps se exponen en UTC.
- El borrado de cuenta elimina o agenda la eliminación según la política aprobada.

## Riesgo de no realizarla

Las tools podrían exponer documentos ajenos o devolver resultados inconsistentes y no paginables.

## Pruebas

- Unitarias:
  - Filtros, orden, fechas y paginación.
- Integración:
  - Repositorio, rules emulator y borrado de cuenta.
- La funcionalidad existente no debe verse afectada (regresión).

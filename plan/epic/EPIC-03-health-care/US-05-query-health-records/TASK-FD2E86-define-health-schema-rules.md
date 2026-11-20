# Tarea técnica — Definir el esquema, índices y reglas de healthRecords

## Trazabilidad en Milano

- Código: `FD2E86`.
- Story Points: 5.

## Resumen

Formalizar y desplegar el contrato nuevo y versionado de `Users/{uid}/healthRecords` con tipos correctos, validación cerrada, índices y reglas estrictas, sin heredar las convenciones defectuosas de las colecciones actuales.

## Justificación

La colección es nueva, contiene información sensible sobre cuidados y debe soportar consultas y evolución sin permitir escrituras directas no autorizadas. A diferencia de la base heredada, el equipo sí es responsable de diseñar correctamente esta estructura desde su primera versión.

## Alcance

Incluido:
1. Definir por separado los contratos cerrados de vacuna, desparasitación, medicación y cita, con campos comunes y reglas específicas.
2. Distinguir fechas civiles sin hora de instantes técnicos; prohibir fechas funcionales como cadenas numéricas y utilizar timestamps gestionados por servidor para auditoría.
3. Añadir identificador estable, `schemaVersion`, propietario, origen, creación, actualización e idempotencia con nombres fijos.
4. Definir opcionalidad, límites de longitud, enums, precisión, zona horaria y combinaciones válidas sin claves dinámicas ni flags enteros.
5. Definir una estrategia extensible para futura asociación a perro sin afirmar soporte multi-perro actual ni duplicar el perfil heredado.
6. Diseñar índices para listados por tipo, fecha, próxima fecha y paginación estable.
7. Escribir reglas: lectura del propio usuario según contrato y escrituras únicamente por la identidad del servicio.
8. Versionar configuración Firestore y probar reglas en emulador con propiedades desconocidas, tipos erróneos y acceso cruzado.
9. Definir compatibilidad hacia delante y estrategia de evolución para futuras versiones de `healthRecords`, no para las colecciones heredadas.

Excluido:
- Recordatorios y datos clínicos no acordados.
- Migración multi-perro.
- Migración, limpieza o reutilización de esquemas de `Users`, `Routes` u otras colecciones existentes.

## Criterios de aceptación

- El esquema rechaza combinaciones inválidas y propiedades desconocidas.
- Ninguna fecha funcional se almacena como cadena numérica y ningún timestamp de auditoría depende del reloj del cliente.
- Los contratos utilizan nombres de campo estables y no aceptan identificadores como claves dinámicas.
- Las reglas impiden accesos cruzados y escrituras directas del cliente.
- Las consultas previstas disponen de índices versionados.
- La evolución futura está definida sin introducir campos especulativos no validados.

## Riesgo de no realizarla

Los datos quedarían inconsistentes, inseguros o imposibles de consultar y evolucionar de forma controlada.

## Pruebas

- Unitarias:
  - Validación de cada tipo, fecha civil, timestamp, enum, límite, propiedad desconocida y combinación inválida.
- Integración:
  - Reglas e índices con emulador y usuarios cruzados.
- La funcionalidad existente no debe verse afectada (regresión).

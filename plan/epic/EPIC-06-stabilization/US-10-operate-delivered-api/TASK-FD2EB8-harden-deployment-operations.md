# Tarea técnica — Endurecer despliegue y operación

## Trazabilidad en Milano

- Código: `FD2EB8`.
- Story Points: 5.

## Resumen

Completar la configuración productiva, observabilidad, alertas, rollback y procedimientos de recuperación del servicio.

## Justificación

Un despliegue funcional en desarrollo no es suficiente para operar una API con datos sensibles y dependencias externas.

## Alcance

Incluido:
1. Definir entornos, promoción de versiones y separación de configuración.
2. Aplicar mínimo privilegio a identidad de servicio, Firestore y Secret Manager.
3. Configurar liveness, readiness, timeouts, escalado y límites del runtime.
4. Definir SLI y alertas para latencia, errores, proveedor, Firestore, cuotas y seguridad.
5. Crear procedimientos de despliegue, smoke test, rollback y rotación de secretos.
6. Verificar restauración o recuperación de configuración y compatibilidad de esquema.
7. Identificar versión desplegada sin exponer información sensible.

Excluido:
- Operación de tiendas y aplicaciones móviles.
- Remediación de servicios heredados no consumidos.

## Criterios de aceptación

- El despliegue y rollback se ejecutan mediante procedimientos reproducibles.
- Los permisos efectivos corresponden al mínimo requerido.
- Readiness distingue indisponibilidad de dependencias relevante.
- Alertas y runbooks tienen responsable y prueba controlada.

## Riesgo de no realizarla

Un incidente podría prolongarse por falta de visibilidad, permisos excesivos o rollback no probado.

## Pruebas

- Unitarias:
  - Validación de settings y políticas configurables.
- Integración:
  - Despliegue, smoke, alertas sintéticas y rollback en entorno autorizado.
- La funcionalidad existente no debe verse afectada (regresión).

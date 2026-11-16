# Tarea técnica — Desplegar el servicio en el entorno de desarrollo

## Resumen

Seleccionar el runtime cloud y crear un despliegue reproducible con identidad de servicio, secretos, salud y acceso controlado.

## Justificación

La integración móvil y las pruebas de Firebase requieren un endpoint estable fuera del entorno local, sin compartir secretos con los clientes.

## Alcance

Incluido:
- 1. Comparar runtimes soportados según región, streaming, timeout, escalado, cold start y observabilidad.
- 2. Registrar la decisión técnica del runtime y modelo de despliegue.
- 3. Configurar build, identidad de servicio de mínimo privilegio y acceso a Secret Manager.
- 4. Separar configuración de desarrollo y producción sin copiar secretos.
- 5. Desplegar liveness/readiness y un endpoint autenticado mínimo.
- 6. Documentar despliegue, rollback inicial y verificación post-despliegue.

Excluido:
- Despliegue productivo final.
- Configuración de publicación móvil.

## Criterios de aceptación

- El servicio se despliega desde configuración reproducible en el entorno de desarrollo.
- La identidad solo dispone de permisos necesarios y los secretos no aparecen en artefactos o logs.
- Readiness representa dependencias acordadas y el smoke test autenticado funciona.
- Existe un rollback básico verificable.

## Riesgo de no realizarla

La integración dependería de ejecuciones locales y configuraciones manuales no auditables.

## Pruebas

- Unitarias:
  - Validación de configuración de runtime.
- Integración:
  - Smoke test, secretos y permisos en desarrollo.
- La funcionalidad existente no debe verse afectada (regresión).

## Dependencias

- TASK-03, TASK-04 y acceso Google Cloud — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Qué región UE es compatible con el proyecto Firebase actual?
  - Respuesta (Supuesto): Se decidirá tras inspeccionar la región y las restricciones del proyecto.
  - Fuente de verdad: Auditoría TASK-02.
  - Alineación: E0 y E6.

## Enlaces

- Épica/ticket relacionado: [US-02](US-02-secure-api-access.md)

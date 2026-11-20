# Épica — E6 · Estabilización y entrega de la API

## Objetivo de negocio

**COMO** equipo responsable de operar Dappy Dogs
**NECESITO** una API estable, verificable y documentada
**PARA** integrar y mantener el chatbot con un riesgo operativo controlado

## Contexto y justificación

La entrega requiere verificar el flujo principal de extremo a extremo, cerrar errores críticos y proporcionar documentación técnica mínima de arquitectura, despliegue, configuración y operación.

## Valor esperado / métricas de éxito

- El catálogo acordado supera las pruebas automatizadas y la verificación de extremo a extremo.
- No quedan defectos críticos abiertos en autenticación, aislamiento, confirmación o seguridad veterinaria.
- El despliegue es reproducible y dispone de runbook, configuración y observabilidad verificadas.

## Alcance

Incluido:
- Banco automatizado y pruebas integradas del catálogo.
- Verificación de seguridad, resiliencia y regresión.
- Ajuste controlado de instrucciones del modelo basado en evidencia.
- Documentación técnica y traspaso operativo de la API.

Excluido:
- Revisión de Apple o Google y publicación en tiendas.
- Corrección de hallazgos heredados fuera del alcance del chatbot.
- Limpieza, normalización en origen, migración o reestructuración de la base de datos existente.

## Riesgos y dependencias

- Dependencia de versiones móviles integradas y entorno estable — (Impacto: alto)
- Falta de datos de prueba representativos — (Impacto: alto)
- Regresiones provocadas por variaciones históricas no incluidas en fixtures — (Impacto: alto)
- Cambios tardíos de proveedor, catálogo o contratos — (Impacto: alto)

## Hitos (opcional)

- Flujo completo disponible para integración móvil — 11/12/2026
- Entrega técnica — 18/12/2026

## Correspondencia de entrega

- Código de Milano: `FD2E0D`.
- Estado de Milano verificado el 18 de noviembre de 2026: `backlog`.
- Asignación de Milano: Sprint 4 y el hito de entrega del 18 de diciembre de 2026.
- El acta de entrega de Milano se sustenta en la matriz catálogo-prueba, la evidencia de seguridad y resiliencia, la versión desplegada identificable y el traspaso técnico; no sustituye esas evidencias.

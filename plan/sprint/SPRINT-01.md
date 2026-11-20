# SPRINT-01 · Fundaciones y primera consulta

## Resumen operativo

- Objetivo: construir las fundaciones y el núcleo conversacional, iniciar la consulta de datos y demostrar una consulta real de perfil en desarrollo.
- Fechas: 10–27 de noviembre de 2026.
- Estado en Milano: `active`.
- Capacidad: 80 puntos.
- Puntos comprometidos en Milano: 0.
- Puntos completados en Milano: 0.
- SP de TASK asignadas: 38.
- Hitos relacionados: `Demo del núcleo conversacional` el 27 de noviembre y contribución inicial a `Demo de consultas y estadísticas` el 4 de diciembre.

## Elementos asignados

| Tipo | Elemento | Padre | Estado | SP | Responsable |
|---|---|---|---:|---:|---|
| EPIC | [EPIC-01 · Fundaciones y núcleo conversacional](../epic/EPIC-01-conversational-core/EPIC-01.md) | — | `todo` | — | Íñigo |
| HU | [US-01 · Acceder de forma segura a la API conversacional](../epic/EPIC-01-conversational-core/US-01-secure-api-access/US-01.md) | EPIC-01 | `todo` | — | Íñigo |
| TASK | [TASK-FD2E56 · Crear las fundaciones del servicio Python](../epic/EPIC-01-conversational-core/US-01-secure-api-access/TASK-FD2E56-bootstrap-python-service.md) | US-01 | `todo` | 3 | Íñigo |
| TASK | [TASK-FD2E5A · Implementar Firebase Auth y App Check](../epic/EPIC-01-conversational-core/US-01-secure-api-access/TASK-FD2E5A-implement-auth-app-check.md) | US-01 | `todo` | 5 | Íñigo |
| TASK | [TASK-FD2E5E · Establecer límites HTTP, errores y observabilidad](../epic/EPIC-01-conversational-core/US-01-secure-api-access/TASK-FD2E5E-establish-http-boundaries.md) | US-01 | `todo` | 3 | Íñigo |
| TASK | [TASK-FD2E62 · Desplegar el servicio en desarrollo](../epic/EPIC-01-conversational-core/US-01-secure-api-access/TASK-FD2E62-deploy-development-service.md) | US-01 | `todo` | 3 | Íñigo |
| HU | [US-02 · Mantener una conversación controlada con el modelo](../epic/EPIC-01-conversational-core/US-02-controlled-conversation/US-02.md) | EPIC-01 | `todo` | — | Íñigo |
| TASK | [TASK-FD2E66 · Evaluar y seleccionar el proveedor de IA](../epic/EPIC-01-conversational-core/US-02-controlled-conversation/TASK-FD2E66-evaluate-model-provider.md) | US-02 | `todo` | 3 | Íñigo |
| TASK | [TASK-FD2E6A · Construir el orquestador conversacional](../epic/EPIC-01-conversational-core/US-02-controlled-conversation/TASK-FD2E6A-build-conversation-orchestrator.md) | US-02 | `todo` | 8 | Íñigo |
| TASK | [TASK-FD2E6E · Aplicar seguridad veterinaria y límites](../epic/EPIC-01-conversational-core/US-02-controlled-conversation/TASK-FD2E6E-enforce-safety-quotas.md) | US-02 | `todo` | 5 | Íñigo |
| EPIC | [EPIC-02 · Consulta de datos y estadísticas](../epic/EPIC-02-data-statistics/EPIC-02.md) | — | `todo` | — | Íñigo |
| HU | [US-03 · Consultar el perfil normalizado del perro](../epic/EPIC-02-data-statistics/US-03-query-dog-profile/US-03.md) | EPIC-02 | `todo` | — | Íñigo |
| TASK | [TASK-FD2E72 · Adaptar en lectura el perfil desde Users](../epic/EPIC-02-data-statistics/US-03-query-dog-profile/TASK-FD2E72-normalize-users-profile.md) | US-03 | `todo` | 5 | Íñigo |
| TASK | [TASK-FD2E76 · Exponer la capacidad conversacional de perfil](../epic/EPIC-02-data-statistics/US-03-query-dog-profile/TASK-FD2E76-expose-profile-capability.md) | US-03 | `todo` | 3 | Íñigo |

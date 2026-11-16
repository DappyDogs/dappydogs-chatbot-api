# Historia de usuario — Acceder de forma segura a la API conversacional

## Objetivo

**COMO** usuario autenticado de Dappy Dogs
**NECESITO** que la API valide mi identidad y la legitimidad de la aplicación
**PARA** acceder al chatbot sin exponer datos de otras cuentas ni credenciales del servicio

## Contexto

Las aplicaciones se autentican con Firebase y actualmente no existe un backend general. La nueva API debe verificar Firebase Auth y App Check y establecer un contrato HTTP seguro y observable.

## Alcance

Incluido:
- Fundación Python y aplicación HTTP.
- Firebase Auth y App Check.
- Errores estables, correlación, límites y observabilidad base.
- Despliegue reproducible en desarrollo.

Excluido:
- Pantallas móviles y activación del SDK App Check en las apps.
- Validación de compras premium.

## Criterios de aceptación

- **AC.01.** Caso: identidad válida
  Dada una petición con tokens válidos de Firebase Auth y App Check;
  Cuando alcanza un endpoint protegido;
  Entonces la API deriva el `uid` verificado y procesa la petición dentro de ese ámbito.
- **AC.02.** Caso: credenciales inválidas
  Dada una petición sin token, expirada o con App Check inválido;
  Cuando alcanza un endpoint protegido;
  Entonces se rechaza con un error estable sin ejecutar capacidades ni revelar detalles internos.
- **AC.03.** Caso: identidad forjada
  Dado un `uid` incluido en el cuerpo distinto del autenticado;
  Cuando se procesa la petición;
  Entonces el valor del cliente no amplía el ámbito ni sustituye la identidad verificada.

## Casos límite / fallos

- Rotación de claves, indisponibilidad de Firebase, token revocado y peticiones repetidas.
- App Check en modo monitorización frente a enforcement.

## Pruebas

- Unitarias:
  - Mapeo de principal autenticado y errores.
- Integración:
  - Adaptadores de Firebase Auth y App Check con emulador o dobles de contrato.
- E2E:
  - Petición válida e inválida contra el entorno de desarrollo autorizado.
- Visuales:
  - No aplica.

## Dependencias

- E0 y configuración Firebase/App Check — debe completarse antes de finalizar.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿App Check se activa directamente en enforcement?
  - Respuesta (Supuesto): La API lo exige desde la primera versión; las apps pueden requerir una transición coordinada.
  - Fuente de verdad: Informe de discovery v1.0.
  - Alineación: E4.

## Enlaces

- Épica: [E1](EPIC.md)
- Tareas: [TASK-03](TASK-03-bootstrap-python-service.md), [TASK-04](TASK-04-implement-auth-app-check.md), [TASK-05](TASK-05-establish-http-boundaries.md), [TASK-06](TASK-06-deploy-development-service.md)
- Diseño/flujo: [Roadmap](../../ROADMAP.md)
- ADR relacionados: Pendientes de runtime y transporte.

# Tarea técnica — Implementar Firebase Auth y App Check

## Trazabilidad en Milano

- Código: `FD2E5A`.
- Story Points: 5.

## Resumen

Crear los puertos y adaptadores que verifican los tokens de usuario y aplicación y producen un principal autenticado inmutable para la capa de aplicación.

## Justificación

La API no puede confiar en identificadores enviados por el cliente ni en las reglas actuales de Firestore para aislar datos.

## Alcance

Incluido:
1. Definir `AuthenticatedPrincipal` y errores de autenticación sin tipos Firebase en dominio.
2. Extraer tokens de cabeceras con contratos y límites explícitos.
3. Implementar verificación Firebase Auth, expiración, issuer, audience y revocación según la política acordada.
4. Implementar verificación App Check y modos de monitorización/enforcement configurables solo durante transición autorizada.
5. Inyectar el principal en endpoints protegidos y prohibir `uid` autoritativo en payloads.
6. Añadir fakes y pruebas negativas de identidad cruzada.

Excluido:
- Inicio de sesión móvil.
- Activación del SDK App Check en iOS y Android.
- Autorización premium.

## Criterios de aceptación

- Tokens válidos producen un principal server-side con `uid` verificado.
- Tokens ausentes, inválidos, expirados o incompatibles se rechazan antes de ejecutar aplicación.
- Un `uid` forjado en la petición no altera el ámbito.
- Los errores no contienen tokens, claims sensibles ni detalles del SDK.

## Riesgo de no realizarla

Un atacante podría invocar la API directamente o intentar acceder a datos de otra cuenta.

## Pruebas

- Unitarias:
  - Extracción, mapeo de principal y errores.
- Integración:
  - Contrato de verificación con Firebase emulado o dobles firmados controlados.
- La funcionalidad existente no debe verse afectada (regresión).

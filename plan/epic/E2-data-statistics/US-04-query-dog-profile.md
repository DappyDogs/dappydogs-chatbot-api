# Historia de usuario — Consultar el perfil normalizado del perro

## Objetivo

**COMO** usuario autenticado
**NECESITO** preguntar por el perfil de mi perro
**PARA** obtener datos correctos y comprensibles sin navegar por distintas pantallas

## Contexto

`Users` contiene dueño y perro en un único documento, con fechas textuales, catálogos numéricos y diferencias de campos entre plataformas. La API debe traducirlo a un modelo canónico limitado al usuario autenticado.

## Alcance

Incluido:
- Repositorio autorizado de `Users`.
- Normalización de perfil y catálogos.
- Tool y respuesta fundamentada de perfil.

Excluido:
- Datos de paseo en curso, amigos, premium y ubicación.
- Varios perros por cuenta.

## Criterios de aceptación

- **AC.01.** Caso: perfil disponible
  Dado un usuario autenticado con perfil válido;
  Cuando consulta un dato soportado de su perro;
  Entonces recibe el valor normalizado correspondiente y no datos de otro usuario.
- **AC.02.** Caso: catálogo conocido
  Dado un valor numérico con traducción canónica;
  Cuando se construye el perfil;
  Entonces se devuelve su representación de dominio acordada.
- **AC.03.** Caso: dato ausente o inválido
  Dado un campo que no puede normalizarse con seguridad;
  Cuando se solicita;
  Entonces la respuesta declara la ausencia sin inventar un valor.

## Casos límite / fallos

- Documento inexistente, fecha inválida, catálogo desconocido y discrepancia de foto entre plataformas.

## Pruebas

- Unitarias:
  - Normalizadores de fecha y catálogos.
- Integración:
  - Lectura autorizada de `Users` con documentos representativos.
- E2E:
  - Casos de perfil incluidos en el catálogo.
- Visuales:
  - No aplica.

## Dependencias

- US-02, US-03 y evidencia de E0 — depende de.

## Preguntas de refinamiento (antes de pasar a «Ready»)

- ¿Cuáles son los catálogos canónicos de raza, sexo y rasgos?
  - Respuesta (Supuesto): Deben extraerse y validarse con ambos repositorios móviles.
  - Fuente de verdad: Informe de discovery v1.0.
  - Alineación: TASK-10.

## Enlaces

- Épica: [E2](EPIC.md)
- Tareas: [TASK-10](TASK-10-normalize-users-profile.md), [TASK-11](TASK-11-expose-profile-capability.md)
- Diseño/flujo: [Roadmap](../../ROADMAP.md)
- ADR relacionados: Modelo canónico pendiente.

# Tarea técnica — Construir el banco automatizado del catálogo

## Trazabilidad en Milano

- Código: `FD2EAE`.
- Story Points: 5.

## Resumen

Convertir el catálogo validado en fixtures, escenarios y aserciones reproducibles para dominio, tools, orquestación y evaluación controlada del modelo.

## Justificación

La aceptación no puede depender de demostraciones manuales ni de evaluar únicamente la fluidez textual de respuestas.

## Alcance

Incluido:
1. Asignar identificador estable a cada consulta y acción del catálogo.
2. Crear datos sintéticos o anonimizados mínimos y resultados deterministas esperados.
3. Relacionar cada caso con tool, argumentos, caso de uso y aserciones de respuesta.
4. Separar pruebas deterministas de evaluación contra proveedor real.
5. Cubrir datos ausentes, ambigüedad, fuera de alcance y seguridad veterinaria.
6. Generar un reporte legible con versión de catálogo, código, configuración y resultado.
7. Ejecutar las capacidades de perfil y actividad contra todas las variaciones observadas de `Users` y `Routes` que puedan afectar a su salida.

## Entrega progresiva entre sprints

Esta tarea sigue siendo la única autoridad técnica del banco final del catálogo, pero sus prerrequisitos y activos reutilizables se desarrollan de forma incremental en lugar de aplazarse hasta la estabilización.

- Sprint 1: versionar el formato del catálogo, asignar identificadores estables y definir los contratos de fixtures y resultados esperados, incluida la cobertura de variantes de `Users`.
- Sprint 2: añadir fixtures y aserciones deterministas de perfil, actividad y salud a medida que estén disponibles las capacidades de E2 y E3; salud utiliza exclusivamente el nuevo esquema correcto.
- Sprint 3: añadir escenarios de contrato móvil, fallos controlados e integración extremo a extremo sin convertir la validación visual móvil en parte de la suite de este repositorio.
- Sprint 4: ejecutar el banco offline completo, realizar cualquier evaluación separada y autorizada contra el proveedor, vincular los resultados a la versión candidata y producir el informe de aceptación.

Las fases anteriores no completan esta tarea. La finalización requiere el catálogo acordado completo, todas las aserciones deterministas aplicables y el informe final reproducible.

Excluido:
- Capturas o validación visual móvil.
- Uso de datos personales no anonimizados.
- Pruebas que escriban, reparen o migren documentos heredados.

## Criterios de aceptación

- Cada caso del catálogo está relacionado con al menos una prueba automatizada.
- Las cifras se comparan con resultados deterministas, no con texto libre del modelo.
- El harness puede ejecutarse sin red mediante fakes.
- La evaluación real es explícita, autorizada y separada de la suite ordinaria.
- Cada variante heredada que afecte a `Users` o `Routes` tiene un resultado esperado de adaptación, exclusión o diagnóstico sanitizado.

## Riesgo de no realizarla

Regresiones funcionales o del modelo podrían pasar inadvertidas y la aceptación no sería reproducible.

## Pruebas

- Unitarias:
  - Carga, validación y reporting del catálogo.
- Integración:
  - Ejecución de todos los casos sobre la aplicación con dependencias controladas.
- La funcionalidad existente no debe verse afectada (regresión).

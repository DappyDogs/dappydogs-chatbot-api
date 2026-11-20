# Tarea técnica — Evaluar y seleccionar el proveedor de IA

## Trazabilidad en Milano

- Código: `FD2E66`.
- Story Points: 3.

## Resumen

Construir un banco controlado de evaluación y seleccionar proveedor/modelo por calidad, tools, seguridad, latencia, privacidad y compatibilidad operativa.

## Justificación

El proveedor está abierto y condiciona el contrato de salida estructurada, la región de tratamiento, los timeouts y los metadatos de uso.

## Alcance

Incluido:
1. Derivar casos de evaluación del catálogo validado, incluidos ambigüedad, fuera de alcance y seguridad veterinaria.
2. Definir métricas y umbrales para selección de tools, argumentos, grounding, idioma, latencia y fallos.
3. Implementar un harness reproducible que elimine o anonimice datos personales.
4. Evaluar candidatos con configuración comparable y registrar resultados agregados.
5. Revisar tratamiento de datos, región, retención y opciones de no entrenamiento.
6. Seleccionar proveedor/modelo y documentar límites, timeouts y metadata disponibles.

Excluido:
- Fine-tuning o entrenamiento.
- Prompts finales de todas las capacidades.

## Criterios de aceptación

- La decisión se apoya en resultados reproducibles del catálogo, no en ejemplos aislados.
- El candidato seleccionado cumple los umbrales de tools y seguridad acordados.
- Las condiciones de tratamiento y región son compatibles con la política aprobada.
- El harness no persiste prompts con datos reales ni respuestas sensibles.

## Riesgo de no realizarla

La API quedaría acoplada a un proveedor que no cumple fiabilidad, privacidad o comportamiento estructurado.

## Pruebas

- Unitarias:
  - Scoring y parsing de resultados.
- Integración:
  - Evaluación controlada de cada proveedor candidato.
- La funcionalidad existente no debe verse afectada (regresión).

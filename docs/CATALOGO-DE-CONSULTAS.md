# Catálogo general de consultas conversacionales

## Propósito

Este documento organiza las intenciones que el chatbot debe reconocer y ofrece variaciones representativas de cómo puede expresarlas una persona. No es una lista cerrada de frases literales: el modelo interpreta lenguaje natural y selecciona una capacidad tipada, mientras que la aplicación valida los argumentos y genera respuestas fundamentadas.

Los ejemplos sirven como catálogo funcional y como base para evaluaciones conversacionales. Una intención se considera disponible cuando existe una capacidad registrada y probada; las funcionalidades futuras se identifican expresamente como planificadas.

## Estado de las capacidades

| Área | Documento específico | Estado |
|---|---|---|
| Directorio y perfil de mascotas | [Capacidad conversacional de perfil](CAPACIDAD-DE-PERFIL.md) | Disponible con fuente temporal de desarrollo |
| Actividad, paseos y estadísticas | Pendiente de `CAPACIDAD-DE-ACTIVIDAD.md` | Planificada |
| Salud, vacunación y recordatorios | Pendiente de `CAPACIDAD-DE-SALUD.md` | Planificada |
| Acciones con confirmación | Pendiente de la capacidad funcional correspondiente | Planificada |

## Directorio de mascotas

| Intención | Variaciones representativas | Capacidad | Estado del contrato |
|---|---|---|---|
| Saber si hay mascotas | «¿Tengo alguna mascota guardada?»<br/>«¿Tengo mascotas registradas?»<br/>«¿Hay algún perro en mi perfil?» | `get_registered_pets` | Disponible |
| Contar mascotas | «¿Cuántas mascotas tengo?»<br/>«¿Cuántos perros tengo registrados?»<br/>«Dime el número de mascotas guardadas» | `get_registered_pets` | Disponible para `0..N` |
| Confirmar el recuento | «¿Entonces solo tengo una?»<br/>«¿Es decir, tengo tres?»<br/>«¿No tengo ninguna?» | `get_registered_pets` con contexto conversacional | Disponible |
| Enumerar nombres | «¿Cómo se llaman mis mascotas?»<br/>«Dime los nombres de mis perros»<br/>«¿Qué mascotas tengo guardadas?» | `get_registered_pets` | Disponible cuando los nombres existen |

El recuento total es independiente del número de nombres recuperados. La fuente definitiva podrá utilizar una consulta agregada y paginar los nombres sin alterar el total real.

## Perfil de una mascota

Las consultas pueden referirse al perfil actual o seleccionar una mascota por su nombre. En los ejemplos se utiliza `Dappy` únicamente como nombre sintético.

| Intención | Variaciones representativas | Campos solicitados | Estado |
|---|---|---|---|
| Consultar el nombre | «¿Cómo se llama mi perro?»<br/>«¿Qué nombre tiene mi mascota?»<br/>«Dime el nombre de mi perro» | `name` | Disponible |
| Consultar la fecha de nacimiento | «¿Cuándo nació mi perro?»<br/>«¿Qué fecha de nacimiento tiene?»<br/>«Dime cuándo nació Dappy» | `birth_date` y, si procede, `pet_name` | Disponible |
| Consultar la raza | «¿Qué raza tiene Dappy?»<br/>«¿Cuál es la raza de Dappy?»<br/>«¿De qué raza es Dappy?»<br/>«Dime la raza de Dappy» | `breed` y `pet_name` | Disponible; devuelve el código mientras no exista catálogo verificado |
| Consultar el sexo | «¿Cuál es el sexo de mi perro?»<br/>«¿Qué sexo tiene Dappy?»<br/>«Dime el sexo registrado de mi mascota» | `gender` y, si procede, `pet_name` | Disponible; devuelve el código mientras no exista catálogo verificado |
| Consultar la sociabilidad | «¿Qué nivel de sociabilidad tiene?»<br/>«¿Cómo de sociable es Dappy?»<br/>«Dime la sociabilidad registrada» | `sociability` y, si procede, `pet_name` | Disponible; devuelve el código mientras no exista catálogo verificado |
| Consultar la energía | «¿Qué nivel de energía tiene?»<br/>«¿Cuánta energía tiene Dappy?»<br/>«Dime el nivel de energía registrado» | `energy` y, si procede, `pet_name` | Disponible; devuelve el código mientras no exista catálogo verificado |
| Combinar datos | «¿Cómo se llama y qué raza tiene?»<br/>«Dime el nombre, el sexo y la energía de Dappy»<br/>«Repite el nombre y la raza de mi mascota» | Combinación mínima de campos | Disponible |

Cuando el usuario escribe un nombre que no corresponde a ninguna mascota de su cuenta, la respuesta indica que esa mascota no está registrada. La selección nunca amplía la búsqueda a otras cuentas.

## Interacción social

| Intención | Variaciones representativas | Comportamiento |
|---|---|---|
| Saludar | «Hola»<br/>«Buenas»<br/>«Hello» | Respuesta determinista sin consultar datos |
| Agradecer | «Gracias»<br/>«Muchas gracias»<br/>«Thank you» | Respuesta determinista sin consultar datos |
| Despedirse | «Adiós»<br/>«Hasta luego»<br/>«Nos vemos»<br/>«Bye» | Respuesta determinista sin consultar datos |

Los mensajes sociales se resuelven directamente solo cuando constituyen el mensaje completo. Una frase como «Adiós, pero antes dime la raza de Dappy» continúa por el flujo funcional.

## Capacidades planificadas

Las siguientes familias pertenecen al alcance general, pero todavía no están disponibles y no deben presentarse como respuestas implementadas:

| Área | Ejemplos de intención |
|---|---|
| Actividad y paseos | «¿Cuánto ha paseado esta semana?», «¿Cuál fue su último paseo?», «¿Qué distancia recorrió?» |
| Estadísticas | «Compara este mes con el anterior», «¿Cuánto tiempo ha paseado hoy?» |
| Salud y vacunación | «¿Qué vacunas tiene?», «Registra una vacuna», «¿Cuándo toca la siguiente dosis?» |
| Recordatorios | «Recuérdame la próxima vacuna», «¿Qué cuidados tengo pendientes?» |
| Edad calculada | «¿Cuántos años tiene Dappy?» |

Cada nueva familia deberá disponer de su documento `CAPACIDAD-DE-*.md`, tools cerradas, reglas de autorización, respuestas fundamentadas y pruebas antes de pasar a estado disponible en este catálogo.

## Criterios para las variaciones

- Las variaciones representan una misma intención semántica; no requieren una coincidencia literal con el texto documentado.
- Los nombres de mascota se tratan como datos proporcionados por el usuario y se validan antes de consultar la fuente.
- Una falta ortográfica puede cambiar el nombre seleccionado y producir un resultado ausente; no se corrigen nombres por inferencia.
- Las preguntas ambiguas deben solicitar contexto o utilizar el perfil actual solo cuando el contrato de la capacidad lo permita.
- La respuesta final utiliza exclusivamente datos devueltos por capacidades autorizadas y nunca completa etiquetas de catálogo por inferencia.

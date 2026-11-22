# Adaptación de solo lectura del perfil heredado

## Propósito

Este documento describe cómo la API consume el perfil del perro almacenado en la colección heredada `Users` sin modificar, corregir ni migrar documentos existentes.

La colección combina datos de cuenta, propietario, perro, dispositivo, localización, suscripción, relaciones y estado de paseo. La API selecciona únicamente los campos necesarios para las consultas de perfil y los transforma en un modelo canónico reducido.

## Autoridad e identidad

El repositorio recibe un `AuthenticatedPrincipal` producido por Firebase Auth y App Check. La ruta de lectura se deriva exclusivamente de `principal.uid`:

```text
Users/{principal.uid}
```

El repositorio no acepta un identificador de usuario procedente del cuerpo HTTP, del modelo de lenguaje ni de los argumentos de una herramienta. El campo heredado `userId` se utiliza únicamente como señal de compatibilidad: una ausencia o discrepancia genera un diagnóstico saneado, pero no cambia la identidad efectiva.

## Modelo canónico

El modelo `DogProfile` contiene exclusivamente:

- Nombre del perro.
- Fecha o año de nacimiento y su precisión.
- Raza.
- Sexo.
- Sociabilidad.
- Energía.
- Diagnósticos de compatibilidad expresados mediante categorías cerradas.

No contiene identificadores, correo electrónico, nombre del propietario, imágenes, tokens de dispositivo, coordenadas, estado premium, amistades ni estado del paseo. Estos campos tampoco aparecen en los fixtures ni en los logs del adaptador.

## Estados heredados

El contrato bruto diferencia para cada campo relevante:

- Campo ausente.
- Valor `null`.
- Cadena vacía.
- Valor presente.
- Valor presente con tipo o formato inválido.

La exportación de 898 documentos produce siete firmas estructurales distintas cuando se consideran únicamente los campos relevantes para perfil. Las siete están representadas mediante fixtures sintéticos y anonimizados. Los valores personales reales no forman parte del repositorio.

## Fechas de nacimiento

`dogDate` se interpreta mediante reglas deterministas:

- Cuatro dígitos numéricos representan únicamente un año y conservan precisión anual.
- Nueve o diez dígitos numéricos representan segundos desde época Unix y producen una fecha civil UTC.
- El resultado debe estar entre la fecha actual y el límite conservador de treinta años configurado para datos heredados.
- Cadenas como `"null"`, longitudes desconocidas, fechas futuras o valores fuera de rango permanecen sin normalizar.

La adaptación no inventa mes, día ni zona horaria cuando el origen no los proporciona.

## Catálogos numéricos

Raza, sexo, sociabilidad y energía se almacenan como enteros. Las etiquetas deben proceder de catálogos contrastados con las aplicaciones iOS y Android y se inyectan mediante `ProfileCatalogs`.

Hasta disponer de esa verificación:

- El código numérico se conserva dentro del contrato de compatibilidad.
- La etiqueta permanece ausente.
- El estado del catálogo es `unknown`.
- Se genera el diagnóstico `unknown_catalog_value`.
- El modelo de lenguaje no debe inferir una etiqueta.

Los catálogos se copian y congelan al configurar el normalizador para impedir cambios accidentales durante la ejecución.

## Adaptadores disponibles

### Firestore

`FirestoreDogProfileRepository` lee exclusivamente `Users/{uid}` y traduce los fallos del SDK a un error de fuente saneado. La interfaz utiliza protocolos propios para que el dominio y la normalización no dependan de tipos de Firebase.

### Snapshot local

`LocalSnapshotDogProfileRepository` permite desarrollar contra una exportación local de solo lectura. Comprueba que el identificador resuelva dentro del directorio configurado, rechaza contratos JSON malformados y nunca escribe en la copia.

El adaptador local es una herramienta de desarrollo; no forma parte del despliegue productivo.

## Diagnósticos y privacidad

Los diagnósticos se limitan a pares de categorías como:

- Campo e incidencia.
- Ausente, nulo, vacío, inválido o incoherente.
- Código de catálogo desconocido.

No incorporan identificadores, valores originales ni contenido personal. Los errores de proveedor tampoco exponen el detalle interno del SDK.

## Evidencia automatizada

Las pruebas verifican:

- Aislamiento de la lectura mediante la identidad autenticada.
- Rechazo de recorridos de ruta en el adaptador local.
- Contratos ausentes o JSON malformado.
- Equivalencia entre documentos sintéticos representativos de iOS y Android.
- Las siete firmas estructurales relevantes observadas en los 898 documentos.
- Fechas de cuatro, nueve y diez dígitos y formatos inválidos.
- Catálogos conocidos, desconocidos e inmutables.
- Exclusión de correo, token, localización, suscripción y relaciones.
- Saneamiento de fallos de Firestore.

Además, una auditoría privada ejecuta el normalizador contra los 898 documentos exportados y solo informa de recuentos agregados.

## Dependencias pendientes

Para cerrar la integración funcional todavía es necesario:

1. Obtener y contrastar los catálogos canónicos de iOS y Android.
2. Inicializar el cliente real de Firestore en el runtime finalmente elegido.
3. Ejecutar la prueba autorizada contra emulador o entorno de desarrollo.
4. Conectar el repositorio con la capacidad conversacional de perfil.


# Acceso al perfil de usuario

## Propósito

Este documento describe el contrato con el que la API accede al perfil del perro asociado al usuario autenticado.

La API selecciona exclusivamente la información necesaria para las funcionalidades de perfil y la proyecta sobre un modelo de producto reducido. La estructura interna de la fuente de datos no se expone al modelo conversacional ni a los clientes de la API.

## Autoridad e identidad

El repositorio recibe un `AuthenticatedPrincipal` producido por Firebase Auth y App Check. La ruta de lectura se deriva exclusivamente de `principal.uid`:

```text
Users/{principal.uid}
```

El repositorio no acepta un identificador de usuario procedente del cuerpo HTTP, del modelo de lenguaje ni de los argumentos de una herramienta. El campo `userId` de la fuente se utiliza únicamente como señal de compatibilidad: una ausencia o discrepancia genera un diagnóstico saneado, pero no cambia la identidad efectiva.

## Modelo canónico

El modelo `DogProfile` contiene exclusivamente:

- Nombre del perro.
- Fecha o año de nacimiento y su precisión.
- Raza.
- Sexo.
- Sociabilidad.
- Energía.
- Diagnósticos de compatibilidad expresados mediante categorías cerradas.

El directorio de mascotas representa una colección `0..N` asociada al principal autenticado. Cada entrada contiene una referencia interna estable y el nombre cuando está disponible. La consulta de cantidad se calcula a partir de esa colección, no mediante una estimación del modelo.

La fuente temporal actual contiene un único perro embebido en `Users/{uid}` y, por tanto, su adaptador solo puede aportar cero o una entrada. Esto no limita el contrato de producto. La consulta Firestore definitiva para múltiples mascotas se implementará cuando se identifiquen y validen la colección real, su relación de propiedad y sus reglas de acceso.

No contiene identificadores, correo electrónico, nombre del propietario, imágenes, tokens de dispositivo, coordenadas, estado premium, amistades ni estado del paseo. Estos campos tampoco aparecen en los fixtures ni en los logs del adaptador.

## Estados de los datos de origen

El contrato bruto diferencia para cada campo relevante:

- Campo ausente.
- Valor `null`.
- Cadena vacía.
- Valor presente.
- Valor presente con tipo o formato inválido.

La fuente actual presenta siete firmas estructurales distintas cuando se consideran únicamente los campos relevantes para perfil. Todas están representadas mediante fixtures sintéticos y anonimizados. Los valores personales reales no forman parte del repositorio.

## Fechas de nacimiento

`dogDate` se interpreta mediante reglas deterministas:

- Cuatro dígitos numéricos representan únicamente un año y conservan precisión anual.
- Nueve o diez dígitos numéricos representan segundos desde época Unix y producen una fecha civil UTC.
- El resultado debe estar entre la fecha actual y el límite conservador de treinta años configurado para los datos de origen.
- Cadenas como `"null"`, longitudes desconocidas, fechas futuras o valores fuera de rango permanecen sin normalizar.

La adaptación no inventa mes, día ni zona horaria cuando el origen no los proporciona.

## Catálogos numéricos

Raza, sexo, sociabilidad y energía se almacenan como enteros. Las etiquetas deben proceder de catálogos contrastados con las aplicaciones iOS y Android y se inyectan mediante `ProfileCatalogs`.

La capacidad conversacional conserva estos enteros como datos disponibles mientras no exista una correspondencia verificada. El resultado los identifica como `catalog_code`, por lo que la aplicación comunica el código exacto sin inferir una raza, sexo, sociabilidad o nivel de energía. La integración conversacional se describe en [Capacidad conversacional de perfil](CAPACIDAD-DE-PERFIL.md).

Hasta disponer de esa verificación:

- El código numérico se conserva dentro del contrato de compatibilidad.
- La etiqueta permanece ausente.
- El estado del catálogo es `unknown`.
- Se genera el diagnóstico `unknown_catalog_value`.
- El modelo de lenguaje no debe inferir una etiqueta.

Los catálogos se copian y congelan al configurar el normalizador para impedir cambios accidentales durante la ejecución.

## Fuentes de datos

### Firestore

`FirestoreDogProfileRepository` lee exclusivamente `Users/{uid}` y traduce los fallos del SDK a un error de fuente saneado. La interfaz utiliza protocolos propios para que el dominio y la normalización no dependan de tipos de Firebase.

### Snapshot de desarrollo

`LocalSnapshotDogProfileRepository` permite validar el producto contra una exportación de solo lectura. Comprueba que el identificador resuelva dentro del directorio configurado, rechaza contratos JSON malformados y nunca escribe en la copia.

Esta fuente es temporal y se utiliza para desarrollar y verificar las capacidades sin afectar a los documentos existentes. El contrato de aplicación se mantiene estable cuando la fuente se sustituya por Firestore.

## Diagnósticos y privacidad

Los diagnósticos se limitan a pares de categorías como:

- Campo e incidencia.
- Ausente, nulo, vacío, inválido o incoherente.
- Código de catálogo desconocido.

No incorporan identificadores, valores originales ni contenido personal. Los errores de proveedor tampoco exponen el detalle interno del SDK.

## Evidencia automatizada

Las pruebas verifican:

- Aislamiento de la lectura mediante la identidad autenticada.
- Rechazo de recorridos de ruta en el adaptador de snapshot.
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
2. Identificar la fuente real de múltiples mascotas y su relación con el usuario autenticado.
3. Implementar el adaptador Firestore del directorio `0..N` sin exponer identificadores de usuario al modelo.
4. Inicializar el cliente real de Firestore en el runtime finalmente elegido.
5. Ejecutar la prueba autorizada contra emulador o entorno de desarrollo.


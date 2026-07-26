# Guía de adopción

## Elegir perfil

| Perfil | Usar cuando | Artefacto central |
|---|---|---|
| Conversacional | El resultado principal es comportamiento de un bot, agente o prompt | Constitución, Behavior Specs y Test Suite |
| Software | El resultado principal es una aplicación, API o automatización determinista | PRD, SDD, BDD y TDD |
| Híbrido | Software y comportamiento conversacional cambian juntos | Ambas cadenas con trazabilidad coordinada |

El riesgo se elige de forma independiente. Un bot puede ser R3 y una aplicación puede ser R0.

## Proyecto nuevo

1. Ejecutar `humanio init`.
2. Resolver Constitución, contexto, alcance y fuentes.
3. Completar requisitos o reglas del primer incremento.
4. Definir escenarios y pruebas.
5. Actualizar trazabilidad.
6. Ejecutar validación normal durante descubrimiento.
7. Ejecutar validación estricta antes de aprobar.

## Repositorio existente

No ejecutar el inicializador directamente sobre archivos que ya existen.

1. Auditar documentación, código, pruebas, despliegue y fuentes.
2. Clasificar confirmados, inferencias, pendientes y contradicciones.
3. Generar una línea base Humanio en un directorio temporal.
4. Reconciliar la documentación existente con el orden de autoridad.
5. Copiar o adaptar un artefacto por vez.
6. Mantener los IDs existentes cuando sean estables y no ambiguos.
7. Ejecutar las pruebas reales del repositorio.
8. Activar validación estricta en CI cuando la migración esté completa.

## Cambios posteriores

1. Registrar el cambio con ID `CHG-###`.
2. Modificar primero la fuente de mayor autoridad.
3. Propagar requisitos, diseño, escenarios y pruebas.
4. Implementar el cambio mínimo.
5. Registrar evidencia.
6. Evaluar readiness según riesgo.

## Antipatrones

- Completar todos los documentos con texto genérico.
- Duplicar datos volátiles que ya tienen fuente canónica.
- Editar el prompt compilado sin cambiar sus reglas fuente.
- Crear trazabilidad ficticia para eliminar alertas.
- Confundir prueba escrita con prueba ejecutada.

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
2. Ejecutar `humanio install --adapter auto`.
3. Resolver Constitución, contexto, alcance y fuentes.
4. Completar requisitos o reglas del primer incremento.
5. Definir escenarios y pruebas.
6. Actualizar trazabilidad.
7. Ejecutar validación normal durante descubrimiento.
8. Ejecutar validación estricta antes de aprobar.

## Repositorio existente

1. Auditar documentación, código, pruebas, despliegue y fuentes.
2. Clasificar confirmados, inferencias, pendientes y contradicciones.
3. Simular `humanio init --adopt` y revisar cualquier colisión distinta de
   `README.md` o `AGENTS.md`.
4. Ejecutar la adopción cuando el destino sea seguro.
5. Instalar explícitamente los adaptadores requeridos.
6. Reconciliar la documentación existente con el orden de autoridad.
7. Mantener los IDs existentes cuando sean estables y no ambiguos.
8. Ejecutar las pruebas reales del repositorio.
9. Activar validación estricta en CI cuando la migración esté completa.

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

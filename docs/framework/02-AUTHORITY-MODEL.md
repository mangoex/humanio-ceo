# Modelo de autoridad y propagación

## Jerarquía general

1. Constitución y decisiones confirmadas.
2. PRD y reglas de negocio.
3. Blueprint, Behavior Specs y SDD.
4. ADR vigentes.
5. BDD, TDD y evaluaciones.
6. Roadmap y tareas.
7. Prompt o código.

Una capa inferior no puede redefinir silenciosamente una capa superior.

## Fuentes canónicas operativas

Datos como precios, menús, inventarios, disponibilidad, tiempos, direcciones y políticas vigentes deben residir en la fuente autorizada más adecuada.

El prompt conserva la instrucción de consulta y el comportamiento de contingencia, no una copia innecesaria del dato.

## Clasificación de información

| Estado | Definición | Uso |
|---|---|---|
| Confirmado | Decisión o evidencia explícita | Puede gobernar requisitos |
| Inferido | Deducción razonable aún no aprobada | Debe señalarse |
| Pendiente | Decisión necesaria no resuelta | Puede bloquear |
| Contradictorio | Dos fuentes incompatibles | Detener propagación |

## Propagación de cambios

1. Crear `CHG-###`.
2. Formular el cambio como comportamiento observable.
3. Identificar fuente de autoridad e IDs afectados.
4. Resolver contradicciones.
5. Actualizar requisitos o reglas.
6. Actualizar diseño.
7. Actualizar BDD, TDD o evaluaciones.
8. Implementar el cambio mínimo.
9. Ejecutar pruebas afectadas y regresiones críticas.
10. Actualizar trazabilidad, evidencia y changelog.

## Identificadores

| Elemento | Formato |
|---|---|
| Objetivo | `OBJ-###` |
| Requisito funcional | `PRD-FR-###` |
| Requisito no funcional | `PRD-NFR-###` |
| Regla de comportamiento | `BS-RULE-###` |
| Flujo | `BS-FLOW-###` |
| Decisión arquitectónica | `ADR-###` |
| Escenario | `BDD-SC-###` |
| Prueba | `TDD-TC-###` |
| Evaluación conversacional | `PBD-T-###` |
| Riesgo | `RSK-###` |
| Cambio | `CHG-###` |
| Evidencia | `EVD-###` |

Los IDs se mantienen estables y no se reutilizan.

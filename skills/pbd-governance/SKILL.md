---
name: pbd-governance
description: Crea, audita o actualiza constituciones y reglas Prompt/Policy-Based Development, resolviendo autoridad, excepciones, controles sensibles y propagación ordenada de cambios.
---

# PBD Governance

Gobernar comportamiento y decisiones mediante reglas explícitas, versionadas y comprobables.

## Procedimiento

1. Leer la constitución y el modelo de autoridad.
2. Identificar la fuente canónica de cada regla afectada.
3. Asignar o conservar IDs estables.
4. Definir regla, motivo, alcance, excepción y control.
5. Resolver contradicciones desde la fuente de mayor autoridad.
6. Si cambia un ADR, registrar explícitamente el estado anterior como reemplazado o revocado, la decisión sucesora, el impacto y la aprobación requerida.
7. Propagar el cambio hacia especificaciones, escenarios, pruebas y compilados.
8. Registrar la evidencia de la transición y los artefactos afectados.

## Controles

- Tratar acciones financieras, datos sensibles, comunicaciones externas e irreversibilidad como controles explícitos.
- Separar propuesta, aprobación y ejecución cuando el riesgo lo requiera.
- Mantener visible toda excepción temporal.
- No editar un prompt compilado como fuente primaria.

## Salida

- Reglas afectadas e IDs.
- Fuente de autoridad.
- Conflictos resueltos o pendientes.
- Artefactos derivados que deben actualizarse.
- Aprobaciones y evidencia.

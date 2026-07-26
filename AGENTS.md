# Humanio CEO Engineering Framework

Este repositorio es la fuente canónica del plugin `humanio-ceo`.

## Orden de autoridad

Aplicar esta prioridad:

1. `docs/framework/00-CONSTITUTION.md`
2. Decisiones confirmadas y ADR vigentes.
3. Requisitos y reglas de negocio.
4. Blueprint, Behavior Specs y SDD.
5. BDD, TDD y evaluaciones.
6. Planes y tareas.
7. Prompt o código.

No modificar una capa inferior para ocultar una contradicción en una capa superior.

## Reglas de trabajo

- Distinguir siempre información confirmada, inferida, pendiente y contradictoria.
- Trabajar por incrementos verticales y verificables.
- Mantener identificadores estables.
- Actualizar especificaciones y pruebas antes del prompt o código afectado.
- No declarar pruebas aprobadas sin evidencia de ejecución.
- No introducir secretos, credenciales ni datos personales en ejemplos o fixtures.
- No publicar ni desplegar sin completar los gates aplicables.
- Preservar los documentos consultivos existentes salvo decisión explícita de migración.

## Perfiles

- `conversational`: bots, agentes, asistentes y prompts maestros.
- `software`: aplicaciones, APIs, SaaS y sistemas.
- `hybrid`: software con componentes conversacionales o agentes.

## Niveles de riesgo

- `R0`: experimento o documento.
- `R1`: automatización interna de bajo riesgo.
- `R2`: sistema productivo estándar.
- `R3`: dinero, datos sensibles, decisiones críticas o impacto regulado.

El perfil determina los artefactos. El riesgo determina el rigor y los gates.

## Validación

Antes de cerrar un cambio:

1. Validar estructura del plugin y skills.
2. Revisar IDs y referencias.
3. Verificar trazabilidad.
4. Registrar pruebas realmente ejecutadas.
5. Reportar riesgos, pendientes y siguiente incremento.

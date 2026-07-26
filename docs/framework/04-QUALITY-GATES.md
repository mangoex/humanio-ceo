# Puertas de calidad

## Gate 0 — Entrada suficiente

- Problema, usuario y resultado identificados.
- Fuentes inventariadas.
- Confirmados, inferidos, pendientes y contradicciones visibles.
- Decisiones bloqueantes identificadas.

## Gate 1 — Gobierno

- Constitución o reglas vigentes.
- Alcance y exclusiones claros.
- Perfil y riesgo definidos.
- Fuentes canónicas exactas.
- Contradicciones resueltas o bloqueadas.

## Gate 2 — Diseño trazable

- Requisitos con IDs.
- Blueprint, Behavior Specs o SDD aplicables.
- Estados, integraciones, permisos e invariantes.
- ADR para decisiones relevantes.
- Riesgos con mitigación y dueño.

## Gate 3 — Pruebas definidas

- Flujo feliz.
- Alternos y datos faltantes.
- Errores e integraciones.
- Permisos y seguridad.
- Fallos de herramienta.
- Regresiones críticas.
- Trazabilidad de escenario a requisito.

## Gate 4 — Implementación verificada

- Prompt o código rastreable.
- Pruebas ejecutadas con comando, fecha y resultado.
- Evidencia registrada.
- Sin secretos ni datos personales innecesarios.
- Sin errores críticos abiertos.

## Gate 5 — Producción

- Responsable humano.
- Observabilidad y logs.
- Modo degradado.
- Rollback.
- Métricas iniciales.
- Riesgos residuales aceptados.
- Aprobación registrada.

## Gate 6 — Operación gobernada

- Métricas revisadas.
- Incidentes registrados.
- Conocimiento actualizado.
- Deriva evaluada.
- Backlog y siguiente incremento.

## Regla de evidencia

Usar estados separados:

- `defined`
- `implemented`
- `executed`
- `passed`
- `approved`

Ningún estado implica automáticamente el siguiente.

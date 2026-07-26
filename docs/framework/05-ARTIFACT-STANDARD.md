# Estándar de artefactos

## Principios

- Una sola fuente de autoridad por decisión.
- IDs únicos y estables.
- Enlaces explícitos entre capas.
- Plantillas adaptadas por perfil y riesgo.
- Contenido pendiente marcado, nunca oculto.

## Artefactos comunes

- Contexto.
- Constitución.
- Registro de fuentes.
- Riesgos.
- Matriz de trazabilidad.
- Registro de cambios.
- Evidencias.
- Roadmap.

## Perfil conversacional

- Constitution.
- Behavior Specs.
- Test Suite.
- Master Prompt.

## Perfil software

- Contexto de producto.
- PRD.
- SDD.
- ADR.
- BDD.
- TDD.
- Trazabilidad.
- Roadmap.
- Prompt de importación para Codex.

## Perfil híbrido

Usa el perfil software como armazón y añade el paquete conversacional bajo `docs/pbd/`.

## Matriz mínima

```text
objetivo -> requisito -> diseño -> escenario -> prueba -> implementación -> evidencia
```

Los huecos se señalan; no se rellenan con referencias ficticias.

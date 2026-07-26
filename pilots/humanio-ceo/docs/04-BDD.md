# Behavior-Driven Development

## Feature: PRD-FR-001 — Validación gobernada

### BDD-SC-001 — Autopiloto estricto

```gherkin
Given un workspace híbrido completo de Humanio CEO
When el CI ejecuta humanio validate con modo estricto
Then termina con código cero y sin advertencias
```

## Escenarios cubiertos

- Inicialización de tres perfiles.
- Colisiones de archivos.
- Placeholders.
- Archivos obligatorios.
- IDs duplicados e indefinidos.
- Instalación y paquete reproducible.

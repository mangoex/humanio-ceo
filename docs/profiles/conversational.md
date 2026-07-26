# Perfil conversacional

Aplicar a bots, asistentes, agentes de WhatsApp y productos cuyo comportamiento principal se gobierna mediante instrucciones, conocimiento, herramientas y estado conversacional.

## Artefactos mínimos

```text
docs/pbd/
├── 01-constitution.md
├── 02-behavior-specs.md
├── 03-test-suite.md
└── 04-master-prompt.md
```

## Cobertura

- Identidad, misión y usuarios.
- Jerarquía de instrucciones.
- Fuentes canónicas.
- Guardrails y privacidad.
- Actores, canales y estados.
- Datos mínimos por estado.
- Flujos felices, alternos y de recuperación.
- Herramientas y fallos.
- Escalamiento humano.
- Casos de regresión.

## Regla de compilación

El prompt se compila desde Constitución y Behavior Specs coherentes. No se improvisa primero para documentarlo después.

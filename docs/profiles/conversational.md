# Perfil conversacional

Aplicar a bots, asistentes, agentes de WhatsApp y productos cuyo comportamiento principal se gobierna mediante instrucciones, conocimiento, herramientas y estado conversacional.

## Artefactos mínimos

```text
humanio.yaml
docs/pbd/
├── 01-constitution.md
├── 02-behavior-specs.md
├── 03-test-suite.md
├── 04-master-prompt.md
└── 05-traceability.md
docs/
├── 08-registro-riesgos.md
└── 09-registro-cambios.md
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

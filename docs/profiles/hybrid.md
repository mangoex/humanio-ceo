# Perfil híbrido

Aplicar cuando un producto de software incorpora uno o más bots, agentes, prompts maestros o flujos conversacionales.

## Estructura

Usar el perfil software como armazón. Añadir:

```text
docs/pbd/
├── 01-constitution.md
├── 02-behavior-specs.md
├── 03-test-suite.md
└── 04-master-prompt.md
```

## Reglas

- El PRD gobierna el valor y alcance del producto.
- El SDD gobierna la arquitectura y las integraciones.
- El paquete PBD gobierna el comportamiento conversacional.
- Las reglas compartidas se definen una vez y se referencian.
- BDD/TDD y Test Suite deben cubrir handoffs entre software, agente, herramientas y humanos.
- Un cambio transversal debe registrar todos los IDs afectados.

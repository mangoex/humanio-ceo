# Behavior Specs

## Historias

### BS-US-001

Como mantenedor, quiero que el coordinador seleccione perfil, riesgo y gate para evitar declaraciones de calidad sin evidencia.

## Reglas

### BS-RULE-001

El coordinador no debe declarar `READY` si la validación estricta aplicable termina con código distinto de cero.

Fuente canónica: `docs/framework/06-DEFINITION-OF-DONE.md`.

## Estados

| Estado | Datos mínimos | Acción | Salida |
|---|---|---|---|
| verify | perfil, riesgo y workspace | ejecutar gates | READY, CONDITIONAL o NOT READY |

## Flujos

### BS-FLOW-001 — Verificación

1. Ejecutar validación estricta y pruebas aplicables.
2. Emitir decisión únicamente con evidencia registrada.

## Herramientas y fallos

- Herramientas: CLI, unittest, validadores oficiales y GitHub Actions.
- Fallback: `NOT READY` cuando falta evidencia.
- Escalamiento: decisión del propietario para licencia o riesgos nuevos.

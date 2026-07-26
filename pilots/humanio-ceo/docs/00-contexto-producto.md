# Contexto de producto

## Identidad

- Producto: Humanio CEO Engineering Framework.
- Problema: los proyectos con IA pierden decisiones, trazabilidad y evidencia entre conversación, especificación e implementación.
- Usuarios: responsables de producto, consultores, desarrolladores y agentes Codex.
- Resultado: una línea base gobernada, validable, instalable y reutilizable.

## Objetivos

- `OBJ-001`: distribuir un plugin válido que inicialice y valide proyectos gobernados.

## Alcance

### Incluye

- Plugin, seis skills, plantillas, CLI, pruebas, CI, instalación y empaquetado.

### Excluye

- Despliegue de proyectos consumidores y certificación automática de su readiness.

## Fuentes y decisiones

| Fuente | Autoridad | Estado |
|---|---|---|
| `docs/framework/00-CONSTITUTION.md` | Constitucional | Aprobada |
| `AGENTS.md` | Operativa | Aprobada |
| `VERSION` | Release | Aprobada |

## Restricciones

- Negocio: conservar la neutralidad respecto al modelo.
- Técnicas: biblioteca estándar de Python para el CLI.
- Seguridad: no incluir secretos ni datos reales en fixtures.
- Operación: todo PR debe superar CI.

## Perfil y riesgo

- Perfil: híbrido.
- Nivel: R1.
- Justificación: combina software determinista y skills, sin despliegues o transacciones externas automáticas.

## Criterio del primer incremento

- Capacidad: instalar, inicializar, validar y empaquetar el plugin.
- Gate: validación estricta, pruebas, CI e instalación aislada.
- Evidencia: `EVIDENCE.md`.

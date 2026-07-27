# Contexto de producto

## Identidad

- Producto: Humanio CEO Engineering Framework.
- Problema: los proyectos con IA pierden decisiones, trazabilidad y evidencia entre conversación, especificación e implementación.
- Usuarios: responsables de producto, consultores, desarrolladores y usuarios de
  IDE o agentes con acceso a una terminal.
- Resultado: una línea base gobernada, validable, instalable y reutilizable.

## Objetivos

- `OBJ-001`: distribuir un plugin válido que inicialice y valide proyectos gobernados.
- `OBJ-002`: ejecutar el CLI fuera del checkout desde Windows, macOS o Linux.
- `OBJ-003`: integrar el gobierno Humanio con distintos agentes sin perder
  contenido del proyecto ni acoplar el núcleo a un proveedor.

## Alcance

### Incluye

- Plugin, seis skills, plantillas, CLI portable, adaptadores, pruebas, CI,
  instalación y empaquetado.

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

## Criterio del incremento vigente

- Capacidad: instalar, inicializar, validar, integrar agentes y empaquetar el framework.
- Gate: validación estricta, pruebas, CI, instalación aislada y reversibilidad.
- Evidencia: `EVIDENCE.md`.

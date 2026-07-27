# Product Requirements Document

## Problema

La calidad del marco no puede depender de afirmaciones manuales ni de un checkout parcial.
La instalación vigente está acoplada al marketplace de Codex y obliga a ejecutar el CLI
desde el checkout del framework, lo que limita su adopción en otros IDE y agentes.

## Personas

- Mantenedor que publica el plugin.
- Equipo que lo instala.
- Agente que inicia o audita un proyecto.
- Profesional que trabaja desde cualquier IDE con terminal y requiere el mismo gobierno.

## Alcance y exclusiones

- Incluye: validación, inicialización segura, instalación local, CLI portable,
  adaptadores de agentes y paquete reproducible.
- Excluye: despliegue de aplicaciones consumidoras.
- Excluye: instalar extensiones propietarias de IDE o afirmar compatibilidad automática
  con herramientas sin un adaptador declarado.

## Requisitos funcionales

### PRD-FR-001

El sistema debe crear y validar líneas base para los tres perfiles sin sobrescribir archivos existentes.

Criterio de aceptación: los tres perfiles pasan pruebas y fixtures estrictos.

### PRD-FR-002

El sistema debe instalar un comando `humanio` reutilizable fuera del checkout y
conservar la instalación específica del plugin de Codex.

Criterio de aceptación: una instalación aislada puede ejecutar `humanio doctor`,
inicializar y validar un proyecto sin depender del directorio fuente.

### PRD-FR-003

El sistema debe integrar proyectos con adaptadores `generic`, `codex`, `cursor`,
`claude`, `copilot` y `gemini`, y administrar su ciclo de vida mediante detección,
instalación, sincronización y desinstalación.

Criterios de aceptación:

- Los archivos preexistentes conservan todo contenido ajeno al bloque administrado.
- Una marca administrada incompleta cancela la operación sin escribir.
- La desinstalación elimina únicamente contenido administrado por Humanio.
- El modo `auto` siempre instala el adaptador genérico y añade solo herramientas
  detectadas mediante señales explícitas del repositorio.

## Requisitos no funcionales

### PRD-NFR-001

El sistema debe producir instalaciones y paquetes reproducibles sin dependencias externas de Python.

Métrica: dos paquetes del mismo árbol tienen el mismo SHA-256 y una instalación aislada pasa `doctor`.

### PRD-NFR-002

La integración debe ser determinista, auditable, reversible y compatible con
Windows, macOS y Linux usando únicamente Python 3.11 o posterior.

Métrica: pruebas aisladas verifican `dry-run`, actualización idempotente,
protección de colisiones, sincronización y desinstalación segura.

## Criterios de éxito

- CI aprobado.
- Pruebas automatizadas de framework, release y adaptadores aprobadas.
- Workspace de autopiloto aprobado en modo estricto.

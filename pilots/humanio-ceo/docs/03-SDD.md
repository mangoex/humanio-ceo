# Software Design Document

## Arquitectura

Núcleo declarativo con skills y plantillas, acompañado por un CLI determinista en
Python. Codex se mantiene como distribución especializada; los IDE y agentes se
integran mediante adaptadores desacoplados.

## Componentes

### SDD-CMP-001

- Responsabilidad: coordinar diagnóstico, inicialización, validación, instalación y empaquetado.
- Cubre: PRD-FR-001, PRD-NFR-001.
- Entradas: manifiesto, perfil, riesgo, templates y workspace.
- Salidas: artefactos, hallazgos, códigos de salida, instalación y ZIP.

### SDD-CMP-002

- Responsabilidad: instalar y actualizar el CLI portable en un prefijo de usuario.
- Cubre: PRD-FR-002, PRD-NFR-001, PRD-NFR-002.
- Entradas: árbol validado, prefijo, directorio de binarios y modo de actualización.
- Salidas: copia preparada del runtime y lanzadores `humanio` o `humanio.cmd`.
- Invariantes: no reemplaza un lanzador ajeno, prepara la copia antes de sustituir
  la vigente y permite desinstalación explícita.

### SDD-CMP-003

- Responsabilidad: detectar y materializar adaptadores de proyecto.
- Cubre: PRD-FR-003, PRD-NFR-002.
- Entradas: workspace, adaptadores solicitados y estado `.humanio/integrations.json`.
- Salidas: bloques administrados en archivos nativos y estado auditable.
- Adaptadores:
  - `generic`: `.humanio/README.md`.
  - `codex` y `cursor`: `AGENTS.md`.
  - `claude`: `CLAUDE.md`.
  - `copilot`: `.github/copilot-instructions.md`.
  - `gemini`: `GEMINI.md`.

## Datos e invariantes

- Modelos: `humanio.yaml` con schema versionado y
  `.humanio/integrations.json` con adaptadores y destinos administrados.
- Invariantes: versiones sincronizadas, IDs únicos, referencias definidas,
  marcas completas, escrituras atómicas y ausencia de sobrescritura silenciosa.

## Estados y transiciones

| Actor | Precondición | Evento | Efectos | Auditoría |
|---|---|---|---|---|
| Mantenedor | Árbol validado | Publica PR | CI ejecuta gates | GitHub Actions |
| Usuario | Checkout válido | Instala CLI | Runtime y lanzador preparados | Salida del instalador |
| Usuario | Workspace accesible | Integra adaptador | Bloque y estado actualizados | `integrations.json` |
| Usuario | Integración vigente | Sincroniza | Solo bloques administrados cambian | Hashes y salida CLI |
| Usuario | Integración vigente | Desinstala | Solo contenido administrado se retira | Estado remanente |

## Integraciones, seguridad y observabilidad

- Integraciones: Codex personal marketplace, archivos nativos de agentes y GitHub Actions.
- Permisos: instalación local explícita y escritura limitada al destino.
- Logs y métricas: códigos de salida, hallazgos y resultados de tests.
- Migraciones y rollback: actualización por copia preparada, reemplazo controlado
  y bloques delimitados que pueden retirarse sin afectar contenido ajeno.

# Software Design Document

## Arquitectura

Plugin declarativo con skills y plantillas, acompañado por un CLI determinista en Python.

## Componentes

### SDD-CMP-001

- Responsabilidad: coordinar diagnóstico, inicialización, validación, instalación y empaquetado.
- Cubre: PRD-FR-001, PRD-NFR-001.
- Entradas: manifiesto, perfil, riesgo, templates y workspace.
- Salidas: artefactos, hallazgos, códigos de salida, instalación y ZIP.

## Datos e invariantes

- Modelo: `humanio.yaml` con schema versionado.
- Invariantes: versiones sincronizadas, IDs únicos, referencias definidas y ausencia de sobrescritura silenciosa.

## Estados y transiciones

| Actor | Precondición | Evento | Efectos | Auditoría |
|---|---|---|---|---|
| Mantenedor | Árbol validado | Publica PR | CI ejecuta gates | GitHub Actions |

## Integraciones, seguridad y observabilidad

- Integraciones: Codex personal marketplace y GitHub Actions.
- Permisos: instalación local explícita y escritura limitada al destino.
- Logs y métricas: códigos de salida, hallazgos y resultados de tests.
- Migraciones y rollback: actualización por copia preparada y reemplazo controlado.

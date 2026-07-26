# Registro de riesgos

## Clasificación

- Nivel: R1
- Justificación: herramienta local sin despliegue o transacciones externas automáticas.
- Responsable: mantenedor.

## Riesgos

| ID | Riesgo | Probabilidad | Impacto | Control | Evidencia | Estado |
|---|---|---|---|---|---|---|
| RSK-001 | Declarar readiness usando solo fixtures | media | alto | Workspace gobernado y gate estricto en CI | `EVIDENCE.md` | mitigated |

## Riesgo residual

- Riesgos aceptados: incompatibilidad futura dentro de la serie 1.x.
- Aprobador: propietario del repositorio.
- Condiciones: SemVer, changelog y pruebas de regresión.

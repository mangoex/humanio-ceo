# Matriz de trazabilidad

| Objetivo | Requisito | Diseño | Escenario | Prueba | Implementación | Evidencia | Estado |
|---|---|---|---|---|---|---|---|
| OBJ-001 | PRD-FR-001 | SDD-CMP-001 | BDD-SC-001 | TDD-TC-001, TDD-TC-002, TDD-TC-003 | `scripts/humanio.py`, `scripts/init_project.py` | `EVIDENCE.md` | passed |
| OBJ-001 | PRD-NFR-001 | SDD-CMP-001 | BDD-SC-001 | TDD-TC-004, TDD-TC-005 | `scripts/package_plugin.py`, `scripts/install_plugin.py` | `EVIDENCE.md` | passed |
| OBJ-002 | PRD-FR-002 | SDD-CMP-002 | BDD-SC-002 | TDD-TC-006 | `scripts/install_cli.py`, `scripts/humanio.py` | CI y `EVIDENCE.md` | passed |
| OBJ-003 | PRD-FR-003 | SDD-CMP-003 | BDD-SC-003, BDD-SC-004, BDD-SC-005 | TDD-TC-007, TDD-TC-008, TDD-TC-009 | `scripts/adapters.py`, `scripts/humanio.py` | CI y `EVIDENCE.md` | passed |
| OBJ-003 | PRD-NFR-002 | SDD-CMP-002, SDD-CMP-003 | BDD-SC-002, BDD-SC-003, BDD-SC-004, BDD-SC-005 | TDD-TC-006, TDD-TC-007, TDD-TC-008, TDD-TC-009 | Instalador y adaptadores | CI y `EVIDENCE.md` | passed |

## Huecos

- La licencia de distribución requiere decisión del propietario.

# Test-Driven Development

## TDD-TC-001

- Cubre: BDD-SC-001 y el gate estructural del autopiloto.
- Nivel: integración.
- Fixture: `pilots/humanio-ceo`.
- Acción: ejecutar validación estricta desde CI.
- Aserciones: código cero, cero errores y cero advertencias.
- Estado: passed.

## TDD-TC-002

- Cubre: PRD-FR-001.
- Ejecutable: `FrameworkFlowTests.test_each_profile_initializes_and_passes_normal_validation`.
- Aserción: los perfiles conversacional, software e híbrido se inicializan y validan.
- Estado: passed.

## TDD-TC-003

- Cubre: PRD-FR-001.
- Ejecutable: `FrameworkFlowTests.test_initializer_never_overwrites_existing_files`.
- Aserción: una colisión cancela la inicialización sin alterar archivos.
- Estado: passed.

## TDD-TC-004

- Cubre: PRD-NFR-001.
- Ejecutable: `ReleaseTests.test_package_is_deterministic_and_auditable`.
- Aserción: dos paquetes son idénticos e incluyen los insumos de auditoría.
- Estado: passed.

## TDD-TC-005

- Cubre: PRD-NFR-001.
- Ejecutable: `ReleaseTests.test_local_installer_registers_personal_marketplace`.
- Aserción: instalación y actualización aisladas terminan correctamente.
- Estado: passed.

## TDD-TC-006

- Cubre: PRD-FR-002, PRD-NFR-002, BDD-SC-002.
- Ejecutable: `PortableCliTests.test_isolated_cli_install_update_and_uninstall`.
- Aserciones: el lanzador usa el intérprete validado y ejecuta `doctor`; rechaza
  una reinstalación implícita; no reemplaza temporales ajenos; revierte fallos
  iniciales; y permite actualización y desinstalación explícitas.
- Estado: passed.

## TDD-TC-007

- Cubre: PRD-FR-003, PRD-NFR-002, BDD-SC-003, BDD-SC-004.
- Ejecutable: `AdapterIntegrationTests.test_integrate_sync_and_uninstall_preserve_user_content`.
- Aserciones: los seis adaptadores son idempotentes, conservan contenido ajeno
  byte a byte y permisos POSIX, sincronizan sus bloques y se desinstalan selectivamente.
- Estado: passed.

## TDD-TC-008

- Cubre: PRD-FR-003, PRD-NFR-002, BDD-SC-005.
- Ejecutable: `AdapterIntegrationTests.test_malformed_markers_abort_without_writes`.
- Aserciones: una marca incompleta, estado JSON no-objeto o symlink de destino
  cancela la operación con error controlado y no crea ni modifica destinos ajenos.
- Estado: passed.

## TDD-TC-009

- Cubre: PRD-FR-003, PRD-NFR-002, BDD-SC-003.
- Ejecutable: `AdapterIntegrationTests.test_auto_detection_and_dry_run`.
- Aserciones: `auto` parte de `generic`, añade señales explícitas y `dry-run`
  no modifica el workspace.
- Estado: passed.

## Estrategia

- Unitarias: parsing, selección de archivos e IDs.
- Integración: inicializador, validador, instaladores, adaptadores y empaquetador.
- Contrato: manifiesto y estructura del plugin.
- Seguridad: secretos potenciales y sobrescrituras.
- Regresión: suite completa, evaluación conversacional y autopiloto estricto en cada PR.

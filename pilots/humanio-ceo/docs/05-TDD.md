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

## Estrategia

- Unitarias: parsing, selección de archivos e IDs.
- Integración: inicializador, validador, instalador y empaquetador.
- Contrato: manifiesto y estructura del plugin.
- Seguridad: secretos potenciales y sobrescrituras.
- Regresión: suite completa, evaluación conversacional y autopiloto estricto en cada PR.

# Test-Driven Development

## TDD-TC-001

- Cubre: BDD-SC-001, PRD-FR-001.
- Nivel: integración.
- Fixture: `pilots/humanio-ceo`.
- Acción: ejecutar validación estricta desde CI.
- Aserciones: código cero, cero errores y cero advertencias.
- Estado: passed.

## Estrategia

- Unitarias: parsing, selección de archivos e IDs.
- Integración: inicializador, validador, instalador y empaquetador.
- Contrato: manifiesto y estructura del plugin.
- Seguridad: secretos potenciales y sobrescrituras.
- Regresión: diez pruebas y autopiloto estricto en cada PR.

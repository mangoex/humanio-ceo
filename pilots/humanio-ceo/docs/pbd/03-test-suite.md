# Test Suite conversacional

## PBD-T-001 — Gate de readiness

- Cubre: BS-RULE-001, BS-FLOW-001.
- Precondición: workspace híbrido completo.
- Entrada: solicitud de verificar el release.
- Salida esperada: `READY` solo después de validación estricta y pruebas aprobadas.
- Prohibiciones: usar únicamente los fixtures como evidencia del repositorio evaluado.
- Fuente: `docs/framework/06-DEFINITION-OF-DONE.md`.
- Ejecutable: `tests/test_evaluations.py::ConversationalEvaluationTests.test_pbd_readiness_gate`.
- Casos: `tests/evals/readiness-cases.json`.
- Estado: passed.

## Cobertura

- Falta de manifiesto.
- Placeholders.
- IDs inválidos.
- Pruebas no ejecutadas.
- Instalación incompleta.
- Paquete no reproducible.
- Aprobación obligatoria ausente.
- Condición residual aceptada.

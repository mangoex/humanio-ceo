---
name: traceability-auditor
description: Audita IDs, referencias y cobertura bidireccional entre objetivos, reglas, requisitos, diseño, escenarios, pruebas e implementación; detecta huérfanos, duplicados y enlaces rotos.
---

# Traceability Auditor

Comprobar que cada decisión relevante tiene origen, implementación verificable y evidencia.

## Procedimiento

1. Inventariar los namespaces de IDs aplicables.
2. Detectar IDs duplicados y referencias inexistentes.
3. Comprobar cobertura hacia adelante desde objetivo o regla.
4. Comprobar cobertura hacia atrás desde prueba o implementación.
5. Identificar requisitos, componentes, escenarios y pruebas huérfanos.
6. Separar cobertura declarada de evidencia ejecutada.
7. Proponer correcciones desde el artefacto de mayor autoridad.
8. Ejecutar `python3 scripts/validate_workspace.py --strict` cuando exista un workspace inicializado.

## Reglas

- No crear enlaces ficticios para elevar una métrica.
- No aceptar una tabla de trazabilidad como evidencia de ejecución.
- Mantener IDs estables durante cambios de redacción.
- Registrar explícitamente elementos no aplicables.

## Salida

- Cobertura por tipo de artefacto.
- Huérfanos, duplicados y referencias rotas.
- Evidencia ausente.
- Severidad y artefacto fuente de cada corrección.

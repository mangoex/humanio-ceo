# Evidencia del autopiloto

## Gate estricto

```bash
python3 scripts/humanio.py validate pilots/humanio-ceo --strict
```

Resultado esperado y comprobado: código cero, cero errores y cero advertencias.

## Suite

```bash
python3 -m unittest discover -s tests -v
```

Resultado: catorce pruebas aprobadas.

## Evaluación conversacional

```bash
python3 scripts/evaluate_readiness.py
```

Resultado: `PBD-T-001` aprobado en cinco casos, incluidos gates fallidos, aprobación ausente, condición aceptada y readiness completa.

## Validadores oficiales

Ejecutados el 2026-07-26 sobre los artefactos de la versión `1.0.5`:

```bash
python3 /root/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
for skill in skills/*; do
  python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"
done
```

Resultados, hashes de validadores y hashes de los siete artefactos validados:

`evidence/official-validation.json`

CI ejecuta `scripts/verify_official_evidence.py`; cualquier cambio al manifest o a una skill invalida la aprobación registrada.

## Release

- Plugin y seis skills aprobados por validadores oficiales con evidencia ligada por SHA-256.
- Instalación aislada aprobada por el validador de plugin y `humanio doctor`.
- Empaquetado determinista comprobado por SHA-256.
- CI verifica evidencia oficial, suite, evaluación conversacional y autopiloto estricto en cada pull request.

## Límite

La decisión `READY` cubre uso interno del plugin. La distribución a terceros permanece condicionada a una licencia explícita.

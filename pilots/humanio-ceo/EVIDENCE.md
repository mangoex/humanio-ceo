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

Resultado: once pruebas aprobadas.

## Release

- Plugin y seis skills aprobados por validadores oficiales.
- Instalación aislada aprobada por el validador de plugin y `humanio doctor`.
- Empaquetado determinista comprobado por SHA-256.
- CI ejecuta este gate en cada pull request.

## Límite

La decisión `READY` cubre uso interno del plugin. La distribución a terceros permanece condicionada a una licencia explícita.

# CLI de Humanio CEO

El CLI usa únicamente la biblioteca estándar de Python.

## Diagnóstico de instalación

```bash
python3 scripts/humanio.py doctor
```

## Inicialización

```bash
python3 scripts/humanio.py init \
  --project mi-proyecto \
  --profile hybrid \
  --risk R2 \
  --output ./mi-proyecto
```

Perfiles: `conversational`, `software` e `hybrid`.

Riesgos: `R0`, `R1`, `R2` y `R3`.

El comando inspecciona todas las colisiones antes de escribir y cancela la operación completa si algún archivo de destino ya existe.

## Validación

```bash
python3 scripts/humanio.py validate ./mi-proyecto
python3 scripts/humanio.py validate ./mi-proyecto --strict
python3 scripts/humanio.py validate ./mi-proyecto --strict --json
```

La validación normal permite pendientes explícitos como advertencias durante el descubrimiento. La validación estricta los convierte en errores y debe utilizarse antes de aprobar un incremento.

## Códigos de salida

| Código | Significado |
|---|---|
| 0 | Operación válida |
| 1 | Validación o diagnóstico fallido |
| 2 | Entrada o instalación inválida |
| 3 | Inicialización cancelada por colisiones |
| 4 | Fallo de escritura con limpieza compensatoria |

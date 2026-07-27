# CLI de Humanio CEO

El CLI usa únicamente la biblioteca estándar de Python 3.11 o posterior. Puede
invocarse como `humanio` después de la instalación portable o directamente con
`python3 scripts/humanio.py`.

## Diagnóstico

```bash
humanio doctor
```

Comprueba archivos esenciales y sincronización de versiones.

## Inicialización

Proyecto nuevo:

```bash
humanio init \
  --project mi-proyecto \
  --profile hybrid \
  --risk R2 \
  --output ./mi-proyecto
```

Repositorio existente con `README.md` o `AGENTS.md`:

```bash
humanio init \
  --project mi-proyecto \
  --profile hybrid \
  --risk R2 \
  --output ./mi-proyecto \
  --adopt
```

`--adopt` preserva esos dos archivos. Cualquier otra colisión sigue cancelando la
operación completa. Perfiles: `conversational`, `software` e `hybrid`. Riesgos:
`R0`, `R1`, `R2` y `R3`.

## Detección

```bash
humanio detect .
humanio detect . --json
```

La detección siempre incluye `generic` y solo añade herramientas con señales
explícitas en el repositorio. No inspecciona ni instala extensiones del IDE.

## Integración de agentes

```bash
humanio install . --adapter auto
humanio install . --adapter codex --adapter claude
humanio install . --adapter all
```

`integrate` es alias de `install`. Adaptadores:

- `generic`
- `codex`
- `cursor`
- `claude`
- `copilot`
- `gemini`

El proyecto debe contener `humanio.yaml`. La operación hace preflight sobre todos
los destinos antes de escribir. `--dry-run` muestra el plan sin modificar archivos.

## Estado y sincronización

```bash
humanio status .
humanio status . --json
humanio sync .
humanio sync . --dry-run
```

`status` termina con código 1 cuando detecta deriva. `sync` regenera exclusivamente
los bloques delimitados administrados por Humanio y conserva el resto del archivo.

## Desinstalación del proyecto

```bash
humanio uninstall . --adapter claude
humanio uninstall .
```

Sin `--adapter`, elimina todas las integraciones del proyecto. No desinstala el
CLI global ni borra `humanio.yaml` o la documentación gobernada.

## Validación

```bash
humanio validate ./mi-proyecto
humanio validate ./mi-proyecto --strict
humanio validate ./mi-proyecto --strict --json
```

La validación normal permite pendientes explícitos como advertencias durante el
descubrimiento. La estricta los convierte en errores.

## Códigos de salida

| Código | Significado |
|---|---|
| 0 | Operación válida |
| 1 | Validación, diagnóstico o integración fallida |
| 2 | Entrada o instalación inválida |
| 3 | Inicialización cancelada por colisiones |
| 4 | Fallo de escritura con limpieza compensatoria |

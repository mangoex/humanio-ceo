# Instalación

Humanio ofrece dos canales complementarios:

1. CLI portable para cualquier IDE con terminal.
2. Plugin de Codex para cargar las skills de forma nativa.

## Requisitos

- Python 3.11 o posterior.
- Windows, macOS o Linux.
- Repositorio descargado o clonado.

## CLI portable

Desde la raíz del repositorio:

```bash
python3 scripts/humanio.py doctor
python3 scripts/install_cli.py
```

En Windows puede utilizarse:

```powershell
py scripts\install_cli.py
```

Destinos predeterminados:

| Sistema | Runtime | Lanzador |
|---|---|---|
| macOS y Linux | `~/.local/share/humanio-ceo` | `~/.local/bin/humanio` |
| Windows | `%LOCALAPPDATA%\Humanio\humanio-ceo` | `%LOCALAPPDATA%\Humanio\bin\humanio.cmd` |

El instalador informa cuando el directorio de binarios no pertenece a `PATH`.
También pueden usarse rutas aisladas:

```bash
python3 scripts/install_cli.py \
  --install-root /ruta/runtime \
  --bin-dir /ruta/bin
```

### Actualización

```bash
python3 scripts/install_cli.py --update
humanio doctor
```

La actualización prepara la copia completa antes de sustituir la versión vigente.
Rechaza lanzadores ajenos y respaldos pendientes.

### Simulación y desinstalación

```bash
python3 scripts/install_cli.py --dry-run
python3 scripts/install_cli.py --uninstall --dry-run
python3 scripts/install_cli.py --uninstall
```

La desinstalación global exige que el lanzador contenga la identidad Humanio. Las
integraciones dentro de cada proyecto se retiran por separado con
`humanio uninstall`.

## Plugin de Codex

```bash
python3 scripts/install_plugin.py
codex plugin add humanio-ceo@personal
```

El instalador:

1. Copia únicamente archivos incluidos en el paquete canónico.
2. Usa por defecto `~/.agents/plugins/plugins/humanio-ceo`.
3. Actualiza atómicamente `~/.agents/plugins/marketplace.json`.
4. Se detiene ante una instalación existente sin `--update`.
5. Se detiene si `humanio-ceo` apunta a otra fuente.

Después de activarlo, abrir un hilo nuevo para que Codex cargue las skills.

Actualización:

```bash
python3 scripts/install_plugin.py --update
codex plugin add humanio-ceo@personal
```

## Verificación final

```bash
humanio doctor
humanio detect .
codex plugin list
```

La instalación del CLI permite ejecutar el framework desde cualquier terminal.
La carga automática de contexto por un agente exige su adaptador correspondiente.

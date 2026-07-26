# Instalación del plugin

## Requisitos

- Python 3.11 o posterior.
- Codex con soporte de plugins.
- Repositorio descargado o clonado.

## Marketplace personal

Desde la raíz del repositorio:

```bash
python3 scripts/humanio.py doctor
python3 scripts/install_plugin.py
codex plugin add humanio-ceo@personal
```

El instalador:

1. Copia solo los archivos necesarios del plugin.
2. Usa por defecto `~/.agents/plugins/plugins/humanio-ceo`.
3. Crea o actualiza de forma atómica `~/.agents/plugins/marketplace.json`.
4. Se detiene si existe otra instalación y no se indicó `--update`.
5. Se detiene si el nombre `humanio-ceo` apunta a otra fuente.

Después de activarlo, abrir un hilo nuevo para que Codex cargue las skills.

## Actualización

Actualizar primero el repositorio fuente y después ejecutar:

```bash
python3 scripts/install_plugin.py --update
codex plugin add humanio-ceo@personal
```

`--update` prepara una copia completa antes de reemplazar la instalación anterior.

## Marketplace aislado

Para probar sin tocar el marketplace personal:

```bash
python3 scripts/install_plugin.py --marketplace-root /ruta/de/prueba
```

Ese marketplace no es descubierto automáticamente. Debe configurarse explícitamente antes de activar el plugin.

## Verificación

```bash
codex plugin list
python3 ~/.agents/plugins/plugins/humanio-ceo/scripts/humanio.py doctor
```

Si Codex conserva una versión anterior, confirmar qué marketplace está sirviendo el plugin, reinstalarlo desde ese marketplace y abrir un hilo nuevo.

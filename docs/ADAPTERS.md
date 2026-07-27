# Adaptadores de IDE y agentes

## Principio

Los documentos Humanio siguen siendo la fuente canónica. Los adaptadores solo
insertan instrucciones breves para que cada agente encuentre y respete esa fuente.
No instalan extensiones, cuentas ni herramientas de terceros.

## Compatibilidad

| Adaptador | Señal para `auto` | Destino administrado |
|---|---|---|
| `generic` | Siempre | `.humanio/README.md` |
| `codex` | `.codex/` | `AGENTS.md` |
| `cursor` | `.cursor/` | `AGENTS.md` |
| `claude` | `.claude/` o `CLAUDE.md` | `CLAUDE.md` |
| `copilot` | Archivo de instrucciones o `.github/instructions/` | `.github/copilot-instructions.md` |
| `gemini` | `.gemini/` o `GEMINI.md` | `GEMINI.md` |

Codex y Cursor comparten un único bloque en `AGENTS.md` cuando ambos están activos.
El estado conserva los dos adaptadores y una desinstalación selectiva actualiza el
bloque sin retirarlo mientras el otro siga instalado.

## Bloques administrados

Humanio usa estas marcas:

```markdown
<!-- humanio-ceo:managed:start -->
...
<!-- humanio-ceo:managed:end -->
```

Contenido antes y después de las marcas pertenece al proyecto y se conserva. Una
marca faltante, duplicada o desordenada se considera corrupción y cancela toda la
operación antes de escribir.

## Estado local

`.humanio/integrations.json` registra:

- versión del esquema;
- versión del framework;
- adaptadores activos;
- destinos y hash esperado de cada bloque.

Puede versionarse para compartir la misma integración con el equipo. No contiene
credenciales, rutas personales ni datos sensibles.

## Flujo recomendado

```bash
humanio detect .
humanio install . --adapter auto --dry-run
humanio install . --adapter auto
humanio status .
humanio validate . --strict
```

Use selección explícita cuando el repositorio no contiene una señal:

```bash
humanio install . --adapter codex
```

## Límites

- `auto` detecta convenciones del repositorio, no extensiones activas del IDE.
- El adaptador genérico garantiza uso por terminal, no carga automática por un agente.
- Las convenciones de proveedores pueden cambiar; la matriz de CI verifica el
  comportamiento de Humanio, mientras la compatibilidad externa debe revisarse en
  cada release menor.

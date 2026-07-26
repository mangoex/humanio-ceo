# Humanio CEO Engineering Framework

Plugin y marco metodológico de Humanio para diagnosticar, especificar, desarrollar, validar y gobernar agentes y software con inteligencia artificial.

**CEO** significa:

- **Contexto:** qué debe comprender la solución y qué fuentes gobiernan sus decisiones.
- **Ecosistema:** dónde opera y con qué personas, canales, datos y sistemas se conecta.
- **Orquestación:** cómo se coordinan agentes, humanos, herramientas, estados, reglas y métricas.

## Estado

Versión `1.0.0`: marco estable, instalable, verificable y reutilizable.

El plugin incorpora:

- Constitución.
- Arquitectura.
- Modelo de autoridad.
- Perfiles conversacional, software e híbrido.
- Niveles de riesgo.
- Quality gates.
- Plantillas comunes.
- Skill coordinadora y cinco skills especializadas.
- Inicializador de proyectos.
- Validador de estructura, placeholders, riesgo, secretos y trazabilidad.
- Pruebas automatizadas para los tres perfiles.
- Comando unificado `humanio`.
- Detección de IDs duplicados o indefinidos.
- Fixtures estrictos versionados.
- Validación automática en pull requests.
- Empaquetado reproducible.
- Instalador seguro para marketplace personal de Codex.
- Guías de adopción, operación y releases.

## Principio central

Una solución con IA está lista cuando produce un resultado útil, repetible, medible, trazable y gobernable dentro de un ecosistema real.

## Uso conceptual

1. Recibir una idea, requisito, prompt o repositorio.
2. Elegir modo, perfil y riesgo.
3. Inventariar fuentes y decisiones.
4. Crear o auditar la línea base.
5. Mantener trazabilidad.
6. Ejecutar quality gates.
7. Entregar evidencia y siguiente incremento.

## Modos

- `intake`
- `audit`
- `bootstrap`
- `update`
- `verify`
- `compile`

## Inicializar un proyecto

```bash
python3 scripts/humanio.py init \
  --profile hybrid \
  --risk R2 \
  --project "Mi proyecto" \
  --output /ruta/al/proyecto
```

El inicializador inspecciona todos los destinos antes de escribir y se detiene si alguno ya existe.

## Validar un proyecto

```bash
python3 scripts/humanio.py validate /ruta/al/proyecto
python3 scripts/humanio.py validate /ruta/al/proyecto --strict
```

La validación normal permite una línea base con pendientes visibles. La validación estricta falla mientras existan `POR CONFIRMAR`, huecos de cobertura o errores.

La referencia completa del comando está en [docs/CLI.md](./docs/CLI.md).

## Instalar como plugin de Codex

```bash
python3 scripts/install_plugin.py
codex plugin add humanio-ceo@personal
```

La instalación se copia al marketplace personal sin modificar este repositorio. Para actualizar una instalación existente:

```bash
python3 scripts/install_plugin.py --update
codex plugin add humanio-ceo@personal
```

Abrir un hilo nuevo después de instalar o actualizar. Consultar [la guía de instalación](./docs/INSTALLATION.md) para rutas personalizadas y diagnóstico.

## Adoptar en un proyecto

- Proyecto nuevo: inicializar directamente con el perfil y riesgo aplicables.
- Repositorio existente: auditar primero, generar una línea base en un directorio temporal y reconciliar decisiones antes de copiar artefactos.

La estrategia completa está en [docs/ADOPTION.md](./docs/ADOPTION.md).

## Pruebas del framework

```bash
python3 -m unittest discover -s tests -v
```

## Documentación existente

La metodología consultiva original se conserva en:

- [CEO Framework para Agentes de IA](./docs/ceo-framework/README.md)
- [Narrativa comercial](./docs/comercial/00_NARRATIVA_COMERCIAL.md)
- [Presentación para cliente](./docs/comercial/01_PRESENTACION_CLIENTE.md)
- [Guía de sesión de diagnóstico](./docs/comercial/02_GUIA_SESION_DIAGNOSTICO.md)

## Gobierno

La fuente principal del nuevo marco es [la Constitución](./docs/framework/00-CONSTITUTION.md).

## Alcance de la estabilidad 1.0

La versión 1.0 estabiliza estructura, perfiles, namespaces de IDs, CLI y contrato del manifiesto. No certifica por sí sola un proyecto real: cada adopción debe completar sus artefactos, pruebas y gates.

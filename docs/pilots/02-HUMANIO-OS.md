# Piloto 2: Humanio OS

## Alcance

Auditoría de adopción sin modificar `mangoex/humanio-os`.

- Commit observado: `7174df5122988d4acfc2b86b9770c254482aa206`.
- Perfil recomendado: híbrido.
- Riesgo recomendado: R2.
- Motivo: combina conocimiento, prompts, agentes e información operativa de varios proyectos en un repositorio público.

## Evidencia observada

- 378 archivos versionados.
- 254 archivos Markdown.
- Tres vaults conectados mediante índices y wikilinks.
- Fuentes `raw/` declaradas inmutables.
- Wiki generada con reglas de frontmatter, idioma, enlaces y lint.
- Registro de decisiones y bitácoras.
- Documentación de agentes, skills, integraciones, operación y mercado.
- Ocho archivos superan 5 MB.
- Dieciséis archivos contienen direcciones de correo.
- Diez archivos contienen marcadores textuales relacionados con claves, tokens, contraseñas o secretos. Este conteo no demuestra que existan credenciales válidas.
- No se encontraron en raíz `humanio.yaml`, `AGENTS.md`, `SECURITY.md`, `CONTRIBUTING.md` ni workflow de validación Humanio.

## Fortalezas

- La separación entre fuentes inmutables y conocimiento derivado ya implementa un modelo de autoridad útil.
- Los índices, wikilinks y logs ofrecen trazabilidad documental.
- Las convenciones explícitas reducen duplicación y pérdida de contexto.
- El registro de decisiones es una base adecuada para gobierno incremental.

## Brechas

- El validador Humanio termina con `MANIFEST_MISSING`.
- No existe clasificación formal de perfil, riesgo o estado.
- Las reglas viven en varios archivos `CLAUDE.md` y `AGENTS.md` anidados sin una Constitución raíz común.
- No hay gate automatizado para secretos, datos personales, enlaces rotos o calidad del vault.
- La exposición pública de información personal y operativa necesita revisión deliberada.
- Archivos grandes y recursos binarios elevan costo de clonación y dificultan auditoría.
- No existe matriz que conecte decisiones, agentes, prompts, integraciones, pruebas y evidencia.

## Decisión

`NOT READY` para considerarse gobernado por Humanio CEO 1.0.

Esto no implica que el vault sea inútil. Su arquitectura de conocimiento es valiosa, pero la gobernanza está distribuida y carece de gates verificables.

## Incremento recomendado

1. Crear una rama de adopción.
2. Clasificar qué contenido debe seguir público.
3. Ejecutar revisión de secretos y datos personales sin imprimir valores.
4. Añadir `humanio.yaml`, `AGENTS.md` raíz y política de seguridad.
5. Definir Constitución y autoridad entre memoria, `raw/`, wiki y decisiones.
6. Introducir IDs para decisiones, agentes, flujos y controles críticos.
7. Añadir CI para lint, enlaces, archivos grandes y exposición accidental.
8. Migrar un solo flujo, preferentemente Prenomina Agent, como incremento vertical.

## Madurez

Nivel 2, trazable de forma documental. Para alcanzar nivel 3 necesita validación automatizada y evidencia ejecutada.

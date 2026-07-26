# Changelog

Todos los cambios relevantes del framework se documentan aquí.

## [0.3.0] - 2026-07-26

### Added

- CLI unificado para diagnóstico, inicialización y validación.
- Esquema JSON del manifiesto de proyecto.
- Detección de tokens sin renderizar, IDs duplicados e IDs indefinidos.
- Definición formal de terminado.
- Fixtures estrictos versionados para los tres perfiles.
- Workflow de GitHub Actions sin dependencias externas.

### Changed

- Los objetivos conversacionales usan namespace `PBD-OBJ`.
- La Constitución conversacional separa principios y reglas de comportamiento.
- Versión del plugin actualizada a `0.3.0`.

## [0.2.0] - 2026-07-26

### Added

- Inicializador determinista para perfiles conversacional, software e híbrido.
- Validador de estructura, perfil, riesgo, placeholders, secretos y trazabilidad.
- Plantillas completas para los tres perfiles.
- Skills especializadas para descubrimiento, PBD, software, trazabilidad y producción.
- Pruebas automatizadas que generan fixtures temporales de los tres perfiles.

### Changed

- La skill coordinadora ahora enruta hacia capacidades especializadas y scripts.
- Los perfiles incluyen manifiesto, riesgos, cambios y trazabilidad canónica.
- Versión del plugin actualizada a `0.2.0`.

## [0.1.0] - 2026-07-26

### Added

- Manifest inicial del plugin `humanio-ceo`.
- Constitución del framework.
- Arquitectura, autoridad, perfiles, riesgo y quality gates.
- Plantillas base de intake, trazabilidad y riesgos.
- Skill coordinadora inicial `humanio-project-engineer`.

### Notes

Esta versión establece el gobierno y la estructura. La automatización determinista, las skills especializadas y los fixtures se desarrollarán en incrementos posteriores.

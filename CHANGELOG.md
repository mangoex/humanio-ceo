# Changelog

Todos los cambios relevantes del framework se documentan aquí.

## [1.0.2] - 2026-07-26

### Fixed

- El autopiloto usa ahora un workspace híbrido gobernado que pasa validación estricta.
- La evidencia registra el conteo real del paquete construido desde el repositorio completo.
- El README muestra la misma versión que el manifest, la plantilla y `VERSION`.

### Added

- Gate de CI y prueba de regresión para el workspace de autopiloto.

## [1.0.1] - 2026-07-26

### Added

- Evidencia del piloto de release sobre `humanio-ceo`.
- Auditoría de adopción, sin modificaciones, sobre `humanio-os`.
- Registro explícito de límites y decisiones pendientes de distribución.

### Changed

- Se completa la evidencia constitucional de aplicación en dos proyectos reales.

## [1.0.0] - 2026-07-26

### Added

- Versión canónica en `VERSION` y verificación de consistencia.
- Empaquetado ZIP determinista y mínimo.
- Instalador local seguro para marketplace personal de Codex.
- Pruebas de empaquetado, instalación y actualización.
- Guías de instalación, adopción, operación, madurez y releases.
- Políticas de contribución y seguridad.

### Changed

- El framework alcanza estabilidad 1.0 para estructura, CLI, perfiles y manifiesto.
- Versión del plugin y nuevas líneas base actualizadas a `1.0.0`.

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

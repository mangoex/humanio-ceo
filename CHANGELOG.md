# Changelog

Todos los cambios relevantes del framework se documentan aquí.

## [1.0.6] - 2026-07-26

### Fixed

- Un contrato canónico versiona el inventario de skills, sus dependencias documentales y los escenarios obligatorios de readiness.
- La evidencia oficial cubre todos los archivos distribuidos de cada skill y sus dependencias; metadata oculta no canónica tampoco se empaqueta.
- El gate `PBD-T-001` rechaza conjuntos de casos vacíos, incompletos, duplicados o con valores, campos o tipos alterados.
- La evidencia de release declara y prueba que los fixtures versionados se distribuyen intencionalmente.

### Added

- Pruebas negativas para skills faltantes o sin validar, metadata oculta y suites de readiness incompletas, alteradas o con tipos incorrectos.

## [1.0.5] - 2026-07-26

### Fixed

- La Constitución ocupa por sí sola el nivel superior de autoridad.
- Toda sustitución o revocación de ADR exige registrar el cambio de estado y la decisión sucesora.
- `software-specification` detecta conflictos de ADR y delega su transición a `pbd-governance`.
- La prueba de regresión verifica jerarquía, transición explícita y separación de responsabilidades.

## [1.0.4] - 2026-07-26

### Fixed

- La aprobación de validadores oficiales queda ligada por SHA-256 a los artefactos evaluados y verificada por CI.
- Requisitos funcionales y no funcionales apuntan a pruebas ejecutables específicas.
- `PBD-T-001` cuenta con una evaluación determinista de cinco casos.
- El paquete incluye el workspace, la evidencia y los insumos necesarios para auditar el release.

### Added

- Verificador de evidencia oficial.
- Evaluador determinista de readiness.
- Casos de evaluación y pruebas de regresión asociadas.

## [1.0.3] - 2026-07-26

### Fixed

- Los ADR vigentes se ubican por encima del PRD y del diseño derivado en toda la jerarquía.
- La propagación exige reemplazar o revocar explícitamente un ADR incompatible antes de actualizar especificaciones subordinadas.
- Plantillas, autopiloto, fixtures y skill de especificación aplican el mismo orden canónico.

### Added

- Prueba de regresión para la consistencia del orden de autoridad.

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

# Piloto 1: Humanio CEO

## Alcance

Aplicar el marco a su propio desarrollo, empaquetado e instalación como plugin.

- Repositorio: `mangoex/humanio-ceo`.
- Versión evaluada: `1.0.4`.
- Perfil: híbrido, porque combina herramientas deterministas y skills de agentes.
- Riesgo: R1, porque el plugin produce artefactos y cambios locales pero no despliega ni ejecuta transacciones externas por sí mismo.

## Evidencia

- Constitución, autoridad, riesgo, gates y definición de terminado versionados.
- Seis skills aprobadas por el validador oficial.
- Plugin aprobado por el validador oficial.
- Catorce pruebas automatizadas aprobadas.
- Tres fixtures aprobados en modo estricto con cero errores y cero advertencias.
- Workflow de GitHub Actions aprobado en los PR de fases 3 y 4.
- Paquete ZIP auditable validado sin errores desde el repositorio completo.
- Dos empaquetados del mismo estado produjeron los mismos bytes.
- Instalación aislada aprobó validación de plugin y `humanio doctor`.
- Inicializador comprobado para los tres perfiles.
- Protección contra sobrescritura comprobada.
- `pilots/humanio-ceo` aprobó validación estricta con cero errores y cero advertencias.
- La evaluación ejecutable `PBD-T-001` impide emitir `READY` con gates o aprobaciones fallidas.
- La evidencia oficial está ligada por hashes al manifest y a las seis skills.
- El paquete incluye workspace, evidencia, pruebas, casos de evaluación y workflow.

## Hallazgos

- La estructura y el CLI alcanzan estabilidad 1.x.
- CI hace verificable el gate técnico en cada pull request.
- El empaquetado excluye fixtures y metadatos de desarrollo.
- El repositorio no contiene una licencia.

## Decisión

- `READY` para uso interno y para proyectos autorizados por el propietario, sustentado por el workspace gobernado `pilots/humanio-ceo`.
- `CONDITIONAL` para distribución a terceros: requiere una decisión explícita de licencia.

## Madurez

Nivel 4, operable. Existe gobierno, validación, CI, instalación, actualización, empaquetado y evidencia. La retroalimentación de adopciones futuras permitirá avanzar hacia nivel 5.

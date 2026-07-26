# Modelo de riesgo y rigor adaptativo

## Propósito

Aplicar suficiente control sin convertir el framework en burocracia.

## Niveles

### R0 — Exploratorio

Ejemplos: documento, prompt experimental, prototipo sin datos reales.

Mínimos:

- Contexto.
- Alcance.
- Resultado esperado.
- Prueba mínima.

### R1 — Operativo interno

Ejemplos: automatización reversible o bot interno de bajo impacto.

Mínimos:

- Constitución o reglas.
- Especificación.
- Casos normales y fallos.
- Fuente canónica.
- Trazabilidad básica.

### R2 — Producción estándar

Ejemplos: SaaS, API, agente de atención o integración usada por clientes.

Mínimos:

- Línea base completa según perfil.
- Seguridad y permisos.
- Observabilidad.
- BDD/TDD o evaluaciones.
- Evidencia.
- Rollback y responsable.

### R3 — Crítico

Ejemplos: nómina, pagos, salud, legal, datos sensibles o acciones irreversibles.

Mínimos adicionales:

- Threat model.
- Aprobación humana definida.
- Auditoría reforzada.
- Pruebas de seguridad y regresión crítica.
- Simulación de fallos.
- Reversión probada.
- Riesgo residual aceptado explícitamente.

## Factores de clasificación

- Impacto económico.
- Sensibilidad de datos.
- Irreversibilidad.
- Alcance de usuarios.
- Dependencia de terceros.
- Exposición externa.
- Impacto legal o regulatorio.
- Capacidad de detección y reversión.

Si un solo factor es crítico, el proyecto no se clasifica por simple promedio.

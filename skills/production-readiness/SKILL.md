---
name: production-readiness
description: Evalúa preparación para producción con gates proporcionales al riesgo, evidencia de pruebas, seguridad, privacidad, observabilidad, rollback, operación y aprobaciones.
---

# Production Readiness

Emitir una recomendación verificable de salida, salida condicionada o bloqueo.

## Procedimiento

1. Confirmar perfil, riesgo y alcance de la liberación.
2. Leer `../../docs/framework/04-QUALITY-GATES.md`.
3. Ejecutar el validador estricto y las pruebas disponibles.
4. Revisar seguridad, privacidad, permisos y secretos.
5. Revisar observabilidad, alertas, soporte y responsables.
6. Verificar migración, reversión, recuperación e idempotencia aplicables.
7. Comprobar aprobaciones humanas requeridas.
8. Registrar evidencia con fecha, comando, resultado y responsable.

## Decisión

- `READY`: todos los gates obligatorios tienen evidencia válida.
- `CONDITIONAL`: solo quedan condiciones explícitas aceptadas por la autoridad correspondiente.
- `NOT READY`: existe un gate obligatorio fallido, sin evidencia o sin aprobación.

## Reglas

- No interpretar ausencia de fallos como prueba aprobada.
- No ocultar resultados parciales o no ejecutados.
- No aprobar una acción sensible sin control definido.
- Elevar el rigor cuando cambie el nivel de riesgo.

## Salida

- Decisión y alcance.
- Gates evaluados.
- Evidencia ejecutada.
- Bloqueos, condiciones y riesgos residuales.
- Aprobaciones y plan de reversión.

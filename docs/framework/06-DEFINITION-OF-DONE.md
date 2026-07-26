# Definición de terminado

Un proyecto gobernado por Humanio CEO está terminado para un incremento cuando satisface simultáneamente estas condiciones.

## Artefactos

- Perfil y riesgo constan en `humanio.yaml`.
- Constitución, alcance y fuentes canónicas están aprobados.
- Los artefactos obligatorios del perfil existen y no contienen placeholders.
- Cada ID tiene una sola definición y todas sus referencias son válidas.

## Trazabilidad

- Cada objetivo está conectado con comportamiento o requisito.
- Cada comportamiento crítico tiene diseño, escenario y prueba aplicables.
- La implementación y la evidencia están registradas cuando existen.
- Los huecos aceptados tienen responsable, fecha y autoridad.

## Calidad

- La validación estricta termina con código cero.
- Las pruebas aplicables fueron ejecutadas, no solo descritas.
- Los gates proporcionales al riesgo cuentan con evidencia.
- No existen secretos incrustados ni riesgos críticos sin tratamiento.

## Operación

- Hay responsables de soporte, observabilidad y escalamiento.
- Existe reversión o recuperación para cambios con impacto operativo.
- Las decisiones y cambios quedan registrados.

## Decisión

La salida solo puede declararse `READY`, `CONDITIONAL` o `NOT READY` según la skill `production-readiness`. Una condición aceptada no equivale a una prueba aprobada.

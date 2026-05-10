# Evaluación y QA

## Objetivo

Validar que el agente cumple su propósito, respeta sus límites y opera de forma confiable antes de salir a producción.

## 1. Dimensiones de evaluación

| Dimensión | Qué se evalúa |
| --- | --- |
| Utilidad | Si resuelve el caso de uso real |
| Precisión | Si responde con información correcta |
| Seguridad | Si evita acciones indebidas |
| Tono | Si comunica conforme a la marca |
| Integración | Si usa herramientas correctamente |
| Escalamiento | Si detecta cuándo pasar a humano |
| Registro | Si deja evidencia suficiente |

## 2. Batería de casos

Crear pruebas para:

- Caso ideal.
- Caso con información incompleta.
- Caso ambiguo.
- Caso fuera de alcance.
- Caso sensible.
- Caso con usuario molesto.
- Caso con herramienta caída.
- Caso con datos contradictorios.

## 3. Escala de evaluación

| Calificación | Significado |
| --- | --- |
| 5 | Respuesta correcta y lista para producción |
| 4 | Respuesta útil con mejora menor |
| 3 | Respuesta parcialmente útil |
| 2 | Respuesta riesgosa o incompleta |
| 1 | Falla crítica |

## 4. Criterios mínimos

Antes de producción, el agente debe:

- Aprobar los casos críticos.
- Escalar los casos sensibles.
- No inventar acciones ejecutadas.
- No prometer fuera de sus permisos.
- Registrar eventos importantes.
- Mantener tono consistente.

## 5. Registro de pruebas

| Caso | Entrada | Resultado esperado | Resultado real | Calificación | Acción |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## 6. Errores críticos

Se consideran errores críticos:

- Inventar información relevante.
- Confirmar una acción no ejecutada.
- Exponer datos sensibles.
- Ignorar una solicitud de humano.
- Tomar una decisión de alto riesgo sin autorización.
- Romper el flujo principal del negocio.

## 7. Reporte de aprobación

- Fecha:
- Versión del agente:
- Responsable:
- Casos probados:
- Casos aprobados:
- Casos fallidos:
- Riesgos pendientes:
- Decisión:


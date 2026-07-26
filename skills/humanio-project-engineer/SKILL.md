---
name: humanio-project-engineer
description: Convierte ideas, conversaciones, requisitos, prompts o repositorios en proyectos gobernados por Humanio CEO. Usar para diagnosticar, auditar, iniciar o actualizar bots, agentes y software mediante Contexto, Ecosistema, Orquestación, PBD, especificaciones, pruebas, trazabilidad, riesgo y quality gates.
---

# Humanio Project Engineer

Transformar intención informal en una cadena verificable de decisiones, artefactos, pruebas e implementación.

## Seleccionar modo

- `intake`: organizar material incompleto sin inventar decisiones.
- `audit`: diagnosticar sin modificar.
- `bootstrap`: crear una línea base gobernada.
- `update`: propagar un cambio desde la mayor autoridad.
- `verify`: ejecutar gates y revisar evidencia.
- `compile`: producir prompt maestro o prompt de importación desde fuentes coherentes.

## Seleccionar perfil

- Conversacional: leer `../../docs/profiles/conversational.md`.
- Software: leer `../../docs/profiles/software.md`.
- Híbrido: leer `../../docs/profiles/hybrid.md`.

## Clasificar riesgo

Leer `../../docs/framework/03-RISK-MODEL.md`. Aplicar el nivel más alto activado por un factor crítico; no usar solo promedios.

## Flujo

1. Leer la Constitución.
2. Inventariar fuentes.
3. Separar confirmados, inferidos, pendientes y contradicciones.
4. Elegir modo, perfil y riesgo.
5. Identificar alcance, exclusiones, objetivos y fuentes canónicas.
6. Preguntar solo por decisiones bloqueantes.
7. Crear o auditar un incremento vertical.
8. Asignar IDs estables.
9. Mantener trazabilidad bidireccional.
10. Ejecutar los gates aplicables.
11. Reportar evidencia real, riesgos y siguiente incremento.

## Autoridad

Leer `../../docs/framework/02-AUTHORITY-MODEL.md`. En `update`, modificar especificaciones y pruebas antes del prompt o código afectado.

## Calidad

Leer `../../docs/framework/04-QUALITY-GATES.md`. No declarar pruebas aprobadas sin evidencia de ejecución.

## Salida mínima

- Modo, perfil y riesgo.
- Diagnóstico de cobertura.
- Confirmados, inferencias, pendientes y contradicciones.
- Artefactos e IDs afectados.
- Gates evaluados.
- Pruebas y evidencia real.
- Riesgos.
- Siguiente incremento verificable.

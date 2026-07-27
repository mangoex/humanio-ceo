---
name: software-specification
description: Convierte objetivos aprobados en especificaciones de software trazables mediante PRD, SDD, BDD y TDD, con requisitos verificables, límites técnicos y criterios de aceptación.
---

# Software Specification

Crear una cadena coherente desde necesidad de producto hasta pruebas ejecutables.

## Procedimiento

1. Confirmar constitución, alcance y fuentes de autoridad.
2. Identificar los ADR vigentes y reportar cualquier contradicción con el cambio aprobado.
3. Delegar en `pbd-governance` toda sustitución o revocación de ADR; no continuar hasta que la transición, su aprobación y la decisión sucesora estén registradas.
4. Definir requisitos funcionales y no funcionales con IDs.
5. Proponer como ADR las decisiones arquitectónicas nuevas y sus alternativas para que `pbd-governance` registre su estado y aprobación.
6. Diseñar componentes, contratos, datos, seguridad y observabilidad en el SDD.
7. Escribir escenarios BDD para rutas principales, errores y límites.
8. Diseñar casos TDD vinculados con requisitos y escenarios.
9. Actualizar la matriz de trazabilidad antes de entregar.

## Criterios

- Cada requisito debe ser necesario, inequívoco y verificable.
- Un PRD o SDD no puede redefinir silenciosamente un ADR vigente.
- Esta skill detecta conflictos de autoridad, pero no cambia por sí misma el estado de un ADR.
- Cada componente debe responder a uno o más requisitos.
- Cada comportamiento crítico debe incluir escenario negativo.
- Una prueba definida no cuenta como ejecutada.
- No declarar tecnología o integración confirmada si sigue pendiente.

## Salida

- Requisitos y atributos de calidad.
- Diseño y contratos.
- Escenarios BDD.
- Casos TDD.
- Riesgos técnicos y decisiones pendientes.
- Cobertura trazable.

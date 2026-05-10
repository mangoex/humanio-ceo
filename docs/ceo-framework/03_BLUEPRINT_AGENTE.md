# Blueprint del Agente

## Objetivo

Definir con precisión qué hará el agente, cómo debe comportarse, qué herramientas usará, qué límites tendrá y cómo se evaluará.

## 1. Identidad del agente

- Nombre:
- Rol:
- Propósito:
- Usuario principal:
- Canal principal:
- Responsable humano:

## 2. Resultado de negocio

- Resultado esperado:
- Indicador principal:
- Indicadores secundarios:
- Frecuencia de medición:

## 3. Capacidades

El agente puede:

- 
- 
- 

El agente no puede:

- 
- 
- 

## 4. Contexto necesario

- Información de empresa:
- Productos o servicios:
- Políticas:
- Preguntas frecuentes:
- Casos especiales:
- Ejemplos de buenas respuestas:
- Ejemplos de malas respuestas:

## 5. Tono y comportamiento

- Tono:
- Nivel de formalidad:
- Nivel de iniciativa:
- Qué debe preguntar antes de actuar:
- Qué debe evitar:
- Cómo debe reconocer incertidumbre:

## 6. Herramientas

| Herramienta | Uso | Permisos | Riesgo |
| --- | --- | --- | --- |
| CRM | Consultar o registrar prospectos | Lectura/escritura limitada | Datos incorrectos |
| Calendario | Consultar disponibilidad | Lectura | Disponibilidad desactualizada |
| Base de conocimiento | Responder preguntas | Lectura | Información incompleta |

## 7. Flujo básico

1. Recibe solicitud.
2. Identifica intención.
3. Consulta contexto disponible.
4. Decide si puede responder o debe preguntar.
5. Ejecuta acción permitida.
6. Registra evento.
7. Escala si encuentra excepción.

## 8. Reglas de escalamiento

Escalar a humano cuando:

- Hay duda legal, médica, financiera o contractual.
- El usuario está molesto.
- El agente no tiene información suficiente.
- La acción puede afectar dinero, reputación o datos sensibles.
- El usuario solicita una persona.

## 9. Criterios de aceptación

El agente se considera aprobado si:

- Resuelve al menos el porcentaje definido de casos objetivo.
- No inventa información crítica.
- Escala correctamente los casos sensibles.
- Usa el tono acordado.
- Registra las acciones importantes.
- Funciona en el canal previsto.

## 10. Casos de prueba

| Caso | Entrada | Resultado esperado | Estado |
| --- | --- | --- | --- |
| Caso normal |  |  | Pendiente |
| Caso incompleto |  |  | Pendiente |
| Caso sensible |  |  | Pendiente |
| Caso fuera de alcance |  |  | Pendiente |


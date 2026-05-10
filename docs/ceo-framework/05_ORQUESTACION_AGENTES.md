# Orquestación de Agentes

## Objetivo

Definir cómo se coordinan agentes, humanos, herramientas y estados para que el sistema produzca resultados confiables.

## 1. Modelo de roles

| Rol | Responsabilidad | Entrada | Salida |
| --- | --- | --- | --- |
| Agente principal | Coordina la conversación o proceso | Mensaje/evento | Decisión o respuesta |
| Agente especialista | Resuelve una tarea específica | Solicitud estructurada | Resultado específico |
| Humano supervisor | Aprueba o corrige casos sensibles | Escalamiento | Decisión final |
| Sistema externo | Ejecuta acción o guarda dato | API/webhook | Confirmación/error |

## 2. Estados del proceso

Estados sugeridos:

- Nuevo
- En clasificación
- En atención automática
- Esperando datos del usuario
- Requiere humano
- Acción ejecutada
- Cerrado
- Error

## 3. Reglas de decisión

| Condición | Acción del agente | Escalamiento |
| --- | --- | --- |
| Intención clara y bajo riesgo | Responder o ejecutar | No |
| Información incompleta | Preguntar | No |
| Riesgo alto | Detener y escalar | Sí |
| Usuario molesto | Reconocer y escalar | Sí |
| Herramienta falla | Informar y registrar | Según impacto |

## 4. Handoffs

Un handoff debe incluir:

- Motivo del escalamiento.
- Resumen del caso.
- Datos capturados.
- Última acción realizada.
- Recomendación del agente.
- Nivel de urgencia.

## 5. Logs mínimos

Registrar:

- Fecha y hora.
- Usuario o conversación.
- Intención detectada.
- Acción ejecutada.
- Herramienta usada.
- Resultado.
- Error si existe.
- Escalamiento si aplica.

## 6. Métricas de orquestación

- Tiempo hasta primera respuesta.
- Porcentaje de resolución automática.
- Porcentaje de escalamiento correcto.
- Errores por herramienta.
- Casos reabiertos.
- Satisfacción del usuario.
- Conversión o resultado de negocio.

## 7. Modo degradado

Cuando una herramienta falla, el agente debe:

1. No inventar confirmaciones.
2. Informar con claridad si la acción no pudo completarse.
3. Registrar el error.
4. Ofrecer alternativa segura.
5. Escalar si el usuario necesita continuidad inmediata.


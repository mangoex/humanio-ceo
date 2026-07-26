# Pilotos de validación

## Propósito

Comprobar el framework fuera de ejemplos sintéticos y registrar evidencia, límites y aprendizaje.

| Piloto | Modalidad | Perfil | Riesgo | Resultado |
|---|---|---|---|---|
| `humanio-ceo` | Release autopilotado | Híbrido | R1 | `READY` para uso interno |
| `humanio-os` | Auditoría de adopción sin modificaciones | Híbrido | R2 | `NOT READY` para gobierno Humanio 1.0 |

## Criterio satisfecho

Los dos pilotos aplican clasificación, autoridad, validación, evidencia y decisión de readiness a repositorios reales. Los fixtures continúan cubriendo de forma determinista los tres perfiles.

## Límite

La auditoría de `humanio-os` no autoriza ni ejecuta su migración. La distribución pública de `humanio-ceo` tampoco concede derechos de reutilización a terceros mientras el propietario no publique una licencia.

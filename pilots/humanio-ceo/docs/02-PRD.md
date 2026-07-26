# Product Requirements Document

## Problema

La calidad del marco no puede depender de afirmaciones manuales ni de un checkout parcial.

## Personas

- Mantenedor que publica el plugin.
- Equipo que lo instala.
- Agente que inicia o audita un proyecto.

## Alcance y exclusiones

- Incluye: validación, inicialización segura, instalación local y paquete reproducible.
- Excluye: despliegue de aplicaciones consumidoras.

## Requisitos funcionales

### PRD-FR-001

El sistema debe crear y validar líneas base para los tres perfiles sin sobrescribir archivos existentes.

Criterio de aceptación: los tres perfiles pasan pruebas y fixtures estrictos.

## Requisitos no funcionales

### PRD-NFR-001

El sistema debe producir instalaciones y paquetes reproducibles sin dependencias externas de Python.

Métrica: dos paquetes del mismo árbol tienen el mismo SHA-256 y una instalación aislada pasa `doctor`.

## Criterios de éxito

- CI aprobado.
- Doce pruebas aprobadas.
- Workspace de autopiloto aprobado en modo estricto.

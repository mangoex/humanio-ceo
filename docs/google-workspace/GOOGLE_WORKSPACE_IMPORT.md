# Importar el CEO Framework a Google Workspace

## Objetivo

Convertir el paquete local del CEO Framework en archivos nativos de Google Docs, Google Sheets y Google Slides.

## Archivos generados

Los archivos estan en:

`exports/google-workspace/`

## Orden recomendado de importacion

1. Crear una carpeta en Google Drive llamada `Humanio CEO Framework`.
2. Subir todos los `.docx` y abrirlos con Google Docs.
3. Subir `Humanio_CEO_Workbook_Operativo.xlsx` y convertirlo a Google Sheets.
4. Subir `Humanio_CEO_Presentacion_Comercial.pptx` y convertirla a Google Slides.
5. Compartir la carpeta con el equipo o cliente segun corresponda.

## Uso de cada archivo

| Archivo | Tipo Google | Uso |
| --- | --- | --- |
| Manual Maestro | Docs | Explicar el marco conceptual CEO |
| Playbook de Implementacion | Docs | Ejecutar el proyecto paso a paso |
| Plantilla Diagnostico | Docs | Levantar informacion del cliente |
| Plantilla Blueprint | Docs | Definir el agente a construir |
| Ecosistema y Orquestacion | Docs | Mapear sistemas, datos, humanos y flujos |
| Entregable Ejecutivo | Docs | Presentar propuesta o resultado al cliente |
| Narrativa Comercial | Docs | Alinear mensaje de venta |
| Workbook Operativo | Sheets | Gestionar diagnostico, priorizacion, QA y gobierno |
| Presentacion Comercial | Slides | Explicar el metodo en reuniones |

## Estado de la integracion directa

En esta sesion, Google Drive permitio leer, listar y buscar archivos, pero bloqueo la creacion/subida con `403 Forbidden`.

Accion recomendada:

- Reconectar Google Drive concediendo permisos de crear/subir archivos.
- Reintentar la importacion automatica desde Codex.


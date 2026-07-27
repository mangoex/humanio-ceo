# Behavior-Driven Development

## Feature: PRD-FR-001 — Validación gobernada

### BDD-SC-001 — Autopiloto estricto

```gherkin
Given un workspace híbrido completo de Humanio CEO
When el CI ejecuta humanio validate con modo estricto
Then termina con código cero y sin advertencias
```

## Escenarios cubiertos

- Inicialización de tres perfiles.
- Colisiones de archivos.
- Placeholders.
- Archivos obligatorios.
- IDs duplicados e indefinidos.
- Instalación y paquete reproducible.

## Feature: PRD-FR-002 — CLI portable

### BDD-SC-002 — Instalación aislada

```gherkin
Given un paquete Humanio validado y un prefijo de usuario aislado
When el usuario instala el CLI portable
Then el lanzador ejecuta doctor fuera del checkout fuente
And una segunda instalación requiere actualización explícita
```

## Feature: PRD-FR-003 — Adaptadores reversibles

### BDD-SC-003 — Integración sin pérdida

```gherkin
Given un proyecto con instrucciones preexistentes
When Humanio instala y sincroniza un adaptador compatible
Then conserva el contenido preexistente
And administra únicamente su bloque delimitado
And registra adaptadores y destinos en el estado local
```

### BDD-SC-004 — Desinstalación segura

```gherkin
Given uno o varios adaptadores Humanio instalados
When el usuario desinstala un adaptador
Then solo se elimina el bloque administrado
And se conservan los demás adaptadores y el contenido del usuario
```

### BDD-SC-005 — Colisión de marcas

```gherkin
Given un archivo con una marca Humanio incompleta
When el usuario intenta instalar o sincronizar
Then la operación termina con error antes de escribir archivos
```

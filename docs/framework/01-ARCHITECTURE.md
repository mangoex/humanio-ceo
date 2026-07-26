# Arquitectura del framework

## Objetivo

Separar metodología, ejecución determinista y artefactos de proyecto para que el plugin sea reusable y mantenible.

## Capas

### 1. Gobierno

Contiene Constitución, autoridad, perfiles, riesgo, quality gates y control de cambios.

### 2. Skills

Interpretan la intención, seleccionan el flujo y aplican la metodología. Deben ser concisas y cargar referencias de forma progresiva.

### 3. Plantillas

Definen la estructura de los artefactos que el plugin crea dentro de proyectos objetivo.

### 4. Esquemas

Permiten validación estructural y salidas legibles por máquinas.

### 5. Scripts

Ejecutan validaciones repetibles: estructura, IDs, trazabilidad, placeholders, evidencias e impacto de cambios.

### 6. Fixtures

Prueban el framework sobre casos conversacionales, software e híbridos anonimizados.

## Flujo

1. Recibir idea, requisitos, prompt, documentos o repositorio.
2. Seleccionar modo.
3. Seleccionar perfil.
4. Clasificar riesgo.
5. Inventariar fuentes.
6. Crear o auditar la línea base.
7. Ejecutar gates.
8. Producir reporte y siguiente incremento.

## Modos

- `intake`
- `audit`
- `bootstrap`
- `update`
- `verify`
- `compile`

## Roles de ejecución

- Arquitecto: resuelve contexto, diseño y decisiones.
- Constructor: implementa el incremento aprobado.
- Verificador: ejecuta pruebas y comprueba trazabilidad.
- Auditor: revisa riesgo, seguridad y evidencia cuando corresponda.

Los roles pueden ser asumidos por uno o varios agentes según complejidad. El framework no exige una cadena multiagente fija.

## Estructura objetivo

```text
.codex-plugin/
skills/
templates/
schemas/
scripts/
tests/
examples/
docs/
```

Las integraciones externas se mantendrán desacopladas. Solo se añadirá `.mcp.json` o `.app.json` cuando exista una capacidad implementada y necesaria.

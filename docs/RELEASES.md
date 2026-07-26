# Releases

## Política de versiones

Humanio CEO usa SemVer:

- Mayor: cambio incompatible en estructura, manifiesto, IDs o comportamiento esperado.
- Menor: capacidad compatible, nueva skill, plantilla o validación.
- Parche: corrección compatible.

`VERSION`, `.codex-plugin/plugin.json` y `templates/common/PROJECT_MANIFEST.yaml` deben coincidir.

## Checklist

1. Actualizar versión y changelog.
2. Ejecutar `python3 scripts/humanio.py doctor`.
3. Compilar scripts.
4. Ejecutar todas las pruebas.
5. Validar plugin y skills.
6. Ejecutar fixtures estrictos.
7. Crear paquete reproducible.
8. Revisar diff y riesgos.
9. Fusionar mediante PR.
10. Crear tag o release únicamente después de que `main` esté validada.

## Paquete

```bash
python3 scripts/package_plugin.py
```

El archivo resultante excluye pruebas, fixtures, cachés y metadatos Git. Dos ejecuciones sobre el mismo contenido producen los mismos bytes.

## Compatibilidad

La serie 1.x conserva:

- `schema_version: 1`.
- Perfiles `conversational`, `software` e `hybrid`.
- Riesgos R0 a R3.
- Namespaces publicados.
- Comandos `doctor`, `init` y `validate`.

Una futura incompatibilidad debe elevar la versión mayor e incluir guía de migración.

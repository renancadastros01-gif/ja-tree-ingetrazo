# Contribuir a JA Tree

**Alcance de esta separación:** este repositorio contiene el plugin, su documentación y el ZIP instalable. Los comandos de pruebas y empaquetado descritos abajo pertenecen al entorno o paquete de fuentes original; sus carpetas `tests/`, `scripts/` y `.reference/` no se incluyen aquí. No se presentan como comandos ejecutables desde esta copia.


JA Tree 0.1.0 es un plugin de código abierto para IngeTrazo. El código, los iconos,
las traducciones, la documentación y el ejemplo de este proyecto se distribuyen
bajo **GPL-3.0-or-later**. Las contribuciones se realizan bajo esa misma licencia.
El texto completo está en LICENSE.

## Entorno reproducible

Descomprime el paquete de código fuente y trabaja desde su raíz. Requiere
Python 3.10 o posterior, Git y las dependencias del anfitrión. IngeTrazo se
descarga por separado; no está incluido en JA Tree.

```sh
git clone https://github.com/ingelibre/ingetrazo.git .reference/ingetrazo
git -C .reference/ingetrazo checkout 6be29fe
python3 -m venv dev-env
dev-env/bin/python -m pip install -r .reference/ingetrazo/requirements.txt
dev-env/bin/python -m pytest tests/test_outliner.py -q
dev-env/bin/python scripts/preview_outliner.py
dev-env/bin/python scripts/build_outliner_release.py
```

En Windows sustituye dev-env/bin/python por dev-env/Scripts/python.exe.
La prueba de convivencia se omite cuando no están presentes las otras
extensiones del repositorio de desarrollo. Las pruebas restantes usan el código
real del anfitrión. Las capturas Qt no sustituyen una prueba manual de instalación
en el binario de IngeTrazo.

## Cambios

- Describe el problema, la versión del anfitrión y cómo reproducirlo.
- Mantén las operaciones reversibles y la geometría, identidades y datos de
  otros plugins al organizar el árbol.
- Conserva el identificador interno outliner para evitar instalaciones duplicadas
  y mantener preferencias de las versiones de desarrollo anteriores.
- Actualiza los tres catálogos de outliner/locales juntos. No traduzcas los nombres
  o etiquetas que pertenecen al documento del usuario.
- Añade pruebas cuando cambie la selección, el historial, las transformaciones
  o la persistencia. Para traducciones, verifica claves y marcadores de formato.
- Ejecuta las pruebas y comprueba las capturas antes de preparar una versión.

## Publicar

El script de compilación genera un ZIP instalable y otro de código fuente en
dist. Publica el código fuente correspondiente junto con el instalador e incluye
LICENSE y NOTICES.md. Excluye dev-env, .reference, .plugin_backups, cachés y datos
personales. El paquete de fuentes ya excluye esos elementos. La versión 0.1.0
es la primera versión pública; las versiones anteriores eran de desarrollo.

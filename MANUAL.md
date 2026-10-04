# JA Tree · Manual de usuario / User manual

**Versión / Version 0.1.0 · IngeTrazo 0.5.7 (API de extensiones 2) · Julio Angulo · GPL-3.0-or-later**

[Español](#español) · [English](#english)

---

## Español

### 1. ¿Qué es JA Tree?

JA Tree es un **árbol del modelo** (outliner): un panel que muestra todos los
**grupos, componentes y planos de sección** del modelo como una jerarquía, para
encontrarlos, seleccionarlos, ocultarlos, renombrarlos y reorganizarlos sin tener
que buscarlos en la vista 3D. Es especialmente útil en modelos grandes organizados
por niveles, muros, mobiliario, paisajismo, etc.

Todo lo que hace usa los objetos nativos de IngeTrazo: si quitas la extensión, la
jerarquía del modelo sigue intacta.

### 2. Instalación

1. Descarga `ja_tree-0.1.0.zip` desde el catálogo de IngeTrazo o desde
   [las versiones del repositorio](https://github.com/wrc86/ja-tree-ingetrazo/releases).
2. Descomprímelo. Obtendrás una carpeta llamada **`outliner`** (nombre interno,
   se conserva para actualizar instalaciones anteriores y sus preferencias).
3. En IngeTrazo abre **Extensiones → Abrir carpeta de plugins** y copia allí la
   carpeta `outliner` completa, con sus iconos.
4. Reinicia IngeTrazo.

**Desinstalar:** cierra IngeTrazo y borra la carpeta `outliner`.

### 3. Abrir el panel

- **Extensiones → JA Tree…**
- **Ventana → Paneles → JA Tree**
- Atajo **Ctrl+Alt+O** (macOS: **Cmd+Alt+O**), si está libre.

### 4. El panel

- **Barra superior:** campo **Buscar nombre o etiqueta…**, filtro (**Todos los
  objetos**, Grupos, Componentes, Planos de sección), botón **lupa** (encuadrar),
  botón **mira** (localizar la selección de la vista 3D en el árbol) y botón de
  **opciones**.
- **Ruta:** cuando estás editando dentro de un grupo, aparece «Editando: …» con la
  ruta, y un botón para salir.
- **Árbol:** raíz **Modelo**, con iconos distintos para grupos y componentes, y una
  sección **Planos de sección** al final.
  - Los contenedores abiertos se muestran en **negrita**.
  - Los objetos ocultos se muestran en *cursiva*.
  - Columna de **etiqueta** y **candado** si la etiqueta está bloqueada.
- **Pie:** «X de Y objetos · Z seleccionados».

### 5. Uso

| Acción | Cómo |
|---|---|
| **Expandir / contraer** | Flechas del árbol, u Opciones → **Expandir todo** / **Contraer todo**. |
| **Seleccionar** | Clic en el nombre. **Ctrl/Cmd** o **Mayús** para varios (del mismo contenedor). La selección se sincroniza con la vista 3D en ambos sentidos. |
| **Editar (entrar al grupo)** | **Doble clic** o **Intro**. **Esc** o el botón de salir sube un nivel. |
| **Renombrar** | **F2** o clic derecho → **Renombrar**; escribe y pulsa Intro (1 a 256 caracteres). |
| **Buscar** | Escribe en el buscador: busca por nombre, etiqueta o símbolo del corte, sin distinguir mayúsculas ni tildes. Los contenedores de los resultados siguen visibles. |
| **Ocultar / mostrar** | Clic en el **ojo** (afecta al objeto y a sus hijos). Para varios: clic derecho → **Ocultar** / **Mostrar**. |
| **Encuadrar** | Botón **lupa**, tecla **F** o clic derecho → **Encuadrar**. |
| **Localizar** | Botón **mira**, o en la vista 3D clic derecho → **Localizar en JA Tree**: quita filtros y muestra la selección en el árbol. |
| **Anidar** | **Arrastra** un grupo/componente sobre otro. |
| **Sacar al nivel raíz** | Arrastra sobre **Modelo** o clic derecho → **Mover al nivel del modelo**. |
| **Reordenar** | Arrastra entre hermanos (desactiva antes **Ordenar por nombre (A–Z)**). |
| **Asignar etiqueta** | Clic derecho → **Asignar etiqueta…** (usa las etiquetas existentes). |
| **Eliminar** | Clic derecho → **Eliminar**. Todo el lote se deshace en un solo paso. |

**Orden A–Z:** con Opciones → **Ordenar por nombre (A–Z)** el orden es «natural»:
«Elemento 2» va antes que «Elemento 10».

**Columna de etiquetas:** se oculta sola si el panel mide menos de 330 px; también
puedes ocultarla con Opciones → **Mostrar etiquetas**.

#### Planos de sección

Aparecen en la sección **Planos de sección**. Haz clic en su indicador para
**activar o desactivar** el corte (solo uno puede estar activo a la vez). Se pueden
seleccionar, renombrar y eliminar. No se pueden anidar en grupos.

### 6. Idioma

Opciones → **Idioma**: **Español**, **English**, **Français** o **Automático (IngeTrazo)**
(sigue el idioma del programa; si no está disponible, usa inglés). El cambio es
inmediato y se recuerda.

### 7. Reglas importantes

- **Ocultación heredada:** si el padre o la etiqueta de un objeto está oculto, el objeto
  sigue invisible aunque lo muestres; el panel lo indica («Oculto por un contenedor o
  etiqueta»).
- **Etiquetas bloqueadas:** el candado indica que la etiqueta del objeto o de un antecesor
  está bloqueada. No se puede editar, mover ni eliminar hasta desbloquearla en el panel
  nativo de **Etiquetas**.
- **Posición:** al mover objetos entre contenedores **conservan su posición 3D**, aunque
  los grupos tengan rotación, escala o reflexión.
- **Componentes:** reorganizar afecta solo a la instancia elegida, no a las demás copias.
  Renombrar cambia el nombre de la instancia, no de la definición.
- **Geometría suelta:** caras y aristas sueltas no aparecen en el árbol; agrúpalas primero.
- No se permiten ciclos (un grupo dentro de sí mismo), destinos con escala cero, ni
  reorganizar una vista explotada sin reensamblarla.
- Para organizar, **sal de la edición del grupo** primero.

### 8. Guardar y deshacer

Renombrar, ocultar, etiquetar, reorganizar, activar cortes y eliminar se pueden
**deshacer**. Guarda como **.igz** para conservar jerarquía, nombres, etiquetas y
visibilidad. El orden A–Z y la columna de etiquetas son preferencias personales.

Abre `Ejemplo_JA_Tree.igz` (incluido en el repositorio; guárdalo fuera de la carpeta
de plugins) para ver una casa organizada por niveles, muros, aberturas, mobiliario,
paisajismo y planos de sección.

### 9. Problemas frecuentes

| Mensaje / problema | Solución |
|---|---|
| «Para selección múltiple, elija objetos del mismo contenedor» | Selecciona solo hermanos. |
| «Desactive el orden A–Z para reordenar entre hermanos» | Opciones → desmarca **Ordenar por nombre (A–Z)**. |
| «Salga de la edición del grupo antes de organizar el modelo» | Pulsa **Esc** hasta volver al nivel del modelo. |
| «La etiqueta del destino está bloqueada» | Desbloquea la etiqueta en el panel de Etiquetas. |
| Un objeto no aparece | Puede ser geometría suelta: agrúpala. O revisa el filtro y la búsqueda. |
| No aparece en el menú | La carpeta debe llamarse `outliner` y contener `__init__.py`; reinicia IngeTrazo. |

### Autor

**Julio Eduardo Angulo** — arquitecto colombiano, fundador y director de diseño de
**[Línea Prima](https://lineaprima.co)**, estudio de arquitectura, diseño y construcción
en Bogotá. Desde 2009 proyecta y construye, con 77 proyectos en Colombia, Puerto Rico
y Estados Unidos, bajo un modelo *Design & Build*: un mismo equipo del concepto a la obra
terminada. Línea Prima hace «arquitectura para durar»: atmósfera, materia honesta y
precisión. Estas extensiones nacen de su práctica diaria con BIM y herramientas digitales.

- Web: [lineaprima.co](https://lineaprima.co) · Perfil: [lineaprima.co/julio-eduardo-angulo](https://lineaprima.co/julio-eduardo-angulo/)
- Correo: info@lineaprima.co · Instagram: [@buskua.co](https://instagram.com/buskua.co)
- Código y reportes de errores: [github.com/wrc86/ja-tree-ingetrazo](https://github.com/wrc86/ja-tree-ingetrazo/issues)

---

## English

### 1. What is JA Tree?

JA Tree is a **model outliner**: a panel listing all **groups, components and section
planes** as a hierarchy, so you can find, select, hide, rename and reorganise them
without hunting in the 3D view. It is fully translated into **English, Spanish and
French**. It uses native IngeTrazo objects; removing the extension leaves the hierarchy intact.

### 2. Installation

1. Download `ja_tree-0.1.0.zip` from the IngeTrazo catalog or the
   [repository releases](https://github.com/wrc86/ja-tree-ingetrazo/releases).
2. Unzip it. You get a folder named **`outliner`** (internal name, kept for upgrades).
3. In IngeTrazo open **Extensions → Open plugins folder** and copy the whole folder there.
4. Restart IngeTrazo.

**Uninstall:** close IngeTrazo and delete the `outliner` folder.

### 3. Opening the panel

**Extensions → JA Tree…**, **Window → Panels → JA Tree**, or **Ctrl+Alt+O** (macOS: **Cmd+Alt+O**).

### 4. The panel

- **Top bar:** **Search name or tag…**, a filter (**All objects**, Groups, Components,
  Section planes), **magnifier** (zoom), **crosshair** (locate the 3D selection in the
  tree) and **Tree options**.
- **Path:** while editing inside a group, «Editing: …» and a leave button.
- **Tree:** root **Model**, groups and components with their own icons, and a
  **Section planes** section. Open containers in **bold**, hidden objects in *italics*,
  a **tag** column and a **lock** when the tag is locked.
- **Footer:** «X of Y objects · Z selected».

### 5. Usage

| Action | How |
|---|---|
| **Expand / collapse** | Tree arrows, or Options → **Expand all** / **Collapse all**. |
| **Select** | Click the name; **Ctrl/Cmd** or **Shift** for several (same container). Synced with the 3D view both ways. |
| **Edit (enter group)** | **Double-click** or **Enter**. **Esc** or the leave button goes up one level. |
| **Rename** | **F2** or right-click → **Rename**, type, Enter. |
| **Search** | Name, tag or section symbol; case- and accent-insensitive. |
| **Hide / show** | Click the **eye** (object and children). For several: right-click → **Hide** / **Show**. |
| **Zoom to** | **Magnifier**, **F** or right-click → **Zoom to selection**. |
| **Locate** | **Crosshair**, or right-click in the 3D view → **Locate in JA Tree**. |
| **Nest** | **Drag** a group/component onto another. |
| **Move to root** | Drag onto **Model** or right-click → **Move to model root**. |
| **Reorder** | Drag between siblings (turn off **Sort by name (A–Z)** first). |
| **Assign tag** | Right-click → **Assign tag…**. |
| **Delete** | Right-click → **Delete** (one undo step for the batch). |

**Sorting** is natural («Item 2» before «Item 10»). The tag column hides automatically
below 330 px, or via Options → **Show tags**.

**Section planes:** click the indicator to turn a cut on/off (only one active at a time).
They can be selected, renamed and deleted, but not nested.

### 6. Language

Options → **Language**: **Español**, **English**, **Français** or **Automatic (IngeTrazo)**
(follows the app; falls back to English). Takes effect immediately and is remembered.

### 7. Important rules

- An object hidden by its parent or tag stays invisible even if you show it; the panel says so.
- A **lock** means the object's (or an ancestor's) tag is locked: unlock it in IngeTrazo's
  **Tags** panel before editing, moving or deleting.
- Moving between containers **keeps 3D positions**, even with rotation, scale or mirroring.
- Reorganising a component affects only that instance; renaming renames the instance.
- Loose faces/edges are not listed — group them first.
- Leave group editing before reorganising.

### 8. Saving and undo

All changes are **undoable**. Save as **.igz** to keep hierarchy, names, tags and
visibility. Open `Ejemplo_JA_Tree.igz` (in the repository; save it outside the plugins
folder) for a sample house organised by levels, walls, openings, furniture, landscape
and section planes.

### 9. Troubleshooting

| Message / problem | Fix |
|---|---|
| Multi-select across containers refused | Select siblings only. |
| "Turn off A–Z sorting to reorder" | Options → untick **Sort by name (A–Z)**. |
| "Leave group editing before organising" | Press **Esc** until you are at model level. |
| "Target tag is locked" | Unlock the tag in the Tags panel. |
| Object missing | It may be loose geometry (group it), or check search/filter. |
| Not in the menu | Folder must be named `outliner` and contain `__init__.py`; restart IngeTrazo. |

### Author

**Julio Eduardo Angulo** — Colombian architect, founder and design director of
**[Línea Prima](https://lineaprima.co)**, an architecture, design and construction studio
in Bogotá. Designing and building since 2009, with 77 projects in Colombia, Puerto Rico
and the United States under a *Design & Build* model: one team from concept to finished
building. Línea Prima makes "architecture to last": atmosphere, honest materials and
precision. These extensions come from his daily practice with BIM and digital tools.

- Web: [lineaprima.co](https://lineaprima.co) · Profile: [lineaprima.co/julio-eduardo-angulo](https://lineaprima.co/julio-eduardo-angulo/)
- Email: info@lineaprima.co · Instagram: [@buskua.co](https://instagram.com/buskua.co)
- Code and bug reports: [github.com/wrc86/ja-tree-ingetrazo](https://github.com/wrc86/ja-tree-ingetrazo/issues)
